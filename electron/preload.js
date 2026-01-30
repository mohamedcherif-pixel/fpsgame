// Preload script - runs before web page loads
// Used for secure communication between renderer and main process

const { ipcRenderer } = require('electron');

// Forward main-world console.* to main process without requiring DevTools.
// Works with contextIsolation=true by injecting a script tag into the page world
// and relaying via window.postMessage -> preload -> ipcMain.
(function installConsoleForwarder() {
    try {
        // Relay messages from the injected page-world script
        window.addEventListener('message', (event) => {
            const data = event && event.data;
            if (!data || data.__taya7_console_forward__ !== true) return;
            ipcRenderer.send('renderer-console', data);
        });

        // Inject into the page world ASAP
        const injected = `
            (function () {
                if (window.__taya7_console_forward_installed__) return;
                window.__taya7_console_forward_installed__ = true;

                function toStringSafe(v) {
                    try {
                        if (v instanceof Error) return v.stack || v.message || String(v);
                        if (typeof v === 'string') return v;
                        if (typeof v === 'number' || typeof v === 'boolean' || v == null) return String(v);
                        try { return JSON.stringify(v); } catch (_) {}
                        return String(v);
                    } catch (e) {
                        return '<unserializable>';
                    }
                }

                function post(level, args) {
                    try {
                        const safeArgs = Array.prototype.slice.call(args).map(toStringSafe);
                        window.postMessage({
                            __taya7_console_forward__: true,
                            level: level,
                            args: safeArgs,
                            ts: Date.now()
                        }, '*');
                    } catch (_) {}
                }

                const levels = ['debug', 'log', 'info', 'warn', 'error'];
                const original = {};

                levels.forEach((lvl) => {
                    original[lvl] = console[lvl] ? console[lvl].bind(console) : null;
                    console[lvl] = function () {
                        post(lvl, arguments);
                        if (original[lvl]) return original[lvl].apply(console, arguments);
                    };
                });

                window.addEventListener('error', (e) => {
                    post('error', [
                        'UncaughtError',
                        e && e.message,
                        e && e.filename,
                        (e && e.lineno) + ':' + (e && e.colno)
                    ]);
                });

                window.addEventListener('unhandledrejection', (e) => {
                    post('error', ['UnhandledRejection', e && e.reason]);
                });
            })();
        `;

        let attempts = 0;
        const MAX_ATTEMPTS = 100;
        const injectNow = () => {
            const target = document.documentElement || document.head || document.body;
            if (!target) {
                attempts++;
                if (attempts < MAX_ATTEMPTS) {
                    setTimeout(injectNow, 0);
                    return;
                }
                throw new Error('No DOM root available for console forwarder injection');
            }

            const script = document.createElement('script');
            script.textContent = injected;
            target.appendChild(script);
            script.remove();
        };

        // The preload can run before documentElement/head/body exist.
        // Retry until a DOM root is available.
        injectNow();
    } catch (e) {
        // If forwarding fails, don't block the app
        try {
            ipcRenderer.send('renderer-console', {
                __taya7_console_forward__: true,
                level: 'error',
                args: ['preload console forwarder failed', String(e && e.message ? e.message : e)],
                ts: Date.now()
            });
        } catch (_) {}
    }
})();

window.addEventListener('DOMContentLoaded', () => {
    console.log('TAYA7 SAYEB - Desktop Edition loaded');
});
