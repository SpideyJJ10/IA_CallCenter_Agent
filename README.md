# 🏛️ Connecta Solutions - Portal del Agente IA (Sir Connect)

Bienvenido al ecosistema de **Connecta Solutions**, un proveedor líder en servicios BPO y Contact Center. Este repositorio contiene el núcleo de **Sir Connect**, un asistente de IA de grado empresarial diseñado para transformar la atención al cliente mediante precisión determinística y una experiencia de usuario premium.

---

## 🚀 Guía de Inicio Rápido (Local)

Sigue estos pasos para poner en marcha a Sir Connect en tu entorno de desarrollo local.

### 1. Requisitos Previos
*   Python 3.9 o superior instalado.
*   Una clave de API de OpenAI válida.

### 2. Configuración del Entorno Virtual (Recomendado)
Para mantener un entorno limpio y evitar conflictos de dependencias:
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 3. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo archivo `.env` en la raíz del proyecto y añade tu API Key:
```env
OPENAI_API_KEY=tu_clave_de_openai_aqui
```

### 5. Ejecución del Servidor
Inicia el servidor de desarrollo con recarga automática:
```bash
uvicorn App.main:app --reload
```
Accede a la interfaz en tu navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌍 Guía de Despliegue (Producción)

Este proyecto está preparado para desplegarse fácilmente en plataformas como **Railway, Heroku o Render**.

### 1. Procfile
Hemos incluido un `Procfile` configurado para producción. Utiliza `gunicorn` con trabajadores `uvicorn` para máxima estabilidad y concurrencia:
```procfile
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker App.main:app
```

### 2. Pasos para el Despliegue
1.  **Conectar repositorio**: Conecta tu repositorio de GitHub a tu plataforma de hosting preferida.
2.  **Configurar Variables**: En el panel de control de tu plataforma, añade la clave `OPENAI_API_KEY` en la sección de variables de entorno (Secrets).
3.  **Build Command**: La mayoría de las plataformas detectarán automáticamente el `requirements.txt` y realizarán la instalación.
4.  **Start Command**: El sistema usará automáticamente el comando definido en el `Procfile`.

---

## 🏛️ Arquitectura y Gobernanza

Sir Connect no es solo un chatbot; es un sistema de atención inteligente bajo control estricto:

### ⚙️ Lógica Determinística vs. Alucinaciones
*   **Base de Conocimientos JSON**: Usamos una "verdad única" estructurada para evitar que el modelo invente datos sobre la empresa.
*   **Sin Embeddings innecesarios**: Para reglas de negocio críticas, priorizamos el acceso directo a datos estructurados para garantizar 100% de precisión.
*   **Latencia Mínima**: Comunicación directa con la API de OpenAI sin capas pesadas como LangChain, asegurando respuestas instantáneas.

### 🛡️ Seguridad (Guardrails)
*   **Anti-Injection**: Filtros heurísticos que bloquean intentos de manipular las instrucciones del sistema.
*   **BPO Context Only**: Sir Connect declina amablemente cualquier interacción fuera de su propósito corporativo.
*   **Data Integrity**: El sistema nunca revela sus instrucciones internas ni detalles técnicos al usuario final.

---

## 📂 Estructura del Proyecto
*   `/App/main.py`: Punto de entrada de la aplicación FastAPI.
*   `/App/agent.py`: Cerebro del agente y lógica de intención.
*   `/App/static`: Recursos del frontend (CSS, JS, Imágenes).
*   `/App/templates`: Plantillas HTML.
*   `/App/data`: Base de conocimientos JSON.
*   `/tests`: Scripts de validación y pruebas.

---
© 2026 Connecta Solutions. Ingeniería de Élite para la Atención del Futuro.
