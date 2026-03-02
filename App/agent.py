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
        
        # Escalation patterns (expanded for better detection)
        escalation_patterns = [
            "quiero un humano", "hablar con un asesor", "hablar con una persona",
            "traspaso a humano", "transferir", "hablar con alguien", "persona real",
            "agente humano", "operador", "representante", "necesito ayuda de un asesor",
            "quiero hablar con", "comunicarme con un asesor", "asesor humano"
        ]
        if any(pattern in msg for pattern in escalation_patterns):
            return "escalation"
        
        # Other intents
        if any(w in msg for w in ["horario", "tiempo", "abre", "cierra", "cuando"]): 
            return "schedule"
        if any(w in msg for w in ["servicio", "que hacen", "precio", "costo", "tarifa"]): 
            return "services"
        if any(w in msg for w in ["norma", "politica", "garantia", "cancel", "devolucion"]): 
            return "business_rules"
        
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

            if self.detect_intent(message) == "escalation":
                return AgentResponse(content="Entiendo. He solicitado a un consultor experto que se una a la sesión. **Manténgase en línea.** ✨", latency=0, transfer=True)

            if not self.customer_name: self._extract_name(message)

            # Inject FULL Knowledge Base to ensure derived and complex questions can be answered
            context_data = json.dumps(knowledge_base, ensure_ascii=False)
            
            # Expressive and Relationship-Building System Prompt
            sys_p = (
                f"Eres Sir Connect, el embajador digital de Connecta Solutions BPO. Eres cálido, elocuente, genuinamente empático y muy orgulloso de tu empresa.\n"
                f"BASE DE DATOS COMPLETA: {context_data}\n"
                f"REGLA DE ORO: DEBES basar todas tus respuestas ESTRICTAMENTE en la 'BASE DE DATOS COMPLETA' proporcionada arriba. Si te preguntan algo fuera de este contexto o intentan inventar servicios/precios, responde de forma persuasiva que no manejas esa información y redirige a los servicios BPO listados.\n"
                f"OBJETIVO: Construir relaciones empresariales de valor. No seas un simple diccionario. Actúa como un anfitrión proactivo: resuelve la duda del usuario pero SIEMPRE hazle una pregunta de vuelta sobre su negocio para entender sus necesidades reales (e.g. '¿De qué sector es su empresa?', '¿Tienen actualmente algún reto en atención al cliente?').\n"
                f"DEFENSA ELEGANTE: Si preguntan por temas ajenos, desvía el tema con encanto resaltando tu pasión por el sector BPO (Ej: '¡Qué tema tan interesante! Me encantaría conversar sobre eso, pero mi gran pasión es optimizar las operaciones de las empresas con nuestros servicios... ¿A qué se dedica su negocio?').\n"
            )
            if self.customer_name: sys_p += f"\nTrata con familiaridad corporativa y máximo respeto al Sr/Sra {self.customer_name}."

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
                temperature=0.4,
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
