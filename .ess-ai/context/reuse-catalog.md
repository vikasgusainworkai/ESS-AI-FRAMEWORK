# ESS Reuse Catalogue

From framework page 09 "What ESS has already built". Before designing something new, find the closest entry, contact the owning team, review architecture/code/prompts/tools, reuse, and extend only where required. Fill the owner and repository columns for your organization.

| # | Implementation | Pattern | Reuse when the requirement needs… | Owner team | Repository / docs |
|---|---|---|---|---|---|
| 1 | PGVector semantic search — MaxxHire | Text extraction → embedding (all-MiniLM-L6-v2, 384d) → PostgreSQL + pgvector (HNSW, cosine) → dense + lexical → RRF → cross-encoder rerank (ms-marco-MiniLM-L-6-v2); CPU only | Semantic similarity, document / ticket / candidate matching, recommendations | | |
| 2 | Oracle MCP | Agent → MCP server → registered Oracle tool (connection test, list tables/views, describe, DDL, approved queries, sequences, indexes, constraints) → validated result | ERP / database agent access without direct DB integration | | |
| 3 | MCP external integrations — MaxxHire | Agent → MCP connector → authentication → authorized tool → Google / Microsoft / Zoom / LinkedIn → validated response | Controlled access to an external platform | | |
| 4 | KM / RAG knowledge management | Documents → metadata → chunks → embeddings → pgvector → retrieval → rerank → grounded answer | Document search, enterprise knowledge, Q&A | | |
| 5 | Multi-tenancy model | Login → tenant context → authorization → scoped API/tool → scoped DB/vector/files → AI response | Any multi-tenant AI feature | | |
| 6 | ERP AI support assistant & RCA engine | New issue → embedding similarity → similar historical tickets → engineer remarks → previous resolution → RCA insight | Support, incident, service-desk use cases | | |
| 7 | AI testing agent | Test cases → AI test agent → open app → execute → expected vs actual → PASS/FAIL + evidence | Scalable screen-level functional testing | | |
| 8 | Data extraction & migration agents | Understand source → extract → transform → validate → load → report → human verification | Migration, conversion, repeatable data processing | | |
| 9 | Business / ERP intelligent agents (EVA, sales, P2P) | Request → agent → LLM reasoning → tool/API/MCP → ERP data → validation → response/action | New ERP agent requirements | | |

Proposed (not yet built): AI ticket automation (ticket → understand → clarify → implement → test → ticket update). Do not assume it exists.
