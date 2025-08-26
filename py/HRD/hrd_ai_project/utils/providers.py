
import os, httpx, json
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field
from openai import OpenAI  # OpenAI 공식 SDK
from google import genai     # Gemini 공식 SDK (google-genai)  :contentReference[oaicite:2]{index=2}

Role = Literal["system","user","assistant"]

class Msg(BaseModel):
    role: Role
    content: str

class ProviderResponse(BaseModel):
    text: str
    raw: Dict[str, Any]

# ---------- OpenAI ----------
class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def chat(self, messages: List[Msg], **kwargs) -> ProviderResponse:
        # Responses API도 가능하지만, 여기선 호환 쉬운 chat.completions 스타일 예시
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump() for m in messages],
            temperature=kwargs.get("temperature", 0.3),
            response_format=kwargs.get("response_format")  # {"type": "json_object"} 등
        )
        text = resp.choices[0].message.content
        return ProviderResponse(text=text, raw=resp.model_dump())

# ---------- Perplexity ----------
class PerplexityClient:
    """
    Perplexity Sonar API는 OpenAI Chat Completions 포맷 호환.
    엔드포인트: https://api.perplexity.ai/chat/completions :contentReference[oaicite:3]{index=3}
    """
    def __init__(self, model: str = "sonar-pro"):
        self.model = model
        self.key = os.getenv("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")
        self.base_url = "https://api.perplexity.ai"

    def chat(self, messages: List[Msg], **kwargs) -> ProviderResponse:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "temperature": kwargs.get("temperature", 0.2),
        }
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        with httpx.Client(timeout=60) as client:
            r = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return ProviderResponse(text=text, raw=data)

# ---------- Gemini ----------
class GeminiClient:
    """
    google-genai SDK 사용. 기본 예시는 models.generate_content 호출. :contentReference[oaicite:4]{index=4}
    """
    def __init__(self, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = model

    def chat(self, messages: List[Msg], **kwargs) -> ProviderResponse:
        # system/user를 하나의 prompt로 병합 (Gemini는 role-less 텍스트도 잘 처리)
        sys = "\n".join([m.content for m in messages if m.role == "system"])
        convo = "\n\n".join([f"{m.role.upper()}: {m.content}" for m in messages if m.role != "system"])
        prompt = (sys + "\n\n" + convo).strip()
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"temperature": kwargs.get("temperature", 0.3)}
        )
        # 최신 SDK는 response.text 제공
        return ProviderResponse(text=resp.text, raw=resp.to_dict())
