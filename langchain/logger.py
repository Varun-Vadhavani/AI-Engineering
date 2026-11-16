import time
from langchain_core.callbacks import BaseCallbackHandler

class CallLogger(BaseCallbackHandler):
    def __init__(self):
        self.calls = []       # one dict per finished or failed model call
        self._open = {}       # model calls currently running

    def on_chat_model_start(self, serialized, messages, *, run_id, tags=None, metadata=None, **kwargs):
        step = next((t.split(":", 1)[1] for t in (tags or []) if t.startswith("step:")), "unnamed")
        self._open[run_id] = {
            "t0": time.perf_counter(),
            "q": (metadata or {}).get("q"),
            "step": step,
        }

    def on_llm_end(self, response, *, run_id, **kwargs):
        info = self._open.pop(run_id, None)
        if info is None:
            return
        msg = getattr(response.generations[0][0], "message", None)
        usage = (getattr(msg, "usage_metadata", None) or {})
        meta = (getattr(msg, "response_metadata", None) or {})
        self.calls.append({
            "q": info["q"], "step": info["step"],
            "model": meta.get("model_name") or meta.get("model") or "unknown",
            "in_tokens": usage.get("input_tokens", 0),
            "out_tokens": usage.get("output_tokens", 0),
            "secs": round(time.perf_counter() - info["t0"], 2),
            "error": None,
        })

    def on_llm_error(self, error, *, run_id, **kwargs):
        info = self._open.pop(run_id, None)
        if info is None:
            return
        self.calls.append({
            "q": info["q"], "step": info["step"], "model": "unknown",
            "in_tokens": 0, "out_tokens": 0,
            "secs": round(time.perf_counter() - info["t0"], 2),
            "error": f"{type(error).__name__}: {str(error)[:120]}",
        })