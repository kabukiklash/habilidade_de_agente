/**
 * Sentry V3 - Client Side Telemetry Bridge (Military Grade + Visual)
 * Desenvolvido por Antigravity para AfixControl
 */

(function () {
    // Detectar o caminho base dinamicamente
    const scriptTag = document.currentScript;
    const scriptPath = scriptTag ? scriptTag.src : '';
    let collectorURL = scriptPath.replace('sentry-client.js', 'collector.php');

    // Helper para adicionar query params sem quebrar o URL (evita double ??)
    function getFinalURL(action) {
        // Collector URL may already have ?update=...
        const urlObj = new URL(collectorURL, window.location.origin);
        urlObj.searchParams.set('action', action);
        return urlObj.toString();
    }

    let isSentryActive = false;
    let currentMissionID = localStorage.getItem('sentry_mission_id') || "";
    let consoleBuffer = [];

    // Injetar html2canvas apenas se necessário (otimização de carregamento)
    function injectVisualEngine() {
        if (document.getElementById('sentry-h2c')) return;
        const h2cScript = document.createElement('script');
        h2cScript.id = 'sentry-h2c';
        h2cScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        document.head.appendChild(h2cScript);
    }

    // Proxy para Console
    const originalConsoleError = console.error;
    const originalConsoleWarn = console.warn;

    console.error = function() {
        const msg = Array.from(arguments).map(arg => typeof arg === 'object' ? JSON.stringify(arg) : arg).join(' ');
        consoleBuffer.push({ type: 'error', msg, timestamp: new Date().toISOString() });
        // Defer capture to avoid blocking the console
        setTimeout(() => captureSnapshot({ type: 'console_error', target: { tagName: 'WINDOW' } }, msg), 100);
        originalConsoleError.apply(console, arguments);
    };

    console.warn = function() {
        const msg = Array.from(arguments).map(arg => typeof arg === 'object' ? JSON.stringify(arg) : arg).join(' ');
        consoleBuffer.push({ type: 'warn', msg, timestamp: new Date().toISOString() });
        originalConsoleWarn.apply(console, arguments);
    };

    // Global Error Handler
    window.onerror = function(message, source, lineno, colno, error) {
        const msg = `ERROR: ${message} at ${source}:${lineno}:${colno}`;
        captureSnapshot({ type: 'window_error', target: { tagName: 'WINDOW' } }, msg);
    };

    // Verificar se o Sentinela está ativo
    async function checkSentryStatus() {
        try {
            const response = await fetch(getFinalURL('get_status'));
            const data = await response.json();
            
            // Sync local state with server
            const serverActive = data.active;
            const serverMission = data.current_mission;
            
            if (serverActive !== isSentryActive || serverMission !== currentMissionID) {
                isSentryActive = serverActive;
                currentMissionID = serverMission;
                
                if (isSentryActive) {
                    injectVisualEngine();
                    console.log(`%c🛡️ SENTRY V3: Monitoramento ATIVO [ID: ${currentMissionID}]`, 'color: #00f2ff; font-weight: bold;');
                }
            }
        } catch (e) {
            // Fallback para localStorage se o servidor estiver inacessível temporariamente
            isSentryActive = localStorage.getItem('sentry_active') === 'true';
            currentMissionID = localStorage.getItem('sentry_mission_id') || "";
        }
    }

    // Listener para mudanças instantâneas entre abas
    window.addEventListener('storage', (event) => {
        if (event.key === 'sentry_active') {
            isSentryActive = event.newValue === 'true';
            console.log(`%c🛡️ SENTRY V3: Status alterado via Broadcast -> ${isSentryActive ? 'ON' : 'OFF'}`, 'color: #00f2ff;');
        }
        if (event.key === 'sentry_mission_id') {
            currentMissionID = event.newValue || "";
        }
    });

    // Capturar o Snapshot do DOM + Visual e enviar
    async function captureSnapshot(event, extraMsg = '') {
        if (!isSentryActive) return;

        const target = event.target || { tagName: 'unknown' };
        const selector = event.target ? getSelector(target) : 'unknown';
        
        // Capturar Visual Snapshot se html2canvas estiver carregado
        let visualData = null;
        if (typeof html2canvas !== 'undefined') {
            try {
                const canvas = await html2canvas(document.body, {
                    scale: 0.5, // Reduzir escala para economizar banda
                    logging: false,
                    useCORS: true
                });
                visualData = canvas.toDataURL('image/jpeg', 0.6); // Salvar como JPEG comprimido
            } catch (e) {
                console.warn('Sentry: Falha ao capturar imagem.', e);
            }
        }

        const metadata = {
            url: window.location.href,
            timestamp: new Date().toISOString(),
            mission_id: currentMissionID, // Vinculação explícita
            action: event.type,
            target: selector,
            extra: extraMsg,
            recent_logs: consoleBuffer.slice(-5),
            screen_size: `${window.innerWidth}x${window.innerHeight}`
        };

        const domState = document.documentElement.outerHTML.substring(0, 200000); 

        const formData = new FormData();
        formData.append('action', 'save_snapshot');
        formData.append('metadata', JSON.stringify(metadata));
        formData.append('data', domState);
        if (visualData) {
            formData.append('visual', visualData);
        }

        try {
            // Deferir o envio para não travar o socket do navegador
            setTimeout(() => {
                fetch(collectorURL, {
                    method: 'POST',
                    body: formData
                });
            }, 10);
        } catch (e) {
            // Silencioso
        }
    }

    // Gerar um seletor amigável
    function getSelector(el) {
        if (!el || !el.tagName) return 'unknown';
        if (el.id) return `#${el.id}`;
        if (el.className && typeof el.className === 'string') return `.${el.className.split(' ').join('.')}`;
        return el.tagName.toLowerCase();
    }

    // Inicialização
    document.addEventListener('click', (e) => {
        // Envolver em setTimeout(500) para garantir que o evento original (abrir modal, navegar, etc)
        // seja processado e as animações concluídas ANTES da pesada captura do html2canvas.
        setTimeout(() => captureSnapshot(e), 500);
    }, false); // Usar Bubble Phase (false) para não interceptar o evento prematuramente
    checkSentryStatus();
    setInterval(checkSentryStatus, 5000); // Frequência aumentada para 5s (Military Grade Sync)

    // Log de Inicialização para Debug
    setTimeout(() => {
        const pingData = new FormData();
        pingData.append('action', 'save_log');
        pingData.append('msg', `Client Bridge Initialized on ${window.location.href}`);
        pingData.append('level', 'debug');
        fetch(collectorURL, { method: 'POST', body: pingData }); // POST não usa ?action no URL se estiver no body, mas por segurança o collector.php aceita ambos.
    }, 1000);

})();

