# LangChain Level 2: Hands-On Learning Project

A step-by-step project built while learning LangChain from scratch. Every `stepNN.py` file is one small experiment, and each one builds on the previous ones. The project runs on a **free model** (Google Gemini free tier) and a **local open model** (Ollama), with a one-line switch between them.

## What's covered

| Unit | Topic |
|---|---|
| 2.1 | LangChain basics and conversations |
| 2.2 | Open and local models |
| 2.3 | Streaming |
| 2.4 | Structured outputs |
| 2.5 | Tool calling |
| 2.6 | Chaining steps together |
| 2.7 | Handling failures |
| 2.8 | Processing at scale |
| 2.9 | Cost, logging and tracing |

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (never commit it; see `.env.example`):

```
GOOGLE_API_KEY=your-key-here
MODEL_MODE=local                  # local (Ollama) or gemini
```

For local mode, install [Ollama](https://ollama.com) and pull the model used here:

```bash
ollama pull qwen2.5-coder:7b
```

Run any script, and pick the model with `MODEL_MODE`:

```bash
python step1.py                                  # uses MODEL_MODE from .env
MODEL_MODE=gemini python step24.py               # Mac/Linux
$env:MODEL_MODE="gemini"; python step24.py       # Windows PowerShell
```

> Note: the local `qwen2.5-coder:7b` model does not make real tool calls, so the Unit 2.5 scripts (and anything using tools) should be run in `gemini` mode.

---

## Unit 2.1: LangChain basics and conversations

| File | What it covers |
|---|---|
| `step1.py` | First model call: load the API key from `.env`, create a chat model, call `.invoke()`, print `.content`. |
| `step2.py` | Look inside the response object: `AIMessage`, `usage_metadata` (token counts) and `response_metadata` (finish reason). |
| `step3.py` | Messages and roles: `SystemMessage` and `HumanMessage` in a list, and how a system message changes behaviour. |
| `step4.py` | The model has no memory: a manual chat history list sent on every call, and a comparison with the history dropped. |
| `step5.py` | Prompt templates with `{placeholders}`, how a filled template becomes a message list, and joining a prompt and a model with `\|`. |
| `step6.py` | Template plus history using `MessagesPlaceholder`: the three-turn conversation, then the third call without history. |
| `step7.py` | Reading the whole response: finish reason and token usage, including a forced cut-off with a tiny output limit. |

## Unit 2.2: Open and local models

| File | What it covers |
|---|---|
| `step8.py` | Calling a local Ollama model with `ChatOllama`, with timing, and no API key needed. |
| `step9.py` | Same code, different model: the template and history conversation from `step6.py` with only the model line swapped. |
| `compare.py` | Benchmark: the same 10 questions sent to Gemini and the local model, with timing, saved to `results.md`. |
| `models.py` | `get_model()`: one place that picks the model from the `MODEL_MODE` setting, used by every later script. |
| `step10.py` | Using `get_model()` so the app code never mentions a provider. |
| `VERDICT.md` | Written conclusion on when a local model is good enough. |

## Unit 2.3: Streaming

| File | What it covers |
|---|---|
| `step11.py` | `.stream()` and what individual chunks look like. |
| `step12.py` | Printing chunks live with `end=""` and `flush=True` so text appears as it arrives. |
| `step13.py` | Time to first token: `.invoke()` versus `.stream()` on a long answer. |
| `step14.py` | Reassembling chunks into a full answer, both with `"".join(...)` and by adding chunks together (keeps the metadata). |
| `step15.py` | When streams break: handling a user cancelling, a dropped connection and an answer that stops early, always saving partial text with a status in `last_answer.json`. |
| `step16.py` | Streaming a whole chain (`prompt \| model \| StrOutputParser()`). |

## Unit 2.4: Structured outputs

| File | What it covers |
|---|---|
| `step17.py` | Why "just ask for JSON" is unreliable: repeated attempts and parse failures. |
| `step18.py` | Pydantic schema plus `with_structured_output()`, which returns a typed `Receipt` object. |
| `schemas.py` | The shared `Receipt` schema with field descriptions, allowed category values and validators (real date, not in the future, positive amount). |
| `step19.py` | Validation without any model: invalid data rejected, and a valid-but-wrong example that passes every rule. |
| `step20.py` | Experiment: 10 messy receipts with expected answers, counting valid-and-correct, valid-but-wrong and invalid. |
| `step21.py` | Generate, check, decide: a repair loop that feeds the validation error back, with a retry cap and a clear rejection error. |

## Unit 2.5: Tool calling

| File | What it covers |
|---|---|
| `tools.py` | Tools defined with `@tool`: `get_weather` and `convert_currency` (fake data), where the docstring is the instruction the model reads. |
| `step22.py` | Inspecting a tool's name, description and input schema, and running it by hand. |
| `step23.py` | `bind_tools()` and reading `tool_calls`: the model asks for a tool and nothing runs yet. Includes a question needing no tool. |
| `step24.py` | The full loop: the model asks, the code runs the tool, a `ToolMessage` with the matching `tool_call_id` goes back, and the model answers. |
| `agent_loop.py` | A sturdier loop: repeated rounds for chained calls, a `MAX_STEPS` cap, errors returned to the model as text, and an approval step for dangerous tools. |
| `step25.py` | Tool failures: unknown tool, wrong argument name, wrong type and a crashing tool; plus a same-tool-twice question and a chained question. |
| `step26.py` | Never trust tool inputs: `delete_expense` with input validation and human approval before anything is deleted. |

## Unit 2.6: Chaining steps together

| File | What it covers |
|---|---|
| `step27.py` | A fixed sequence: a points chain feeding a tweet chain, with a Python lambda reshaping the data between them. |
| `step28.py` | Routing: classify a question, clean the label in code, then send it to a different prompt per type. |
| `step29.py` | Parallel steps with `RunnableParallel`, combined into one study card, with sequential versus parallel timing. |

## Unit 2.7: Handling failures

| File | What it covers |
|---|---|
| `step30.py` | Provoking failures on purpose (wrong model, wrong key, tiny timeout, unreachable local server) and inspecting their error types and codes. |
| `errors.py` | `is_temporary()`: the rule for which errors are worth retrying and which should fail immediately. |
| `step31.py` | Hand-written retry with a cap, exponential backoff and jitter. |
| `step32.py` | LangChain's `.with_retry()` and `.with_fallbacks()`, with a local backup model for a failing primary. |
| `step33.py` | Limiting concurrency with `max_concurrency`, shown with a counter of how many calls run at once. |
| `step34.py` | Failing gracefully: short friendly messages for the user, real errors written to `errors.log`, and early rejection of too-long input. |

## Unit 2.8: Processing at scale

| File | What it covers |
|---|---|
| `make_texts.py` | Generates the 200 short sample texts in `texts.json`, so every run uses the same input. |
| `step35.py` | Summarizing texts one at a time versus concurrently with `.batch()` and a concurrency cap, comparing time, errors and tokens. |
| `step36.py` | Estimating tokens, cost and time for a big job from a small measured sample, before running it. |
| `step37.py` | A resumable job: results saved after every chunk to `summaries.jsonl`, finished work skipped on restart, and only temporary failures retried in later rounds. |

## Unit 2.9: Cost, logging and tracing

| File | What it covers |
|---|---|
| `logger.py` | `CallLogger`, a LangChain callback handler that records model, tokens, time and errors for every model call. |
| `app.py` | A two-step app (classify, then answer) with each model call tagged by step. |
| `step38.py` | Runs 10 questions with the logger and prints a report: total tokens and cost, average time per question, the most expensive question, and a per-step breakdown. Raw log saved to `calls.jsonl`. |
| LangSmith (optional) | Hosted tracing, enabled by environment variables in `.env`, giving a visual trace tree for each question. |

## Generated files

These are created when the scripts run and are not committed (see `.gitignore`): `results.md`, `last_answer.json`, `errors.log`, `summaries.jsonl`, `calls.jsonl`.

## Key lessons

- The model has no memory: the app sends the history every time.
- Streaming makes an app feel faster without making it faster.
- Valid output is not the same as correct output: validate, then decide to retry, repair or reject.
- The model asks for tools; the code decides what actually runs.
- Chains give your code control of the steps; agents give the model control.
- Retry temporary failures with backoff and a cap, fail fast on permanent ones, and always show users a clear message.
- Estimate before big jobs, save progress as you go, and measure every call.