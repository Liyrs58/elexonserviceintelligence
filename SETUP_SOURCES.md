# Setup sources

Checked on 2026-09-09. Only official Microsoft, Microsoft GitHub, OpenAI, and official package-registry material was used for the Power BI/Codex setup.

## Microsoft

- [Power BI MCP server documentation](https://learn.microsoft.com/en-us/power-bi/developer/mcp/)
- [Power BI agentic overview](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-agentic-overview)
- [Install Skills for Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/skills-for-fabric-install)
- [Microsoft skills-for-fabric repository](https://github.com/microsoft/skills-for-fabric)
- [Official powerbi-authoring plugin manifest](https://github.com/microsoft/skills-for-fabric/blob/main/plugins/powerbi-authoring/.github/plugin/plugin.json)
- [Power BI Modeling MCP package](https://www.npmjs.com/package/@microsoft/powerbi-modeling-mcp)
- [Power BI report authoring CLI package](https://www.npmjs.com/package/@microsoft/powerbi-report-authoring-cli)
- [Microsoft .NET installation script](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script)
- [Microsoft Power BI Modeling MCP macOS/.NET startup issue](https://github.com/microsoft/powerbi-modeling-mcp/issues/108)
- [Microsoft Power BI Modeling MCP macOS code-signing issue](https://github.com/microsoft/powerbi-modeling-mcp/issues/115)
- [Power BI service](https://app.powerbi.com/)

## OpenAI / Codex

- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Codex skill discovery locations](https://learn.chatgpt.com/docs/build-skills)
- [GPT-6 Astra model guidance](https://developers.openai.com/api/docs/guides/latest-model)

## Pinned local source state

- `microsoft/skills-for-fabric` commit: `74f3262c1c3fcc6d2346daaf479af88b946a3c6b`
- `powerbi-authoring` bundle version: `0.3.15`
- `@microsoft/powerbi-modeling-mcp`: `0.5.0-beta.13`
- `@microsoft/powerbi-report-authoring-cli`: `0.1.4`
- Microsoft .NET runtime: `8.0.31` (`osx-arm64`, local tooling install)
