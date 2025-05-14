"""
Provides a lightweight TF-IDF embedding function to vectorize text
without relying on Hugging-Face/tokenizers (avoids parallelism warnings).
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Optional

_VECTORIZER: Optional[TfidfVectorizer] = None


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    On first call, fits a TfidfVectorizer on `texts` and returns vectors.
    On subsequent calls, transforms with the existing vectorizer.
    Returns dense float vectors.
    """
    global _VECTORIZER
    if _VECTORIZER is None:
        _VECTORIZER = TfidfVectorizer(
            max_features=4096,
            lowercase=True,
            stop_words="english"
        )
        mat = _VECTORIZER.fit_transform(texts)
    else:
        mat = _VECTORIZER.transform(texts)

    return [row.toarray().ravel().astype(float).tolist() for row in mat]
