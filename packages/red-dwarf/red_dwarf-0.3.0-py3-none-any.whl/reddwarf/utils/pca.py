from numpy.typing import ArrayLike
import pandas as pd
import numpy as np
from reddwarf.utils.matrix import VoteMatrix, generate_virtual_vote_matrix
from reddwarf.sklearn.transformers import SparsityAwareCapturer, SparsityAwareScaler
from reddwarf.sklearn.pipeline import PatchedPipeline
from typing import Tuple

from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer


def run_pca(
        vote_matrix: VoteMatrix,
        n_components: int = 2,
) -> Tuple[ pd.DataFrame, pd.DataFrame, PCA ]:
    """
    Process a prepared vote matrix to be imputed and return projected participant data,
    as well as eigenvectors and eigenvalues.

    The vote matrix should not yet be imputed, as this will happen within the method.

    Args:
        vote_matrix (pd.DataFrame): A vote matrix of data. Non-imputed values are expected.
        n_components (int): Number n of principal components to decompose the `vote_matrix` into.

    Returns:
        projected_data (pd.DataFrame): A dataframe of projected xy coordinates for each `vote_matrix` row/participant.
        pca (PCA): PCA object, notably with the following attributes:
            - components_ (List[List[float]]): Eigenvectors of principal `n` components, one per column/statement/feature.
            - explained_variance_ (List[float]): Explained variance of each principal component.
            - mean_ (list[float]): Means/centers of each column/statements/features.
    """
    pipeline = PatchedPipeline([
        ("capture", SparsityAwareCapturer()),
        ("impute", SimpleImputer(missing_values=np.nan, strategy="mean")),
        ("pca", PCA(n_components=n_components)),
        ("scale", SparsityAwareScaler(capture_step="capture")),
    ])

    pipeline.fit(vote_matrix.values)

    # Generate projections of participants.
    X_participants = pipeline.transform(vote_matrix.values)

    # Generate projections of statements via virtual vote matrix.
    # This projects unit vectors for each feature/statement into PCA space to
    # understand their placement.
    n_statements = len(vote_matrix.columns)
    virtual_vote_matrix = generate_virtual_vote_matrix(n_statements)
    X_statements = pipeline.transform(virtual_vote_matrix)

    DEFAULT_DIMENSION_LABELS = ["x", "y", "z"]
    dimension_labels = DEFAULT_DIMENSION_LABELS[:n_components]

    projected_participants = pd.DataFrame(
        X_participants,
        index=pd.Index(vote_matrix.index, name="participant_id"),
        columns=np.asarray(dimension_labels),
    )

    projected_statements = pd.DataFrame(
        X_statements,
        index=pd.Index(vote_matrix.columns, name="statement_id"),
        columns=np.asarray(dimension_labels),
    )

    pca = pipeline.named_steps["pca"]

    return projected_participants, projected_statements, pca

def calculate_extremity(projections: ArrayLike):
    # Compute extremity as vector magnitude on rows.
    # vector magnitude = Euclidean norm = hypotenuse of xy
    return np.linalg.norm(projections, axis=0)