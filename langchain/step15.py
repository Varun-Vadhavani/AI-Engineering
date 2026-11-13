import json
import time
from models import get_model

model = get_model()
FAIL_AFTER = None   # set to e.g. 5 to simulate a dropped connection after 5 chunks

def stream_and_save(question, path="last_answer.json"):
    pieces, status, last_meta = [], "complete", {}
    try:
        for i, chunk in enumerate(model.stream(question)):
            if FAIL_AFTER is not None and i == FAIL_AFTER:
                raise ConnectionError("simulated dropped connection")
            print(chunk.content, end="", flush=True)
            pieces.append(chunk.content)
            if chunk.response_metadata:
                last_meta = chunk.response_metadata
    except KeyboardInterrupt:
        status = "cancelled"
    except Exception as e:
        status = f"error: {e}"
    finally:
        reason = last_meta.get("finish_reason") or last_meta.get("done_reason")
        if status == "complete" and reason not in ("STOP", "stop"):
            status = f"incomplete (stop reason: {reason})"
        record = {
            "question": question,
            "text": "".join(pieces),
            "status": status,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        print(f"\n[{status}] saved {len(record['text'])} characters")
    return record

stream_and_save("Write a detailed 400-word explanation of how the internet works.")