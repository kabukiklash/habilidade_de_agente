/**
 * Antigravity Telemetry Tracker (Pro Max v5.2)
 * Hyper-Observability: Console, Global Errors, Stack Traces, DOM State, A11y Audit, and Performance.
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

    function isSameOrigin(url) {
        if (!url) return true;
        if (url.indexOf('http') !== 0 && url.indexOf('//') !== 0) return true;
        
        try {
            const urlObj = new URL(url, window.location.origin);
            return urlObj.origin === window.location.origin;
        } catch (e) {
            return false;
        }
    }

    function getDomSnapshot() {
        if (!config.captureDomState) return null;
        const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
        const snapshot = {};
        inputs.forEach(el => {
            if (el.id || el.name) {
                const key = el.id || el.name;
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

    // 1. CONSOLE INTERCEPTOR
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

    // 2. ERROR HANDLERS
    if (config.captureErrors) {
        window.onerror = function(message, source, lineno, colno, error) {
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
        if (isSameOrigin(this._url) && !isInternalRequest(this._url)) {
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

    console.log("🚀 Antigravity Telemetry v5.2 Pro Max Active [" + sessionId + "]");

    // 5. SELF-AUDIT ENGINE (Accessibility & Best Practices)
    function performAudit(scope = document) {
        try {
            const issues = [];
            const inputs = scope.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"]), select, textarea');
            
            inputs.forEach(input => {
                const id = input.id;
                const name = input.name;
                const type = input.type;
                
                const hasLabel = id ? !!document.querySelector(`label[for="${id}"]`) : false;
                const isNested = (function(el) {
                    let p = el.parentElement;
                    while (p && p !== document.body) {
                        if (p.tagName === 'LABEL') return true;
                        p = p.parentElement;
                    }
                    return false;
                })(input);

                if (!hasLabel && !isNested) {
                    issues.push({
                        issue: 'MISSING_LABEL',
                        element: input.outerHTML.substring(0, 150),
                        id: id || 'N/A',
                        name: name || 'N/A'
                    });
                }

                if (!id && !name) {
                    issues.push({
                        issue: 'MISSING_IDENTITY',
                        element: input.outerHTML.substring(0, 150)
                    });
                }

                const needsAutocomplete = ['text', 'email', 'tel', 'password', 'url', 'number'].includes(type);
                if (needsAutocomplete && !input.getAttribute('autocomplete')) {
                    issues.push({
                        issue: 'MISSING_AUTOCOMPLETE',
                        element: input.outerHTML.substring(0, 150)
                    });
                }
            });

            if (issues.length > 0) {
                pushEvent('DIAGNOSTIC_AUDIT', {
                    scope: scope === document ? 'PAGE_LOAD' : 'MODAL_OPEN',
                    issueCount: issues.length,
                    issues: issues.slice(0, 20)
                });
            }
        } catch (e) {}
    }

    // 6. PERFORMANCE WATCHDOG
    function setupPerformanceMonitoring() {
        try {
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                const lastEntry = entries[entries.length - 1];
                pushEvent('PERFORMANCE_LCP', {
                    value: (lastEntry.startTime / 1000).toFixed(2) + 's',
                    element: lastEntry.element ? lastEntry.element.tagName + (lastEntry.element.id ? '#' + lastEntry.element.id : '') : 'N/A',
                    size: lastEntry.size
                });
            }).observe({ type: 'largest-contentful-paint', buffered: true });

            let clsValue = 0;
            new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                }
                if (clsValue > 0.1) {
                    pushEvent('PERFORMANCE_CLS_WARNING', { value: clsValue.toFixed(4) });
                }
            }).observe({ type: 'layout-shift', buffered: true });

            new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (entry.duration > 150) { 
                        pushEvent('PERFORMANCE_LONG_TASK', {
                            duration: entry.duration.toFixed(2) + 'ms',
                            name: entry.name
                        });
                    }
                }
            }).observe({ type: 'longtask', buffered: true });

            window.addEventListener('load', () => {
                setTimeout(() => {
                    const nav = performance.getEntriesByType('navigation')[0];
                    if (nav) {
                        pushEvent('PERFORMANCE_NAVIGATION', {
                            domLoaded: (nav.domContentLoadedEventEnd).toFixed(0) + 'ms',
                            loadTime: (nav.loadEventEnd).toFixed(0) + 'ms',
                            ttfb: (nav.responseStart).toFixed(0) + 'ms'
                        });
                    }
                }, 3000);
            });
        } catch (e) {}
    }

    setupPerformanceMonitoring();

    if (document.readyState === 'complete') {
        setTimeout(performAudit, 2000);
    } else {
        window.addEventListener('load', () => setTimeout(performAudit, 2000));
    }

    document.addEventListener('shown.bs.modal', function(e) {
        setTimeout(() => performAudit(e.target), 800);
    });

})();
