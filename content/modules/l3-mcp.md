---
title: Model Context Protocol (MCP)
level: L3
kind: core
hours: 8–10
summary: Explain how MCP connects AI apps to tools and data, build and test an MCP server in Python, connect it to clients, and judge its security risks.
checked: 2026-10-16
review-by: 2027-01-31 | version 2 at the time of writing
review-by: 2027-01-31 | install `mcp>=1.28,<2`
review-by: 2027-04-30 | is deprecated in the 2026-07-28 protocol version
review-by: 2027-04-30 | the 2026-07-28 version made each request self-contained
---

## Why it matters
Before MCP, every AI app needed its own integration for every tool. A GitHub connector for one chat app did nothing for an IDE or for your own agent. The Model Context Protocol (MCP) is an open standard that fixes this. You write a server once, and any MCP-capable host can use its tools, data and prompts, including Claude, ChatGPT, VS Code, Cursor and many agent SDKs.

For you as an agent builder, MCP matters in two directions. You will connect your agents to existing servers instead of writing glue code, and you will publish your own tools as servers that other apps can use. Both directions carry real security risk. A server is code that runs with your permissions, and its text goes straight into the model's context.

## What to learn
- **Why a protocol**: Without a standard, M apps and N tools need M×N integrations. With MCP, each app implements a client and each tool provider implements a server, so the work drops to M+N.
- **Hosts, clients and servers**: The host is the AI application, such as a desktop chat app, an IDE or your agent. It creates one client per server connection. The server is a program that exposes capabilities and can run locally or remotely.
- **Server primitives**: Tools are functions the model can call. Resources are read-only data the app can load into context, such as a file or a database schema. Prompts are reusable templates a user can pick.
- **Client features**: Servers can ask the user for input or confirmation through elicitation. Sampling, where a server asks the host's model for a completion, is deprecated in the 2026-07-28 protocol version, so avoid it in new servers.
- **Messages and transports**: MCP messages are JSON-RPC 2.0, a simple JSON format in which each request names a method and carries an id that its response repeats. Local servers usually use stdio, where the host starts the server as a child process. Remote servers use Streamable HTTP. Protocol versions are dated, and the 2026-07-28 version made each request self-contained, so tutorials describing sessions and an initialize handshake refer to earlier versions.
- **Building a server**: The official Python SDK (version 2 at the time of writing) turns typed, documented functions into tools with a decorator. Version 2 renamed the main class: `from mcp.server import MCPServer` replaces version 1's `from mcp.server.fastmcp import FastMCP`. To follow a tutorial written for version 1, install `mcp>=1.28,<2` or use the SDK's migration guide. FastMCP is a standalone framework with a similar API plus client, auth and deployment helpers. In a stdio server, never print to stdout, because that corrupts the protocol stream; log to stderr instead.
- **Connecting to clients**: Desktop apps and IDEs take a JSON config naming the command that starts your server. Your own agent uses the SDK's client to list tools, pass them to the model and forward its tool calls. Test every server first with the MCP Inspector.
- **Authorization for remote servers**: Remote servers that touch user data should use the OAuth 2.1-based flow in the spec. Local stdio servers usually read credentials from environment variables instead.
- **Third-party server risks**: Tool descriptions can hide instructions (tool poisoning), a server can change its tools after you approve them (a rug pull), and one server can shadow another's tools. Install few servers, read their code, pin versions, grant least privilege and keep a human approving risky calls.

## Resources
### Start here
- [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) · MCP project · Docs · Free · 30 min — The official explanation of hosts, clients, servers, primitives and transports, with annotated JSON-RPC messages for discovery, tool calls and notifications.
- [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server) · MCP project · Tutorial · Free · 1.5 h — Builds a weather server with two tools in Python or another language and connects it to Claude Desktop, including the stdout logging trap.
- [MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/) · DeepLearning.AI · Course · Free tier · 2 h — Turns a paper-search chatbot into an MCP app, building a server with tools, resources and prompts, a client and a remote deployment.
### Go deeper
- [Build an MCP client](https://modelcontextprotocol.io/docs/develop/build-client) · MCP project · Tutorial · Free · 1.5 h — Shows how a chatbot connects to any MCP server, lists its tools and routes the model's tool calls, which is exactly what your agent needs.
- [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/unit0/introduction) · Hugging Face · Course · Free · self-paced — A free course with free certification that goes from fundamentals to an end-to-end and then a deployed MCP application.
- [Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security/authorization) · MCP project · Docs · Free · 45 min — Explains when a server needs authorization and walks through the OAuth 2.1 flow for remote servers.
- [Model Context Protocol has prompt injection security problems](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/) · Simon Willison · Article · Free · 15 min — Concrete examples of tool poisoning, rug pulls and tool shadowing, with practical advice for clients, servers and users.
- [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) · Anthropic · Article · Free · 20 min — Shows how agents can call MCP tools from code instead of loading every tool definition, cutting context use when many servers are connected.
### Reference
- [MCP specification](https://modelcontextprotocol.io/specification/latest) · MCP project · Docs · Free · reference — The authoritative, dated protocol definition to check whenever a tutorial and an SDK disagree.
- [Security Best Practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) · MCP project · Docs · Free · reference — Attacks and required mitigations, including confused deputy, token passthrough, SSRF, local server compromise and scope minimization.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) · MCP project · Repo · Free · reference — The official SDK for servers and clients, with examples and a migration guide from version 1 to version 2.
- [FastMCP](https://gofastmcp.com/getting-started/welcome) · FastMCP · Docs · Free · reference — A popular standalone framework for MCP servers, clients and auth, whose original API became the official SDK's high-level interface.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) · MCP project · Tool · Free · reference — A web, command-line and terminal tool for listing and calling a server's tools before any model touches them.

## Practice
1. **Notes server.** Build a stdio MCP server over a folder of Markdown notes with `search_notes`, `read_note` and `create_note` tools, plus a resource listing all note titles. Done when every tool works in the MCP Inspector.
2. **Connect a host.** Add your server to a desktop chat app or IDE that supports MCP. Done when a single question triggers two of your tools and you can see both calls in the app.
3. **Your agent as a client.** Connect the agent from [The agent loop](#l3-agent-loop) to your server with the SDK client, converting MCP tool listings into your provider's tool format. Done when the agent answers a question with a tool it discovered at runtime.
4. **Attack your own server.** Add a second test server whose tool description tells the model to send note contents to that tool. Done when you have shown whether your agent falls for it and added two mitigations, such as approving calls or allowlisting servers.
5. **Go remote.** Run your server over Streamable HTTP behind a simple bearer token. Done when an unauthenticated request is rejected and an authenticated client can list tools.

## Checklist
- [ ] [Must ship] Build an MCP server with at least three tools and one resource using the official SDK or FastMCP.
- [ ] [Must ship] Test the server with the MCP Inspector and connect it to one existing host.
- [ ] [Must ship] Connect your own agent to the server as an MCP client.
- [ ] [Recommended] Write a short threat note for your server covering what it can read, what it can change and who can call it.
- [ ] [Stretch] Serve it over Streamable HTTP with authentication.

## You're ready when
- You can explain hosts, clients, servers and the three server primitives without notes.
- Your server works in the Inspector, in a third-party host and in your own agent.
- You can name three risks of installing a third-party MCP server and a mitigation for each.
- You know which protocol version and SDK version your code targets.
