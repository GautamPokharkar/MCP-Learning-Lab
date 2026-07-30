# MCP Learning Lab

A collection of hands-on projects exploring the **Model Context Protocol (MCP)** by building practical MCP servers, clients, and real-world AI integrations.

## 📖 About

This repository documents my journey of learning MCP from the ground up. Rather than jumping directly into complex integrations, I start with a simple calculator server to understand the core concepts and then progressively build more advanced MCP projects.

The goal is to understand not only **how to build MCP servers**, but also **how AI assistants discover, invoke, and interact with tools**.

---

## 🚀 What I've Learned So Far

### MCP Fundamentals

* What the Model Context Protocol (MCP) is
* Why MCP exists
* How MCP standardizes AI-to-tool communication
* The difference between APIs and MCP
* Local vs. Remote MCP servers
* MCP Hosts, Clients, and Servers
* Transport mechanisms (`stdio`, HTTP)
* Using the MCP Inspector

### Built So Far

#### Calculator MCP Server

A simple MCP server exposing one tool:

* `add(a, b)`

This project demonstrates:

* Creating an MCP server
* Exposing tools using the MCP SDK
* Running a server over `stdio`
* Discovering tools
* Calling tools from an MCP client
* Testing with the MCP Inspector

---

## 🏗 Project Structure

```text
mcp-learning-lab/
│
├── 01-calculator/
│   ├── server.py
│   ├── client.py
│   └── requirements.txt
│
└── README.md
```

---

## 🧩 Architecture

```text
User
   │
   ▼
MCP Client / Inspector
   │
   ▼
Calculator MCP Server
   │
   ▼
add(a, b)
   │
   ▼
Result
```

---

## 🔍 Key Concepts Learned

### MCP Server

Exposes tools that AI applications can use.

Example:

* `add(a, b)`
* `search_files(query)`
* `find_customer(id)`

### MCP Client

Connects to an MCP server, discovers available tools, and invokes them.

### MCP Host

An AI application (such as Claude Desktop) that manages the LLM and communicates with one or more MCP servers.

### MCP Inspector

A visual testing client used during development to:

* Connect to an MCP server
* Discover tools
* Execute tool calls
* View results
* Debug MCP servers

---

## 🛠 Technologies

* Python
* MCP Python SDK
* AsyncIO
* MCP Inspector

---

## 📚 Learning Roadmap

* [x] Build a basic calculator MCP server
* [x] Build an MCP client
* [x] Test using the MCP Inspector
* [ ] Google Drive MCP Server
* [ ] SQLite / PostgreSQL MCP Server
* [ ] GitHub MCP Server
* [ ] Slack MCP Server
* [ ] Authentication (OAuth)
* [ ] Remote MCP Servers
* [ ] Claude Desktop integration with real-world tools

---

## 🎯 Goal

By the end of this repository, I aim to understand how to build production-style MCP servers that securely connect AI assistants to databases, APIs, cloud services, and internal tools through a standardized interface.
