# Publishing to the ESS AI Knowledge Hub

Build → Document → Publish → Search → Reuse.

1. Finish a reusable AI capability (MCP connector, RAG pattern, agent, integration, prompt, automation, reusable component).
2. Run `prompts/knowledge/01-create-ess-ai-knowledge-document.md`. The output follows `templates/knowledge-hub-document.md`.
3. Save it to `.ess-ai/reports/knowledge-<name>.md` and have your lead confirm it is worth publishing.
4. Publish through the approved MCP / OneDrive workflow to the Hub folder for its category:

```
ESS AI Knowledge Hub
├── MCP Connectors
├── AI Agents
├── RAG / pgvector
├── Integrations
├── Prompts
├── Automations
├── Reusable Code
├── Testing Assets
└── Security Patterns
```

5. Add a row to `.ess-ai/context/reuse-catalog.md` in projects that should know about it.
