/**
 * Antigravity Telemetry Tracker (Pro Max v5.0)
 * Hyper-Observability: Console, Global Errors, Stack Traces, and DOM State.
 */
(function() {
    const config = {
        endpoint: '13_ANTIGRAVITY_TELEMETRY/backend/receiver.php',
        batchSize: 50,
        flushInterval: 10000,
        ignoreUrls: ['receiver.php', 'telemetry', 'viacep.com.br', 'googleapis.com'],
        captureConsole: true,
        captureErrors: true,
        captureDomState: true,
        capturePayload: true,
        captureAllResponses: false
    };

    let eventQueue = [];
    const sessionId = 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    let currentTraceId = 't_' + Math.random().toString(36).substr(2, 9);

    function generateTraceId() {
        return 't_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    function isInternalRequest(url) {
        return config.ignoreUrls.some(ignored => url.includes(ignored));
    }

    function getDomSnapshot() {
        if (!config.captureDomState) return null;
        const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
        const snapshot = {};
        inputs.forEach(el => {
            if (el.id || el.name) {
                const key = el.id || el.name;
                // Mask sensitive info
                if (el.type === 'password' || key.toLowerCase().includes('pass')) {
                    snapshot[key] = '***';
                } else {
                    snapshot[key] = el.value;
                }
            }
        });
        return snapshot;
    }

    function maskSensitiveData(data) {
        if (!data) return data;
        let str = typeof data === 'string' ? data : JSON.stringify(data);
        const sensitiveKeys = ['password', 'senha', 'token', 'auth', 'credit_card', 'cvv'];
        
        try {
            let obj = JSON.parse(str);
            const mask = (o) => {
                for (let key in o) {
                    if (sensitiveKeys.some(sk => key.toLowerCase().includes(sk))) {
                        o[key] = '***';
                    } else if (typeof o[key] === 'object' && o[key] !== null) {
                        mask(o[key]);
                    }
                }
            };
            mask(obj);
            return obj;
        } catch (e) {
            // If not JSON, use regex for basic masking
            sensitiveKeys.forEach(key => {
                const reg = new RegExp('(' + key + '[^=]*=[\\s"\']*)[^&"\'\\s]*', 'gi');
                str = str.replace(reg, '$1***');
            });
            return str;
        }
    }

    function captureContext(element) {
        if (!element) return null;
        let context = element;
        for (let i = 0; i < 2; i++) {
            if (context.parentElement && context.parentElement !== document.body) {
                context = context.parentElement;
            }
        }
        const clone = context.cloneNode(true);
        const sensitveSelectors = ['input[type="password"]', 'input[type="email"]', '.sensitive'];
        sensitveSelectors.forEach(selector => {
            clone.querySelectorAll(selector).forEach(el => {
                el.value = '***';
                el.innerText = '***';
                el.setAttribute('placeholder', 'MASKED');
            });
        });
        let html = clone.outerHTML;
        return html.length > 1000 ? html.substring(0, 1000) + '... [TRUNCATED]' : html;
    }

    let silenceTracker = false;

    function sendPayload() {
        if (eventQueue.length === 0 || silenceTracker) return;
        
        silenceTracker = true;
        const payload = {
            sessionId: sessionId,
            userAgent: navigator.userAgent,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            events: [...eventQueue]
        };
        eventQueue = [];
        
        try {
            if (navigator.sendBeacon) {
                navigator.sendBeacon(config.endpoint, JSON.stringify(payload));
            } else {
                fetch(config.endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                    keepalive: true
                }).catch(() => {});
            }
        } catch (e) {
            // Silently ignore errors from the telemetry system itself
        } finally {
            silenceTracker = false;
        }
    }

    function pushEvent(type, data) {
        if (silenceTracker) return;
        
        eventQueue.push({
            type: type,
            timestamp: new Date().toISOString(),
            traceId: currentTraceId,
            data: data
        });
        
        if (eventQueue.length >= config.batchSize) {
            sendPayload();
        }
    }

    setInterval(sendPayload, config.flushInterval);

    // 1. CONSOLE INTERCEPTOR PRO
    if (config.captureConsole) {
        ['log', 'warn', 'error'].forEach(level => {
            const original = console[level];
            console[level] = (...args) => {
                const msg = args.map(a => {
                    if (a instanceof Error) return { message: a.message, stack: a.stack };
                    try {
                        return typeof a === 'object' ? JSON.stringify(a) : String(a);
                    } catch (e) {
                        return "[Unserializable Object]";
                    }
                }).join(' ');

                pushEvent('CONSOLE_' + level.toUpperCase(), {
                    msg: msg,
                    domState: level === 'error' ? getDomSnapshot() : null
                });
                original.apply(console, args);
            };
        });
    }

    // 2. GLOBAL ERROR HANDLERS (The Black Box)
    if (config.captureErrors) {
        window.onerror = function(message, source, lineno, colno, error) {
            // Ignore browser extension errors and context invalidation noise
            if (String(message).includes('Extension context invalidated') || (source && source.includes('chrome-extension:'))) {
                return false;
            }
            
            pushEvent('FATAL_ERROR', {
                message: message,
                source: source,
                line: lineno,
                col: colno,
                stack: error ? error.stack : 'N/A',
                domState: getDomSnapshot()
            });
            sendPayload();
            return false;
        };

        window.onunhandledrejection = function(event) {
            pushEvent('PROMISE_REJECTION', {
                reason: event.reason ? (event.reason.message || event.reason) : 'Unknown',
                stack: event.reason ? event.reason.stack : 'N/A',
                domState: getDomSnapshot()
            });
            sendPayload();
        };
    }

    // 3. EVENT TRACKING
    document.addEventListener('click', function(e) {
        currentTraceId = generateTraceId();
        const target = e.target;
        pushEvent('CLICK', {
            path: target.tagName,
            id: target.id || 'N/A',
            text: (target.innerText || target.value || '').trim().substring(0, 50),
            snapshot: captureContext(target),
            domState: getDomSnapshot()
        });
    }, true);

    // 4. AJAX INTERCEPTOR
    const oldOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this._url = url;
        this._method = method;
        this._startTime = Date.now();
        this._traceId = currentTraceId;
        return oldOpen.apply(this, arguments);
    };

    const oldSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function(data) {
        if (!isInternalRequest(this._url)) {
            this.setRequestHeader('X-AG-Trace-ID', this._traceId);
            if (config.capturePayload && data) {
                this._payload = maskSensitiveData(data);
            }
        }
        this.addEventListener('load', function() {
            if (isInternalRequest(this._url)) return;
            pushEvent('AJAX', {
                method: this._method,
                url: this._url,
                status: this.status,
                duration: (Date.now() - this._startTime) + 'ms',
                traceId: this._traceId,
                payload: this._payload || null,
                response: (function(xhr) {
                    if (config.captureAllResponses || xhr.status >= 400) {
                        try {
                            // Check if responseType allows responseText access
                            if (!xhr.responseType || xhr.responseType === 'text') {
                                return xhr.responseText ? xhr.responseText.substring(0, 1000) : null;
                            }
                            return "[Non-text response: " + xhr.responseType + "]";
                        } catch (e) {
                            return "[Error reading response: " + e.message + "]";
                        }
                    }
                    return null;
                })(this)
            });
        });
        return oldSend.apply(this, arguments);
    };

    console.log("🚀 Antigravity Telemetry v5.0 Pro Max Active [" + sessionId + "]");
})();

