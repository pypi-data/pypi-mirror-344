from collections.abc import Mapping

import numpy as np
import pandas as pd
from ortools.sat.python import cp_model as cp

from ..abc import Mapper
from ..typing import Array1D, BaseExplanation, Key, Number
from ._env import ENV
from ._variables import FeatureVar


class Explanation(Mapper[FeatureVar], BaseExplanation):
    _epsilon: float = 1e-8

    def vget(self, i: int) -> cp.IntVar:
        name = self.names[i]
        if self[name].is_one_hot_encoded:
            code = self.codes[i]
            return self[name].xget(code)
        return self[name].xget()

    def to_series(self) -> "pd.Series[float]":
        values: list[float] = [
            ENV.solver.Value(v) for v in map(self.vget, range(self.n_columns))
        ]
        for f in range(self.n_columns):
            name = self.names[f]
            value = ENV.solver.Value(self.vget(f))
            if self[name].is_continuous:
                value = self[name].levels[value + 1]
                values[f] = value - self._epsilon
            elif self[name].is_discrete:
                value = self[name].levels[value]
                values[f] = value - self._epsilon
        return pd.Series(values, index=self.columns)

    def to_numpy(self) -> Array1D:
        return (
            self.to_series()
            .to_frame()
            .T[self.columns]
            .to_numpy()
            .flatten()
            .astype(np.float64)
        )

    @property
    def x(self) -> Array1D:
        return self.to_numpy()

    @property
    def value(self) -> Mapping[Key, Key | Number]:
        solver = ENV.solver

        def get(v: FeatureVar) -> Key | Number:
            if v.is_one_hot_encoded:
                for code in v.codes:
                    if np.isclose(solver.Value(v.xget(code)), 1.0):
                        return code
            if v.is_discrete:
                return float(v.levels[solver.Value(v.xget())])
            if v.is_continuous:
                return float(v.levels[solver.Value(v.xget()) + 1])
            x = v.xget()
            return solver.Value(x)

        return self.reduce(get)

    def __repr__(self) -> str:
        mapping = self.value
        prefix = f"{self.__class__.__name__}:\n"
        root = self._repr(mapping)
        suffix = ""

        return prefix + root + suffix


__all__ = ["Explanation"]
