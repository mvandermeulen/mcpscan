# Introducing MCPScan: Security Scanner for Model Context Protocol Servers

Hey r/ModelContextProtocol! I'm excited to share a new open-source tool I've been working on that helps secure MCP server implementations.

## What is MCPScan?

MCPScan is a specialized security scanner that performs automated analysis of MCP servers. It combines multiple scanning approaches:

* **Static Analysis** - Uses Semgrep with custom rules for AI/ML contexts
* **Dependency Scanning** - Checks both Python and Node.js dependencies
* **MCP-Get Integration** - Automatically scans all listed MCP servers

## Key Features

* 🔒 Custom security rules for AI model context
* 🐳 Docker-based isolation for safe scanning
* 📊 Detailed vulnerability reporting
* 🤖 Automated scanning of MCP-Get servers
* 🔍 Detection of:
  * Dangerous code patterns
  * Local file access vulnerabilities 
  * Network security issues
  * Dependency vulnerabilities
  * And more...

## Try It Out

The project is open source and available at: [your-repo-link]

We welcome contributions and feedback from the MCP community!

---
*Built to help secure the Model Context Protocol ecosystem*
