# Mission Control: Google ADK learning campaign

Created: 2026-11-01. Owner: the user of this project.

## Goal

Learn Google ADK deeply by building one useful multi-agent research application. Each topic unlocks a working project capability. Learn enough of the runtime and source code to explain how the application behaves, rather than only assembling prompts.

Example mission:

> Compare three open-source agent frameworks for my project. Research their official documentation, inspect my requirements, identify tradeoffs, and produce a recommendation with sources.

The final system plans a mission; delegates to web, document, and technical researchers; joins evidence; drafts a report; critiques unsupported claims; performs bounded revisions; pauses for human approval; saves versioned artifacts; recalls relevant past work; and exposes inspectable execution telemetry.

## Baseline and campaign rules

- Language assumption: Python, basic APIs, and introductory async programming. Learn missing prerequisites just in time.
- Reference baseline researched on 2026-11-01: ADK Python 2.13.0. Pin the version used by the project. Verify APIs against that version rather than assuming all tutorials apply.
- Suggested pace: 8–10 weeks, approximately 60–90 hours; an estimate, not a deadline.
- 16 quests × 100 XP plus four bosses × 200 XP = 2,400 XP.
- Each quest requires relevant reading, a working feature, and evidence for its acceptance challenge. Make a small commit and record a short explanation when practical. A commit alone is not proof of completion.
- Inspect events/tool calls as well as final answers. Do not add the entire team before its quests.
- Track progress and evidence in `PROGRESS.md`. Review behavior is specified in `AGENTS.md`.

## Architecture to grow toward

User mission → planner → parallel web/document/technical researchers → join evidence → writer → critic.

The critic either requests targeted research/revision within a configured limit or passes the report to human approval. Approval saves a versioned report artifact; revision returns to the writer. Session storage, memory, artifacts, and telemetry support this process.

## Act I — Bring your first agent to life

### Quest 1 — Recruit your first operative — 100 XP

Learn: `Agent`/`LlmAgent`, model selection, instructions, descriptions, tools, and `root_agent`.

Build: One research assistant that converts a vague question into a research brief. Run it through the CLI and development web interface.

Acceptance: Handle three distinct missions and ask for missing requirements when necessary. Show actual runs and explain which behavior your instructions provide and which behavior ADK provides.

First demo prompt: "Turn my rough project idea into a research brief with objectives, constraints, and unanswered questions."

Read: [Python quickstart](https://adk.dev/get-started/python/), [Simple agents](https://adk.dev/agents/llm-agents/).

### Quest 2 — Give it equipment — 100 XP

Learn: Function tools, type annotations, docstrings, argument schemas, async execution, tool results, and failure handling.

Build: Tools such as `read_requirements()`, `fetch_document()`, and `calculate_score()`. Use local sample data before external integrations.

Acceptance: Demonstrate a successful tool call, invalid input, and an unavailable resource. Explain how each outcome reaches the agent and why deterministic tasks such as arithmetic or parsing belong in code.

Read: [Function tools](https://adk.dev/tools-custom/function-tools/).

### Quest 3 — Build the control room: runners and events — 100 XP

Learn: `Runner`, `InMemoryRunner`, `run_async()`, `RunConfig`, `Event`, `EventActions`, invocation IDs, and final versus intermediate responses.

Build: A terminal interface showing which component acted, which tool ran, and when the final response arrived.

Acceptance: Trace one request from user message through tool execution to final response. Explain the runner's processing of events and its connection to configured services. One invocation can include several agents, model calls, and tool executions.

Read: [Runtime event loop](https://adk.dev/runtime/event-loop/).

### Quest 4 — Give the mission a working memory — 100 XP

Learn: `Session`, `SessionService`, `Context`, state changes, persistence, and scoped keys.

Build: A mission that remembers its objective, audience, constraints, and status across turns.

Suggested keys:

| Key | Scope |
| --- | --- |
| `mission_brief` | Current session |
| `user:report_style` | User across their sessions |
| `app:report_template_version` | Shared application setting |
| `temp:retrieval_scratch` | Current invocation |

Acceptance: Demonstrate expected behavior for two users and two sessions; temporary data must not survive the invocation. Explain that surviving a process restart depends on the session service.

Read: [Sessions](https://adk.dev/sessions/session/), [State](https://adk.dev/sessions/state/).

### Boss 1 — The forgetful assistant — 200 XP

After Quests 1–4, complete a three-turn research conversation, restart using persistent session storage, and continue it. Demonstrate that another user's preferences remain separate.

Rank at 600 XP: Agent Apprentice.

## Act II — Assemble the team

### Quest 5 — Create a dependable assembly line — 100 XP

Learn: `SequentialAgent`, `output_key`, input/output schemas, and typed handoffs.

Build: Planner → Researcher → Writer.

Suggested contracts:

- `ResearchPlan`: questions and completion criteria.
- `EvidenceItem`: claim, source, supporting passage, and retrieval time.
- `ResearchReport`: findings, limitations, and references.

Acceptance: Each stage consumes its predecessor's output, and malformed output is detected. Explain the difference between state-based handoffs and graph node outputs. Check the selected model's support for combining tools with output schemas.

Read: [Template workflows](https://adk.dev/agents/workflow-agents/), [Workflow data handling](https://adk.dev/graphs/data-handling/).

### Quest 6 — Research on multiple fronts — 100 XP

Learn: `ParallelAgent`, `Workflow`, nodes, edges, fan-out, and `JoinNode`.

Build: Concurrent web, document, and technical researchers followed by an evidence merger.

Acceptance: The merger waits for every required result. Branches have separate output keys or an explicit safe merge design. Measure sequential and parallel execution on the same mission and explain latency versus total work.

Read: [Graph workflows](https://adk.dev/graphs/), [Graph routes and joins](https://adk.dev/graphs/routes/).

### Quest 7 — Promote a coordinator — 100 XP

Learn: `sub_agents`, descriptions, routing, delegation, and collaboration modes (`chat`, `task`, `single_turn`). Verify supported combinations in the pinned version.

Build: A coordinator that selects specialists according to the mission; document-only work should go to the document specialist.

Acceptance: A small routing dataset demonstrates appropriate delegation, including a request needing several specialists. Compare a fixed graph with model-directed delegation. Inspect what each specialist receives and what returns to the coordinator.

Read: [Agent routing](https://adk.dev/agents/routing/), [Collaborative teams](https://adk.dev/workflows/collaboration/).

### Quest 8 — Hire a skeptical critic — 100 XP

Learn: `LoopAgent`, conditional routes, dynamic workflows, `@node`, `ctx.run_node()`, and stopping conditions.

Build: A critic that identifies unsupported claims, requests targeted revisions, and triggers additional research.

Acceptance: A planted unsupported claim causes revision. Repeated failure stops after a configured limit with an honest limitations statement. Compare an implementation using a template workflow with one using graph or dynamic orchestration.

Read: [Template workflows](https://adk.dev/agents/workflow-agents/), [Dynamic workflows](https://adk.dev/graphs/dynamic/).

### Boss 2 — Conflicting intelligence — 200 XP

After Quests 5–8, provide contradictory sources and one failing research tool. Preserve the disagreement, identify missing evidence, and terminate within configured limits.

Rank at 1,200 XP: Squad Leader.

## Act III — Master context and continuity

### Quest 9 — Open the evidence vault — 100 XP

Learn: `ArtifactService`, save/load operations, versions, filenames, and artifact references.

Build: Stored source documents, evidence collections, and report versions users can reopen. Add a retrieval tool returning relevant passages and source identifiers.

Acceptance: Generate two report versions and explicitly retrieve the earlier one. Explain why file/artifact storage alone is not a document retrieval or RAG pipeline.

Read: [Artifacts](https://adk.dev/artifacts/).

### Quest 10 — Remember previous missions — 100 XP

Learn: `MemoryService`, explicit memory ingestion, search, `load_memory`, and `preload_memory`.

Build: A new mission recalls relevant prior decisions or lessons.

Acceptance: A fresh session retrieves a relevant prior decision; an unrelated request does not indiscriminately receive all past content. Compare a fixed preference in `user:` state with searchable past experience. Demonstrate ingestion as well as retrieval.

Read: [Memory](https://adk.dev/sessions/memory/).

### Quest 11 — Become a context engineer — 100 XP

Learn: Instruction providers, history inclusion, `include_contents`, branch isolation, compaction, and model context caching.

Build: Focused specialist briefs and selected evidence, with manageable context on long missions.

Acceptance: Inspect an actual model request and identify the origin of each major piece of information. Compare a long mission before and after compaction, measuring tokens and retained facts. Explain why caching, compaction, and memory retrieval serve different purposes.

Read: [Context](https://adk.dev/context/), [Compaction](https://adk.dev/context/compaction/), [Caching](https://adk.dev/context/caching/).

### Quest 12 — Put yourself in command — 100 XP

Learn: `RequestInput`, human input nodes, action confirmations, resumability, invocation IDs, replay behavior, and idempotency.

Build: Clarification and approval pauses that continue after a response.

Acceptance: Pause, restart with suitable persistence, and resume without repeating a completed external action. Give actions idempotency keys and explain which nodes rerun versus restore completed results.

Read: [Human input](https://adk.dev/graphs/human-input/), [Resume](https://adk.dev/runtime/resume/).

### Boss 3 — The interrupted investigation — 200 XP

After Quests 9–12, run a long mission, pause for approval, restart, and resume. Retain the objective, retrieve the correct evidence, and produce exactly one approved report.

Rank at 1,800 XP: Context Engineer.

## Act IV — Make it trustworthy and usable

### Quest 13 — Install flight instruments — 100 XP

Learn: Agent/model/tool callbacks, `BasePlugin`, logging, traces, timeouts, retries, and `RunConfig.max_llm_calls`.

Build: A mission timeline with latency, model-call counts, failures, and execution limits.

Acceptance: Deliberately trigger a tool failure and a runaway revision cycle. Both leave understandable traces and stop predictably. Explain local callbacks versus shared instrumentation/policies in plugins.

Read: [Callbacks](https://adk.dev/callbacks/), [Plugins](https://adk.dev/plugins/), [Runtime configuration](https://adk.dev/runtime/runconfig/).

### Quest 14 — Connect a real workspace — 100 XP

Learn: `McpToolset`, tool filtering, connection lifecycle, authentication, and OpenAPI tools as an alternative.

Build: A researcher connected to a selected document collection or another useful external service.

Acceptance: Demonstrate successful access and unavailable access. Expose only tools required for the role. Explain how the connection and credentials differ from those for an ordinary function tool.

Read: [MCP tools](https://adk.dev/tools-custom/mcp-tools/). Use the Authentication guide linked from that documentation and verify the current SDK's APIs.

### Quest 15 — Enter the evaluation arena — 100 XP

Learn: Evaluation datasets, response assessment, tool trajectories, rubrics, and regression checks.

Build: A repeatable research-team scorecard.

Acceptance: Include normal research, ambiguity, conflicting evidence, missing sources, tool failures, and misleading instructions embedded in retrieved content. Deliberately introduce a regression, detect it, and recover. Assess evidence quality as well as tool calls.

Read: [Evaluation](https://adk.dev/evaluate/).

### Quest 16 — Launch Mission Control — 100 XP

Learn: `App`, API serving, streaming responses, deployment, persistent services, configuration, and observability.

Build: An interface to submit missions, watch progress, approve reports, and retrieve them later.

Acceptance: A second person completes a mission without help. Diagnose a failed run through recorded telemetry. Explain the boundaries among agent definitions, App configuration, execution infrastructure, and storage.

Read: [App management](https://adk.dev/apps/), [Cloud Run](https://adk.dev/deploy/cloud-run/), [Observability](https://adk.dev/observability/).

### Boss 4 — The adversarial research mission — 200 XP

After Quests 13–16, combine contradictory sources, a tool outage, irrelevant remembered information, an instruction hidden in a document, and a restart during approval.

Acceptance:

- Support material claims with evidence or explicitly mark them unresolved.
- Keep retrieved document instructions from controlling actions.
- Preserve user and session boundaries.
- Stop within configured limits.
- Resume without duplicate actions.
- Produce a versioned report and an inspectable execution trace.

These are acceptance targets to implement and test, not automatic framework guarantees.

Rank at 2,400 XP: Systems Architect.

## Abstraction map

Distinguish information available to the runtime from information included in one model request.

| Abstraction | Responsibility |
| --- | --- |
| App | Packages the root agent and application-wide configuration |
| Runner | Executes invocations, connects services, processes events, and returns results |
| Session | Records a conversation's state and events |
| Invocation | One execution triggered by an incoming request |
| InvocationContext | Carries invocation runtime information and service references |
| Context | Access to runtime capabilities from tools, callbacks, and workflow nodes |
| State | Named working values with explicit scopes and persistence rules |
| Node output | Result passed to downstream workflow nodes |
| Model context | Instructions, selected history, input, and other content sent to a model |
| Memory | Retrieval of relevant information from previous interactions |
| Artifacts | Files and generated outputs, with versioning |
| Event / EventActions | Execution records, outputs, and tracked actions such as state deltas |

Current Python documentation unifies interfaces older examples call `CallbackContext` or `ToolContext` under `Context`; verify exact behavior in the installed version.

Project design rule: every important piece of information needs an owner, storage location, lifetime, and reason to enter the model prompt.

## Source-code mastery challenge

After Quests 3, 4, and 11, follow a tool-using request through the pinned implementation. Explain where the invocation starts, where the model request is assembled, how the tool gets context, and when state changes are persisted.

Historical reference source links (replace with the project's pinned version if different):

- [Runner](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/runners.py)
- [Context](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/agents/context.py)
- [Event](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/events/event.py)

## Optional expansion packs

These do not block the main campaign and award no core XP.

| Topic | Upgrade | Reference |
| --- | --- | --- |
| A2A / RemoteA2aAgent | Specialist as an independent service | [A2A](https://adk.dev/a2a/intro/) |
| Live audio | Speak with the research team | [Live agents](https://adk.dev/live/) |
| Agent skills | Reusable research procedures | [Skills](https://adk.dev/skills/) |
| Search grounding | Web-grounded research and source metadata | [Search grounding](https://adk.dev/grounding/google_search_grounding/) |
| Alternate models | Compare specialist quality, latency, and cost | Start from Models for Agents in the [official documentation](https://adk.dev/) |

Runnable reference patterns: [Google ADK Recipes](https://github.com/google/adk-recipes). Check each recipe's version and prerequisites.

## Change log

- 2026-11-01: Persisted the agreed 16-quest roadmap and four bosses from the project chat. Added explicit project review and evidence tracking conventions without changing the learning objective.
- 2026-11-01: Added a Git and GitHub side campaign in `GIT_ROADMAP.md`, paired with the acts above. The ADK campaign, quests and XP are unchanged.
