<div align="center">

# State-Aware Agentic AI Chatbot

**A modular, state-aware conversational AI platform built with LangGraph, LangChain and Streamlit**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)](./LICENSE)

</div>

---

## Overview

The **State-Aware Agentic AI Chatbot** is a production-ready, extensible AI agent framework that combines the graph-based orchestration of **LangGraph** with a **Streamlit** frontend. The architecture is built around a typed state machine — every message exchange flows through a compiled `StateGraph`, giving the agent full awareness of conversation history at every step.

The project is designed as a foundation for building increasingly complex agentic workflows. The current implementation ships a **Research Assistant** use case, but the graph-based architecture makes it straightforward to plug in tool-calling nodes, RAG pipelines, multi-agent subgraphs, or any custom workflow.

### Key Highlights

- **State-aware by design** — conversation history is tracked via LangGraph's `add_messages` reducer, not session variables
- **Config-driven UI** — all UI options (LLM providers, models, use cases) are controlled from a single `.ini` file with no code changes needed to add options
- **Separation of concerns** — LLM wiring, graph logic, state schema, and UI rendering are each isolated in their own module
- **Groq-powered inference** — uses Groq's ultra-fast inference API with Llama 3.x models for near-instant responses

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Orchestration** | [LangGraph](https://langchain-ai.github.io/langgraph/) | Stateful graph execution engine for agentic workflows |
| **LLM Framework** | [LangChain](https://www.langchain.com/) | Abstractions for LLMs, messages, and chains |
| **LLM Provider** | [Groq](https://groq.com/) + `langchain_groq` | Fast inference for Llama 3.1 / 3.3 models |
| **Frontend** | [Streamlit](https://streamlit.io/) | Chat UI and sidebar controls |
| **State Schema** | `TypedDict` + `Annotated` | Typed, append-only message state |
| **Config** | `configparser` (.ini) | Declarative UI configuration |
| **Language** | Python 3.10+ | Core runtime |

---

## Project Structure

```
State-aware-bot/
│
├── app.py                                      # Application entry point
├── requirements.txt                            # Python dependencies
├── LICENSE                                     # Apache 2.0 license
│
└── src/
    └── langgraph_agentic_ai/
        │
        ├── main.py                             # App orchestrator — wires UI, LLM, graph, and output
        │
        ├── state/
        │   └── state.py                        # LangGraph state schema (typed message list)
        │
        ├── llms/
        │   └── groqllm.py                      # Groq LLM factory — reads API key and model from UI input
        │
        ├── nodes/
        │   └── basic_chatbot_node.py           # Graph node — invokes the LLM with current state
        │
        ├── graph/
        │   └── graph_builder.py                # Builds and compiles the StateGraph for each use case
        │
        └── ui/
            ├── UI_config.ini                   # Declarative config: page title, LLM/model/usecase options
            ├── UI_config.py                    # Config reader — parses .ini and exposes typed getters
            └── streamlit/
                ├── loadUI.py                   # Renders sidebar controls and returns user selections
                └── display_out.py              # Streams graph output into the Streamlit chat interface
```

---

## File Reference

### `app.py`
The top-level entry point. Imports and calls `load_langgraph_agenticai_app()` from `main.py`. Run this file to start the application.

### `src/langgraph_agentic_ai/main.py`
The central orchestrator. Initializes the Streamlit UI, captures user selections and chat input, instantiates the LLM, builds the graph for the selected use case, and delegates output rendering. All the wiring between components happens here.

### `src/langgraph_agentic_ai/state/state.py`
Defines `State`, the typed dictionary that flows through every node in the LangGraph. The `messages` field uses the `add_messages` reducer so incoming messages are appended rather than overwritten — this is what makes the bot "state-aware" across turns.

### `src/langgraph_agentic_ai/llms/groqllm.py`
The `GroqLLM` factory class. Reads the selected model name and API key from the UI controls dict, validates the key, and returns a configured `ChatGroq` instance ready to be passed into a graph node.

### `src/langgraph_agentic_ai/nodes/basic_chatbot_node.py`
The `BasicChatbotNode` class. Implements a single graph node that invokes the LLM with the current message state and returns the response. This is the building block for more complex multi-node graphs.

### `src/langgraph_agentic_ai/graph/graph_builder.py`
The `GraphBuilder` class compiles a `StateGraph` for a given use case. It wires nodes to `START` and `END` edges and returns a compiled graph ready for `.stream()` or `.invoke()`. Adding a new use case means adding a new build method here.

### `src/langgraph_agentic_ai/ui/UI_config.ini`
The single source of truth for all UI configuration. Controls the page title, available LLM providers, selectable Groq models, and supported use cases — all without touching Python code.

### `src/langgraph_agentic_ai/ui/UI_config.py`
The `Config` class wraps `configparser` and exposes typed getters (`get_llm_options()`, `get_groq_model_options()`, etc.). Validates that required keys exist on load and raises descriptive errors if they are missing.

### `src/langgraph_agentic_ai/ui/streamlit/loadUI.py`
The `LoadStreamlitUI` class sets the Streamlit page config and renders the sidebar: LLM selector, model selector, API key input, and use case selector. Returns a dictionary of user selections consumed by `main.py`.

### `src/langgraph_agentic_ai/ui/streamlit/display_out.py`
The `DisplayOutStreamlit` class handles streaming graph output to the Streamlit chat interface. It renders the user's message and streams the assistant's response as the graph emits events.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com/) (free tier available)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd State-aware-bot

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

### Configuration

1. Open the sidebar in the Streamlit UI
2. Select **Groq** as the LLM provider
3. Choose a model (`llama-3.1-8b-instant` for speed, `llama-3.3-70b-versatile` for quality)
4. Paste your **Groq API key**
5. Select the **Research Assistant** use case
6. Start chatting

---

## Extending the Project

### Adding a new use case

1. Add the use case name to `USECASE_OPTIONS` in `UI_config.ini`
2. Create a new build method in `GraphBuilder` (e.g., `rag_chatbot_build_graph()`)
3. Add a branch in `GraphBuilder.setup_graph()` for the new use case
4. Add a rendering branch in `DisplayOutStreamlit.display_result_on_ui()`

### Adding a new LLM provider

1. Add the provider name to `LLM_OPTIONS` in `UI_config.ini`
2. Create a new factory class in `src/langgraph_agentic_ai/llms/` (mirroring `groqllm.py`)
3. Add a selection branch in `main.py` to instantiate the new factory

---

## License

Distributed under the [Apache License 2.0](./LICENSE).
