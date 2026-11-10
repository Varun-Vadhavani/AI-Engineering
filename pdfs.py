import base64
import time
import pymupdf
import requests
from llm import API_KEY

LINES = """INVOICE
Invoice No: INV-2026-0417
Date: 12 October 2026
Customer: Meridian Traders Pvt Ltd
Item: Industrial sensors x 40 @ 1,150
Item: Installation service x 1 @ 2,250
Total due: 48,250 INR
Payment terms: Net 30"""

# 1. Digital PDF: real text inside
doc = pymupdf.open()
page = doc.new_page()
page.insert_text((72, 90), LINES, fontsize=12)
doc.save("digital.pdf")

# 2. "Scanned" PDF: render the page to a picture, then wrap the picture in a new PDF
pix = pymupdf.open("digital.pdf")[0].get_pixmap(dpi=150)
scan = pymupdf.open()
p = scan.new_page(width=page.rect.width, height=page.rect.height)
p.insert_image(p.rect, pixmap=pix)
scan.save("scanned.pdf")

# What can a parser extract from each?
for name in ["digital.pdf", "scanned.pdf"]:
    with pymupdf.open(name) as pdf:
        text = "\n".join(pdf_page.get_text() for pdf_page in pdf).strip()
    print(f"{name}: extracted {len(text)} characters of text")


def pdf_image_blocks(path: str) -> list[dict[str, object]]:
    with pymupdf.open(path) as pdf:
        if not pdf:
            raise ValueError(f"{path} contains no pages.")
        if len(pdf) > 3:
            raise ValueError(
                f"{path} has {len(pdf)} pages; Groq accepts at most 3 images "
                "per request. Split the PDF into smaller batches."
            )
        blocks = []
        for pdf_page in pdf:
            image_data = pdf_page.get_pixmap(dpi=150, alpha=False).tobytes("png")
            image_b64 = base64.b64encode(image_data).decode("ascii")
            blocks.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_b64}",
                },
            })
    return blocks

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def run(content: list[dict[str, object]], question: str) -> tuple[str, int]:
    body = {
        "model": "qwen/qwen3.8-27b",
        "max_completion_tokens": 100,
        "messages": [{"role": "user", "content": content + [{"type": "text", "text": question}]}],
    }
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=HEADERS,
        json=body,
        timeout=60,
    )
    r.raise_for_status()
    d = r.json()
    return d["choices"][0]["message"]["content"].strip(), d["usage"]["prompt_tokens"]


question = "What is the total due and the invoice number? Answer briefly."
with pymupdf.open("digital.pdf") as pdf:
    plain_text = "\n".join(pdf_page.get_text() for pdf_page in pdf).strip()

print()
for index, (label, content) in enumerate([
    ("digital PDF image", pdf_image_blocks("digital.pdf")),
    ("scanned PDF image", pdf_image_blocks("scanned.pdf")),
    ("plain text ", [{"type": "text", "text": plain_text}]),
]):
    answer, tokens = run(content, question)
    print(f"{label} | in={tokens:>5} | {answer}")
    if index < 2:
        time.sleep(20)