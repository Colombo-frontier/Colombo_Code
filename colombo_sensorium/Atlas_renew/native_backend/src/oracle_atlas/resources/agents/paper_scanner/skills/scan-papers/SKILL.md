---
name: scan-papers
description: "Search the literature broadly within approved tasks, years, and sources, verify bibliographic records, and produce a paper queue for extraction."
---

# Annual Paper Scanning Agent Skill

## Search and verification

1. Read the approved plan and task vocabulary, then query broad task + year. Do not form a Cartesian product over every smoothness, geometry, and oracle-precision choice. Perform a small amount of targeted supplementary search in response to observed gaps.
2. Use available arXiv, Crossref, and OpenAlex bibliographic tools, official journal/conference catalogs, configured MCP services, and web search as complementary sources. If a tool is unavailable, record the actual gap and use available sources; do not fabricate a search record. An LLM answer about relevant papers in a year supplies unverified leads only.
3. Verify candidate titles, authors, DOI/arXiv IDs, versions, and associated dates. Check the year under the plan's event_kind. Save new verified publication events and evidence rather than changing only the top-level year. Preserve publication events and provenance when merging versions/sources, without duplicating a complete nested record for every version.
4. Deduplicate DOI/arXiv records and explicitly identified versions of the same paper while retaining version differences. Abstracts may support relevance screening, but report the result as a relevant lead. Whether a setting should be extracted is for the extractor to decide after reading the source text.
5. Obtain full text for papers that advance, or state the full-text access gap. Store full texts as independent sources. paper_batch contains only fixed references and coverage descriptions, not entire papers or hundreds of unread abstracts.
6. Stop this batch at query_budget/paper_limit, preserving cursors, unverified leads, and next search directions. Report discovered, bibliography_verified, fulltext_available, and read separately; "185 bibliographic records" must not become "185 papers read in full."
7. Call schema_read(paper_batch) before saving queue results. During recovery, reuse search_refs/verified events rather than paying again for identical completed searches.
