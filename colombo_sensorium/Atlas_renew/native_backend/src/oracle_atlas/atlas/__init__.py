"""Read-only Atlas retrieval, dual tag projection, and transactional writes. Agents determine scientific identity."""

from .store import Atlas, AtlasError, AtlasConflict, AtlasValidationError
from .retrieval import retrieve
from .tags import AXES, effective_native_operations, match_interface, project_tags

__all__ = [
    "Atlas", "AtlasError", "AtlasConflict", "AtlasValidationError", "retrieve",
    "AXES", "effective_native_operations", "match_interface", "project_tags",
]
