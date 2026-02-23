import json
import time
import os
from typing import List, Optional, Dict
from pydantic import BaseModel
from openai import AsyncOpenAI
from App.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Knowledge Base (Professional BPO Context)
KB_PATH = os.path.join(os.path.dirname(__file__), "data", "knowledge.json")
with open(KB_PATH, "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

class AgentResponse(BaseModel):
    content: str
    latency: float
    transfer: bool = False

class CallCenterAgent:
    def __init__(self):
        self.customer_name: Optional[str] = None
        self.attempts: int = 0

    def detect_intent(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ["humano", "asesor", "persona", "hablar con", "traspaso"]): return "escalation"
        if any(w in msg for w in ["horario", "tiempo", "abre"]): return "schedule"
        if any(w in msg for w in ["servicio", "que hacen", "precio", "costo"]): return "services"
        if any(w in msg for w in ["norma", "politica", "garantia", "cancel"]): return "business_rules"
        return "unknown"

    def _extract_name(self, message: str):
        msg_lower = message.lower().strip()
        phrases = ["me llamo", "mi nombre es", "soy "]
        for phrase in phrases:
            if phrase in msg_lower:
                parts = message.split()
                for i, p in enumerate(parts):
                    if p.lower() in phrase.split() and i + 1 < len(parts):
                        self.customer_name = parts[i + 1].strip(".,!?")
                        return
        if len(message.split()) <= 2 and not any(k in msg_lower for k in ("hola", "donde", "que", "como")):
            self.customer_name = message.strip().split()[0]

    def _is_malicious(self, message: str) -> bool:
        bad = ["ignora", "ignore", "developer", "hacker", "system prompt", "revela", "prompt injection", "chiste", "joke", "receta"]
        return any(p in message.lower() for p in bad)

    async def generate_response(self, message: str, history: List[Dict] = None) -> AgentResponse:
        try:
            if self._is_malicious(message):
                return AgentResponse(content="Como asesor de **Connecta Solutions**, mi función es asistirle exclusivamente con servicios BPO corporativos. ✨", latency=0)

            intent = self.detect_intent(message)
            if intent == "escalation":
                return AgentResponse(content="Entiendo. He solicitado a un consultor experto que se una a la sesión. **Manténgase en línea.** ✨", latency=0, transfer=True)

            if not self.customer_name: self._extract_name(message)

            context_data = knowledge_base.get(intent, knowledge_base.get("faq", knowledge_base))
            
            # Ultra-compact System Prompt for Low Latency
            sys_p = (
                f"Eres Sir Connect, asesor élite de Connecta Solutions BPO. Orgulloso, ejecutivo y eficiente.\n"
                f"REGLA ORO: Solo responde sobre BPO/Connecta usando estos datos: {json.dumps(context_data)}\n"
                f"Si es ajeno, declina profesionalmente. Sé breve y resolutivo. Máximo 3 oraciones.\n"
            )
            if self.customer_name: sys_p += f"Dirígete al cliente como Sr/Sra {self.customer_name}."

            # History Management (Last 5 for speed)
            msgs = [{"role": "system", "content": sys_p}]
            for h in (history or [])[-5:]:
                role = "assistant" if h.get("role") == "agent" else "user"
                msgs.append({"role": role, "content": h.get("content", "")})
            msgs.append({"role": "user", "content": message})

            start = time.time()
            res = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=msgs,
                temperature=0.3,
                max_tokens=250 # Hard limit for speed
            )
            lat = round(time.time() - start, 3)
            content = res.choices[0].message.content.strip()

            if not content or any(f in content.lower() for f in ["ignora", "hack", "script"]):
                content = "Protocolo de seguridad activo. Solo temas corporativos de Connecta Solutions. ✨"

            return AgentResponse(content=content, latency=lat)

        except Exception as e:
            print(f"ASYNC AGENT ERROR: {e}")
            return AgentResponse(content="Optimizando conexión con nuestro clúster de datos... Un momento. ✨", latency=0)
