from typing import Optional
import numpy as np
from numpy.typing import ArrayLike
from sklearn.cluster import KMeans, kmeans_plusplus
from sklearn.utils.validation import check_random_state, check_array

class PolisKMeans(KMeans):
    """
    A modified version of scikit-learn's KMeans that allows partial initialization
    with user-supplied cluster centers and custom fallback strategies.

    This subclass extends `sklearn.cluster.KMeans` with additional features
    around centroid initialization. Outside the behavior documented, it retains
    all other parameters and behavior from the base KMeans implementation.

    Parameters
    ----------

    init : {'k-means++', 'random', 'polis'}, default='k-means++'
        Strategy to initialize any missing cluster centers if `init_centers` is
        not fully specified. The strategies are:

        - 'k-means++': Smart centroid initialization (same as scikit-learn default)
        - 'random': Random selection of initial centers from the data (same as scikit-learn)
        - 'polis': Selects the first unique data points in `X` as initial centers.
            - This strategy is deterministic for any stable set of `X`, while
            determinism in the other strategies depends on `random_state`.

        !!! note
            Unlike `KMeans` parent class, we prevent passing `ndarray` args
            here, and expect `init_centers` to handle that use-case.

    init_centers : ndarray of shape (n_clusters, n_features), optional
        Initial cluster centers to use. May contain fewer (or more) than `n_clusters`:

        - If more, the extras will be trimmed
        - If fewer, the remaining will be filled using the `init` strategy

    Attributes
    ----------

    init_centers_used_ : ndarray of shape (n_clusters, n_features)
        The full array of initial cluster centers actually used to initialize the algorithm,
        including both `init_centers` and any centers generated from the `init` strategy.

    See Also
    --------

    `sklearn.cluster.KMeans` : Original implementation with full parameter list.
    """
    def __init__(
        self,
        n_clusters=8,
        init="k-means++",  # or 'random', 'polis'
        init_centers: Optional[ArrayLike] = None,  # array-like, optional
        n_init="auto",
        max_iter=300,
        tol=1e-4,
        verbose=0,
        random_state=None,
        copy_x=True,
        algorithm="lloyd",
    ):
        super().__init__(
            n_clusters=n_clusters,
            init=init,  # will override via set_params, with our center selection logic below
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            algorithm=algorithm,
        )
        self._init_strategy = init
        self.init_centers = init_centers
        self.init_centers_used_ = None

    def _generate_centers(self, X, x_squared_norms, n_to_generate, random_state):
        if not isinstance(self._init_strategy, str):
            raise ValueError("Internal error: _strategy must be a string.")

        if self._init_strategy == "k-means++":
            centers, _ = kmeans_plusplus(
                X, n_clusters=n_to_generate,
                random_state=random_state,
                x_squared_norms=x_squared_norms
            )
        elif self._init_strategy == "random":
            indices = random_state.choice(X.shape[0], n_to_generate, replace=False)
            centers = X[indices]
        elif self._init_strategy == "polis":
            unique_X = np.unique(X, axis=0)
            if len(unique_X) < n_to_generate:
                raise ValueError("Not enough unique rows in X for 'polis' strategy.")
            centers = unique_X[:n_to_generate]
        else:
            raise ValueError(f"Unsupported init strategy: {self._init_strategy}")
        return centers

    def fit(self, X, y=None, sample_weight=None):
        X = check_array(X, accept_sparse="csr", dtype=[np.float64, np.float32]) # type:ignore
        random_state = check_random_state(self.random_state)
        x_squared_norms = np.sum(X ** 2, axis=1)

        # Determine init_centers_used_
        if self.init_centers is not None:
            init_array = np.array(self.init_centers)
            if init_array.ndim != 2 or init_array.shape[1] != X.shape[1]:
                raise ValueError("init_centers must be of shape (n, n_features)")

            n_given = init_array.shape[0]
            if n_given > self.n_clusters:
                init_array = init_array[:self.n_clusters]
            elif n_given < self.n_clusters:
                needed = self.n_clusters - n_given
                extra = self._generate_centers(X, x_squared_norms, needed, random_state)
                init_array = np.vstack([init_array, extra])
            self.init_centers_used_ = init_array.copy()
        else:
            self.init_centers_used_ = self._generate_centers(
                X, x_squared_norms, self.n_clusters, random_state
            )

        # Override the init param passed to sklearn with actual centers.
        # We take control of the initialization strategy (`k-means++`, `random`,
        # `polis`, etc) in our own code.
        super().set_params(init=self.init_centers_used_)

        return super().fit(X, y=y, sample_weight=sample_weight)

from sklearn.base import BaseEstimator, TransformerMixin

class PolisKMeansDownsampler(BaseEstimator, TransformerMixin):
    """
    A transformer that fits `PolisKMeans` and returns the cluster centers as the
    downsampled dataset.

    This will support mimicking "base clusters" from the Polis platform.

    This enables use in sklearn pipelines, where intermediate steps
    are expected to implement both `fit` and `transform`.
    """
    def __init__(self,
        n_clusters=100,
        random_state=None,
        init="k-means++",
        init_centers=None,
    ):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.init = init
        self.init_centers = init_centers
        self.kmeans_ = None

    def fit(self, X, y=None):
        self.kmeans_ = PolisKMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            init=self.init,
            init_centers=self.init_centers,
        )
        self.kmeans_.fit(X)
        return self

    def transform(self, X, y=None):
        return self.kmeans_.cluster_centers_ if self.kmeans_ else None