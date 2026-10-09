# RAG and MCP Rule
RAG / pgvector: start from the ESS semantic-search pattern (recorded embedding model and dimensions, pgvector, HNSW cosine index, dense + lexical retrieval, RRF, cross-encoder rerank). Keep vector records tenant-scoped. Test retrieval, grounding and stale data.

MCP / tools: every tool needs a contract, authentication, an authorization boundary, input and output validation, error handling, audit logging and rate/timeout limits. The model never gets direct, unrestricted database or customer-environment access; it calls registered tools.
