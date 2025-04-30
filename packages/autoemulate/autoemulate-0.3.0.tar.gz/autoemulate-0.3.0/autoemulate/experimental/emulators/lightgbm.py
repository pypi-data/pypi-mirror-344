import numpy as np
from lightgbm import LGBMRegressor
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
from torch import Tensor

from autoemulate.experimental.emulators.base import (
    Emulator,
    InputTypeMixin,
)
from autoemulate.experimental.types import InputLike, OutputLike


class LightGBM(Emulator, InputTypeMixin):
    """LightGBM Emulator.

    Wraps LightGBM regression from LightGBM.
    See https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html
    for more details.
    """

    def __init__(  # noqa: PLR0913 allow too many arguments since all currently required
        self,
        x: InputLike | None = None,
        y: InputLike | None = None,
        boosting_type: str = "gbdt",
        num_leaves: int = 31,
        max_depth: int = -1,
        learning_rate: float = 0.1,
        n_estimators: int = 100,
        subsample_for_bin: int = 200000,
        objective: str | None = None,
        class_weight: dict | str | None = None,
        min_split_gain: float = 0.0,
        min_child_weight: float = 0.001,
        min_child_samples: int = 20,
        subsample: float = 1.0,
        colsample_bytree: float = 1.0,
        reg_alpha: float = 0.0,
        reg_lambda: float = 0.0,
        random_state: int | None = None,
        n_jobs: int | None = 1,
        importance_type: str = "split",
        verbose: int = -1,
    ):
        """Initializes a LightGBM object."""
        _, _ = x, y  # ignore unused arguments
        self.boosting_type = boosting_type
        self.num_leaves = num_leaves
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.subsample_for_bin = subsample_for_bin
        self.objective = objective
        self.class_weight = class_weight
        self.min_split_gain = min_split_gain
        self.min_child_weight = min_child_weight
        self.min_child_samples = min_child_samples
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.importance_type = importance_type
        self.verbose = verbose

    @staticmethod
    def is_multioutput() -> bool:
        return False

    def fit(self, x: InputLike, y: InputLike | None):
        """
        Fits the emulator to the data.
        The model expects the input data to be:
            x (features): 2D array
            y (target): 1D array
        """

        x, y = self._convert_to_numpy(x, y)

        if y is None:
            msg = "y must be provided."
            raise ValueError(msg)
        if y.ndim > 2:
            msg = f"y must be 1D or 2D array. Found {y.ndim}D array."
            raise ValueError(msg)
        if y.ndim == 2:  # _convert_to_numpy may return 2D y
            y = y.ravel()  # Ensure y is 1-dimensional

        self.n_features_in_ = x.shape[1]

        x, y = check_X_y(x, y, y_numeric=True)

        self.model_ = LGBMRegressor(
            boosting_type=self.boosting_type,
            num_leaves=self.num_leaves,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            n_estimators=self.n_estimators,
            subsample_for_bin=self.subsample_for_bin,
            objective=self.objective,
            class_weight=self.class_weight,
            min_split_gain=self.min_split_gain,
            min_child_weight=self.min_child_weight,
            min_child_samples=self.min_child_samples,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            reg_alpha=self.reg_alpha,
            reg_lambda=self.reg_lambda,
            random_state=self.random_state,
            n_jobs=self.n_jobs,
            importance_type=self.importance_type,
            verbose=self.verbose,
        )

        self.model_.fit(x, y)
        self.is_fitted_ = True

    def predict(self, x: InputLike) -> OutputLike:
        """Predicts the output of the emulator for a given input."""
        x = check_array(x)
        check_is_fitted(self, "is_fitted_")
        y_pred = self.model_.predict(x)
        # Ensure the output is a 2D tensor array with shape (n_samples, 1)
        return Tensor(y_pred.reshape(-1, 1))  # type: ignore PGH003

    @staticmethod
    def get_tune_config():
        # Note: 10 ** np.random.uniform(-3, 0)
        # is equivalent to scipy.stats.loguniform(0.001, 0.1)
        return {
            "num_leaves": [np.random.randint(10, 100)],
            "max_depth": [np.random.randint(-1, 12)],
            "learning_rate": [10 ** np.random.uniform(-3, -1)],
            "n_estimators": [np.random.randint(50, 1000)],
            "reg_alpha": [10 ** np.random.uniform(-3, 0)],
            "reg_lambda": [10 ** np.random.uniform(-3, 0)],
        }
