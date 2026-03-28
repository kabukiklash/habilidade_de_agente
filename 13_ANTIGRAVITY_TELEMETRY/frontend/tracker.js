/**
 * Antigravity Telemetry Tracker (Pro Max v3.0)
 * Captures 360° context: Clicks, Errors, Console, Performance, and AJAX Timing.
 */
(function() {
    const config = {
        endpoint: '/13_ANTIGRAVITY_TELEMETRY/backend/receiver.php',
        batchSize: 5,
        flushInterval: 3000,
        ignoreUrls: ['receiver.php', 'telemetry'],
        captureConsole: true,
        capturePerformance: true
    };

    let eventQueue = [];
    const sessionId = 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();

    function isInternalRequest(url) {
        return config.ignoreUrls.some(ignored => url.includes(ignored));
    }

    function sendPayload() {
        if (eventQueue.length === 0) return;
        
        const payload = {
            sessionId: sessionId,
            userAgent: navigator.userAgent,
            url: window.location.href,
            title: document.title,
            screen: `${window.screen.width}x${window.screen.height}`,
            timestamp: new Date().toISOString(),
            events: [...eventQueue]
        };
        
        eventQueue = [];
        
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
    }

    function pushEvent(type, data) {
        eventQueue.push({
            type: type,
            timestamp: new Date().toISOString(),
            data: data
        });

        if (eventQueue.length >= config.batchSize) {
            sendPayload();
        }
    }

    // 1. INTERVAL FLUSH
    setInterval(sendPayload, config.flushInterval);

    // 2. PERFORMANCE METRICS
    if (config.capturePerformance) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const nav = performance.getEntriesByType('navigation')[0];
                if (nav) {
                    pushEvent('PERFORMANCE', {
                        loadTime: nav.loadEventEnd,
                        domReady: nav.domContentLoadedEventEnd,
                        dns: nav.domainLookupEnd - nav.domainLookupStart,
                        tcp: nav.connectEnd - nav.connectStart,
                        ttfb: nav.responseStart - nav.requestStart
                    });
                }
            }, 100);
        });
    }

    // 3. CONSOLE INTERCEPTOR
    if (config.captureConsole) {
        ['log', 'warn', 'error'].forEach(level => {
            const original = console[level];
            console[level] = (...args) => {
                pushEvent('CONSOLE_' + level.toUpperCase(), {
                    msg: args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')
                });
                original.apply(console, args);
            };
        });
    }

    // 4. TRACK CLICKS
    document.addEventListener('click', function(e) {
        const target = e.target;
        const path = [];
        let cur = target;
        while(cur && cur !== document.body && path.length < 3) {
            let elDesc = cur.tagName.toLowerCase();
            if (cur.id) elDesc += '#' + cur.id;
            if (cur.className && typeof cur.className === 'string') elDesc += '.' + cur.className.split(' ').join('.');
            path.push(elDesc);
            cur = cur.parentElement;
        }
        
        pushEvent('CLICK', {
            path: path.reverse().join(' > '),
            text: (target.innerText || target.value || '').trim().substring(0, 50),
            node: target.nodeName
        });
    }, true);

    // 5. TRACK ERRORS & STACK TRACES
    window.addEventListener('error', function(e) {
        pushEvent('ERROR', {
            message: e.message,
            stack: e.error ? e.error.stack : 'No stack available',
            file: e.filename,
            line: e.lineno
        });
    });

    // 6. AJAX INTERCEPTOR (with timing)
    const oldOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this._url = url;
        this._method = method;
        this._startTime = Date.now();
        return oldOpen.apply(this, arguments);
    };

    const oldSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function() {
        this.addEventListener('load', function() {
            if (isInternalRequest(this._url)) return;
            const duration = Date.now() - this._startTime;
            
            const contentType = this.getResponseHeader('content-type') || '';
            const isErrorStatus = this.status >= 400;
            const isHtmlInsteadOfJson = (contentType.includes('text/html') && this.responseText.includes('<b>Fatal error</b>'));
            
            const eventType = (isErrorStatus || isHtmlInsteadOfJson) ? 'AJAX_ERROR' : 'AJAX_SUCCESS';
            
            pushEvent(eventType, {
                method: this._method,
                url: this._url,
                status: this.status,
                duration: duration + 'ms',
                response: (isErrorStatus || isHtmlInsteadOfJson) ? this.responseText.substring(0, 500) : 'Payload hidden for success'
            });
        });
        return oldSend.apply(this, arguments);
    };

    // 7. FETCH INTERCEPTOR (with timing)
    const { fetch: originalFetch } = window;
    window.fetch = async (...args) => {
        const start = Date.now();
        const [resource] = args;
        const url = typeof resource === 'string' ? resource : resource.url;
        
        try {
            const response = await originalFetch(...args);
            const duration = Date.now() - start;
            if (!isInternalRequest(url)) {
                if (response.ok) {
                    pushEvent('FETCH_SUCCESS', { url, status: response.status, duration: duration + 'ms' });
                } else {
                    const clone = response.clone();
                    const body = await clone.text();
                    pushEvent('FETCH_ERROR', { url, status: response.status, duration: duration + 'ms', body: body.substring(0, 500) });
                }
            }
            return response;
        } catch (err) {
            const duration = Date.now() - start;
            if (!isInternalRequest(url)) {
                pushEvent('FETCH_CRASH', { url, error: err.message, duration: duration + 'ms' });
            }
            throw err;
        }
    };

    // 8. EXIT
    window.addEventListener('beforeunload', () => {
        pushEvent('EXIT', { url: window.location.href });
        sendPayload();
    });

    window.AntigravityTelemetry = {
        log: (msg, meta) => pushEvent('CUSTOM', { msg, meta }),
        setConfig: (c) => Object.assign(config, c),
        id: sessionId
    };

    console.log("🚀 Antigravity Telemetry Pro Max v3.0 Active [" + sessionId + "]");
})();
