import numpy as np
from scipy.spatial.distance import pdist, squareform
from functools import partial
from pacmap import PaCMAP

def masked_distance(u, v, far_value=np.inf):
    """
    Custom distance function that ignores missing values (NaN) when computing distance
    between two samples.

    Parameters
    ----------
    u, v : np.ndarray
        Two 1D arrays representing samples (participants).
    far_value : float
        Distance to assign if there are no overlapping (non-NaN) entries.

    Returns
    -------
    float
        The masked distance between u and v.
    """
    mask = ~np.isnan(u) & ~np.isnan(v)
    if not np.any(mask):
        return far_value
    return np.linalg.norm(u[mask] - v[mask]) / np.sqrt(mask.sum())

def build_neighbor_pairs(dists, k=10):
    """
    Build neighbor pairs from a distance matrix.

    Parameters
    ----------
    dists : np.ndarray
        Precomputed distance matrix (squareform).
    k : int
        Number of neighbors to select for each sample.

    Returns
    -------
    np.ndarray
        Array of shape (n_pairs, 2) listing neighbor pairs.
    """
    neighbor_pairs = []
    n_samples = dists.shape[0]
    for i in range(n_samples):
        neighbor_indices = np.argsort(dists[i])[:k+1]  # +1 because self is included
        neighbor_indices = neighbor_indices[neighbor_indices != i]  # remove self
        for j in neighbor_indices:
            neighbor_pairs.append([i, j])
    return np.array(neighbor_pairs)

class MaskedPaCMAP(PaCMAP):
    """
    PaCMAP variant that builds neighbor pairs using masked distances,
    ignoring missing values (NaNs) in the dataset.

    Parameters
    ----------
    n_neighbors : int, default=10
        Number of neighbors to use when constructing neighbor pairs.
    far_value : float, default=1e6
        Distance to assign to sample pairs with no shared non-NaN features.
    **kwargs
        Additional keyword arguments passed to the base PaCMAP class.
    """

    def __init__(self, n_neighbors=10, far_value=1e6, X_sparse=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_neighbors = n_neighbors
        self.far_value = far_value
        self.X_sparse = X_sparse

    def fit(self, X, init=None, save_pairs=True):
        """
        Fit the model from X and return the low-dimensional embedding.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data.

        y : Ignored

        Returns
        -------
        X_new : array of shape (n_samples, n_components)
            Embedding of the training data in low-dimensional space.
        """
        X_for_neighbors = self.X_sparse if self.X_sparse is not None else X

        masked_dist = partial(masked_distance, far_value=self.far_value)
        dists = squareform(pdist(X_for_neighbors, metric=masked_dist))
        neighbor_pairs = build_neighbor_pairs(dists, k=self.n_neighbors)
        self.neighbor_pairs = neighbor_pairs
        return super().fit(X, init, save_pairs)