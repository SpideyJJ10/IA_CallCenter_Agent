const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const latencyDisplay = document.getElementById('latency');

let conversationHistory = [];
let transferTimer = null;
let isTransferring = false;

function formatText(text) {
    // Simple markdown: bold and line breaks
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', role);

    const contentDiv = document.createElement('div');
    contentDiv.innerHTML = formatText(text);
    msgDiv.appendChild(contentDiv);

    if (role === 'user' || role === 'agent') {
        const metaDiv = document.createElement('div');
        metaDiv.classList.add('status-meta');
        metaDiv.innerHTML = role === 'user' ? '<span>Entregado</span>' : '<span>✓ Sir Connect</span>';
        msgDiv.appendChild(metaDiv);
    }

    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msgDiv;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.classList.add('typing-indicator');
    indicator.id = 'typing-bubble';
    indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    chatWindow.appendChild(indicator);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return indicator;
}

async function sendMessage(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    userInput.value = '';
    conversationHistory.push({ role: 'user', content: message });

    const typing = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history: conversationHistory })
        });

        const data = await response.json();

        // Aceleración de respuesta: Reducción drástica del retardo artificial para una experiencia "snappy"
        const typeDelay = Math.min(Math.max(data.response.length * 5, 300), 1200);
        await new Promise(resolve => setTimeout(resolve, typeDelay));

        typing.remove();

        const agentMsg = appendMessage('agent', data.response);
        conversationHistory.push({ role: 'agent', content: data.response });

        // Update user message status to "Leído" after agent responds
        const userMessages = document.querySelectorAll('.message.user .status-meta span');
        if (userMessages.length > 0) {
            userMessages[userMessages.length - 1].textContent = 'Leído ✓✓';
        }

        latencyDisplay.textContent = `Latencia: ${Math.round(data.latency_seconds * 1000)} ms`;

        if (data.transfer) {
            isTransferring = true;
            setTimeout(() => handleTransfer(), 3000);
        }
    } catch (err) {
        if (typing) typing.remove();
        console.error('Error:', err);
        appendMessage('agent', 'Lo siento, ocurrió un error al conectar con el servidor.');
    }
}

async function handleTransfer() {
    if (!isTransferring) return;

    const overlay = document.getElementById('transfer-overlay');
    const queueNum = document.getElementById('queue-num');
    const queueBar = document.getElementById('queue-bar');
    const cancelBtn = document.getElementById('cancel-transfer');

    overlay.classList.add('active');
    userInput.disabled = true;
    document.getElementById('send-btn').disabled = true;

    // Cancel logic
    cancelBtn.onclick = () => {
        isTransferring = false;
        overlay.classList.remove('active');
        userInput.disabled = false;
        document.getElementById('send-btn').disabled = false;
        appendMessage('agent', 'Entendido. He cancelado la transferencia. Sigo aquí para ayudarte con lo que necesites. ¿En qué íbamos? 😊');
        userInput.focus();
    };

    let position = 3;
    let cycles = 0;
    const maxCycles = 8 + Math.floor(Math.random() * 5); // Realistic long wait

    const waitMessages = [
        "Verificando disponibilidad de expertos...",
        "Analizando el contexto de tu consulta...",
        "Buscando el mejor perfil para tu solicitud...",
        "Sincronizando historial con la base de datos...",
        "Conectando con el servidor de prioridad..."
    ];

    while (isTransferring) {
        queueNum.textContent = position;
        const progress = position === 0 ? 100 : (1 - (position / 4)) * 100;
        queueBar.style.width = `${progress}%`;

        document.querySelector('.transfer-status').textContent = waitMessages[cycles % waitMessages.length];

        if (position === 0) {
            document.querySelector('.transfer-title').textContent = '¡Conectado!';
            document.querySelector('.transfer-status').textContent = 'Un asesor experto se ha unido a la conversación.';
            queueNum.innerHTML = '<span style="color: #10B981;">✓</span>';
            queueBar.style.background = '#10B981';
            cancelBtn.style.display = 'none';

            await new Promise(resolve => setTimeout(resolve, 2500));
            if (!isTransferring) break;

            overlay.classList.remove('active');
            appendMessage('agent', '¡Gracias por tu paciencia! He revisado nuestros registros de prioridad y he diseñado una solución adaptada a lo que conversamos anteriormente. ¿Podrías confirmarme más detalles para proceder? ✨');
            userInput.disabled = false;
            document.getElementById('send-btn').disabled = false;
            isTransferring = false;
            userInput.focus();
            break;
        }

        const waitTime = 4000 + Math.random() * 3000;
        await new Promise(resolve => setTimeout(resolve, waitTime));

        if (!isTransferring) break;

        cycles++;

        if (position > 1) {
            position--;
        } else if (cycles >= maxCycles) {
            position = 0;
        } else {
            position = Math.random() > 0.7 ? 2 : 1;
        }
    }
}

// Initial Greeting
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        appendMessage('agent', '¡Hola! Soy **Sir Connect**, tu asistente experto de **Connecta Solutions**. Estoy aquí para asesorarte sobre nuestros servicios BPO de clase mundial. ¿En qué puedo apoyarte hoy? ✨');
    }, 800);
});

chatForm.addEventListener('submit', sendMessage);
