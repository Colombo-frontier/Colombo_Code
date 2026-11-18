"""Source discovery and bibliographic verification; Agents determine scientific scope and setting extraction."""
from .bibliography import Bibliography, deduplicate_records, merge_records, qualifies_year, verify_publication
from .sources import fetch_source
from .http import DiscoveryError

__all__ = ["Bibliography", "fetch_source", "merge_records", "qualifies_year",
           "verify_publication", "deduplicate_records", "DiscoveryError"]
