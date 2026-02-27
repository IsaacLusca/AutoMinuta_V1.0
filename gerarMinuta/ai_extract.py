from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()


def _client() -> genai.Client:
    api_key = os.getenv("CHAVE_API") or ""
    return genai.Client(api_key=api_key)


def _clean_json_text(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


def extract_placeholders_from_pdf(file_obj, keys: list[str]) -> dict[str, object]:
    reader = PdfReader(file_obj)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    keys_json = ",\n".join(f'  \"{k}\": \"\"' for k in keys)
    prompt = (
        "Você é um assistente jurídico especialista em licitações portuárias.\n"
        "Analise o TEXTO abaixo e extraia valores para as chaves solicitadas.\n"
        "Se não encontrar a informação exata, deixe o valor em branco (string vazia).\n\n"
        "Responda ESTRITAMENTE em JSON, com exatamente estas chaves:\n"
        "{\n"
        f"{keys_json}\n"
        "}\n\n"
        "TEXTO:\n"
        f"{full_text}"
    )

    response = _client().models.generate_content(model="gemini-2.5-flash", contents=prompt)
    cleaned = _clean_json_text(response.text or "")
    data = json.loads(cleaned) if cleaned else {}

    if not isinstance(data, dict):
        return {}

    out: dict[str, object] = {}
    for k in keys:
        v = data.get(k, "")
        out[k] = v if v is not None else ""
    return out

