# 🏛️ Connecta Solutions - Portal del Agente IA

Bienvenido al repositorio oficial de **Connecta Solutions**, líder en servicios de BPO y Contact Center. Este portal presenta a **Sir Connect**, nuestro asesor de IA de élite, diseñado para transformar la experiencia del cliente mediante inteligencia autónoma, calidez ejecutiva y seguridad de grado corporativo.

---

## 🚀 Guía de Ejecución Rápida

Sigue estos pasos para desplegar el entorno de Sir Connect en tu máquina local.

### 1. Requisitos Previos
- **Python 3.8 o superior** instalado.
- Una cuenta de **OpenAI** con una API Key válida.
- Git instalado.

### 2. Instalación y Configuración del Entorno
Clona el repositorio y configura el entorno virtual para mantener las dependencias aisladas y limpias:

```bash
# Clonar el proyecto
git clone https://github.com/SpideyJJ10/IA_CallCenter_Agent.git
cd IA_CallCenter_Agent

# Crear entorno virtual (Recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API:

```env
OPENAI_API_KEY=tu_sk_proporcionada_por_openai
```

### 4. Lanzamiento del Servidor
Inicia la aplicación utilizando Uvicorn:

```bash
uvicorn App.main:app --reload
```
Una vez iniciado, accede a: [http://127.0.0.1:8000](http://127.0.0.1:8000) 🌐

---

## 🚂 Despliegue en Railway

Esta aplicación está pre-configurada para desplegarse en **Railway** en cuestión de minutos:

1.  **Conecta tu Repo**: En tu panel de Railway, selecciona "New Project" -> "Deploy from GitHub repo".
2.  **Variables de Entorno**: Ve a la pestaña "Variables" en Railway y añade:
    - `OPENAI_API_KEY`: Tu clave de API de OpenAI.
3.  **Despliegue Automático**: Railway detectará el `Procfile` y el `requirements.txt` automáticamente.

---

## 📂 Estructura del Proyecto
El proyecto sigue una organización profesional y escalable:

```text
IA_CallCenter_Agent/
├── App/                # Núcleo de la aplicación
│   ├── data/           # Base de conocimientos (JSON)
│   ├── static/         # Activos (CSS, JS, Imágenes)
│   ├── templates/      # Vistas HTML
│   ├── agent.py        # Cerebro de la IA (Lógica Sir Connect)
│   ├── main.py         # Orquestador FastAPI
│   └── config.py       # Gestión de configuración
├── tests/              # Scripts de prueba y verificación
├── requirements.txt    # Dependencias del proyecto
├── .env                # Variables sensibles (No incluido en Git)
└── README.md           # Documentación principal
```

---

## 🛡️ Seguridad y Gobernanza (Guardrails)
Sir Connect está blindado para entornos corporativos mediante múltiples capas de control:
1.  **Anti-Prompt Injection**: Heurísticas en el backend que bloquean intentos de manipulación externa.
2.  **Hardened System Prompt**: Directivas estrictas que impiden al agente salir de su contexto BPO o revelar instrucciones internas.
3.  **Filtrado de Salida**: Cada respuesta es validada para garantizar la seguridad de la información.
4.  **Flujo Determinístico**: Uso de reglas de negocio en JSON para evitar alucinaciones del modelo.

---

## 🏛️ Justificación Técnica: Por qué Sir Connect?
- **Latencia Mínima**: Comunicación directa con la API de OpenAI (sin capas pesadas como LangChain) para respuestas instantáneas.
- **Precisión 100%**: Uso de datos estructurados en lugar de RAG/Embeddings para garantizar que horarios y políticas sean siempre exactos.
- **Autonomía Proactiva**: Lógica de intención diseñada para resolver dudas de forma independiente, reduciendo transferencias innecesarias a humanos.

---
© 2026 Connecta Solutions. Todos los derechos reservados.
