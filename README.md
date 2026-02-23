# 🏛️ Connecta Solutions - Portal del Agente IA

Bienvenido al repositorio oficial de **Connecta Solutions**, un proveedor de BPO y Contact Center de clase mundial. Este proyecto presenta a **Sir Connect**, un asistente de IA avanzado diseñado para ofrecer atención al cliente de élite con precisión y calidez.

## ### 1. Descripción del proyecto

**Sir Connect** es un prototipo funcional de un Agente de IA para BPO que automatiza la atención al cliente de primer nivel. El sistema está diseñado para:
- Responder consultas sobre horarios, servicios y políticas empresariales.
- Capturar el nombre del cliente para una atención personalizada.
- Gestionar escalamientos a asesores humanos de forma inteligente.
- Cumplir con requisitos de **baja latencia**, **precisión determinística** y **seguridad de datos**.

## ### 2. Arquitectura

El ecosistema de Sir Connect se basa en una arquitectura modular y ligera:

- **Orquestador**: Un backend desarrollado en **FastAPI** que gestiona el flujo de mensajes, el historial de conversación y la lógica de negocio.
- **Control de Escalamiento**: Un sistema basado en intención y conteo de intentos que detecta cuándo un cliente requiere atención humana o cuando el agente no puede resolver una duda compleja.
- **Uso de LLM**: Implementación refinada de **OpenAI GPT-4o-mini**, optimizada mediante *System Prompts* de alta precisión para mantener un tono corporativo y evitar redundancias.
- **Base de Conocimiento JSON**: Una estructura de datos estructurada que actúa como la "verdad única" de la empresa, garantizando que el agente nunca invente información fuera de las políticas de Connecta Solutions.

## Seguridad y Gobernanza (Guardrails) 🛡️🔐
Para garantizar la integridad corporativa y prevenir el mal uso de la IA, el sistema implementa múltiples capas de protección:
1.  **Detección de Inyección (Heurística)**: El backend intercepta patrones conocidos de "Prompt Injection" (ej. "ignore previous instructions") antes de que lleguen al modelo.
2.  **Hardened System Prompt**: Sir Connect opera bajo directivas estrictas que le prohíben revelar instrucciones internas, adoptar roles no autorizados o salir del contexto de **Connecta Solutions**.
3.  **Filtrado de Salida**: Cada respuesta del modelo es verificada para asegurar que no se haya filtrado información sensible o instrucciones del sistema.
4.  **Entorno Determinístico**: Al no depender de agentes autónomos sin supervisión (tipo AutoGPT), el flujo de la conversación permanece siempre bajo los límites de negocio definidos en el JSON.

## ### 3. Cómo ejecutar

1.  **Clonar el repositorio**:
    ```bash
    git clone [url-del-repositorio]
    cd Test_work
    ```
2.  **Configurar el entorno**:
    - Crea un archivo `.env` en la raíz con tu clave: `OPENAI_API_KEY=tu_clave_aqui`
    - Instala las dependencias: `pip install fastapi uvicorn openai python-dotenv`
3.  **Iniciar el servidor**:
    ```bash
    uvicorn App.main:app --reload
    ```
4.  **Acceder**: Abre `http://127.0.0.1:8000` en tu navegador.

## ### 4. Justificación técnica

A diferencia de otros desarrollos, Sir Connect utiliza un enfoque de **Ingeniería de Precisión**:

- **Por qué NO usamos Embeddings**: En un entorno de BPO con políticas fijas (como horarios y precios), los embeddings pueden introducir imprecisiones. El uso de un JSON estructurado garantiza que la respuesta sea 100% veraz y coherente.
- **Por qué NO usamos LangChain**: Para este prototipo, priorizamos la **latencia mínima**. LangChain añade capas de abstracción que incrementan los tiempos de respuesta. Sir Connect se comunica directamente con la API de OpenAI para una experiencia instantánea.
- **Uso de Control Determinístico**: Hemos implementado heurísticas en la detección de intenciones para asegurar que reglas de negocio críticas (como cancelaciones o garantías) se manejen siempre bajo el protocolo estricto de la empresa, eliminando el riesgo de alucinaciones del modelo.

---
© 2026 Connecta Solutions. Todos los derechos reservados.
