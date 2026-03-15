# Maven Indexer MCP

- GitHub: [tangcent/maven-indexer-mcp](https://github.com/tangcent/maven-indexer-mcp)

Maven Indexer MCP indexes your local Maven/Gradle caches and provides tools to search for classes, artifacts, resources, and implementations within internal company libraries. It's especially useful for navigating large Java/Kotlin codebases that depend on internal packages.

## Key Features

- Search for classes by fully qualified name, partial name, or keyword
- Retrieve source code or signatures from cached JARs (with decompilation fallback)
- Search artifacts by coordinate, keyword, or class name
- Find implementations of interfaces or base classes
- Search for resources (XML configs, proto files, etc.) inside JARs

## Tools

| Tool | Description |
|------|-------------|
| `search_classes` | Find classes in local Maven/Gradle caches |
| `get_class_details` | Get source code, signatures, or docs for a class |
| `search_artifacts` | Search artifacts by coordinate or keyword |
| `search_implementations` | Find implementations of an interface or base class |
| `search_resources` | Search non-class files inside JARs |
| `refresh_index` | Re-scan and re-index the Maven repository |

## Sample Config

```json
{
  "mcpServers": {
    "maven-indexer": {
      "command": "npx",
      "args": ["-y", "maven-indexer-mcp@latest"],
      "autoApprove": [
        "search_classes",
        "get_class_details",
        "search_artifacts",
        "refresh_index"
      ],
      "disabled": false
    }
  }
}
```
