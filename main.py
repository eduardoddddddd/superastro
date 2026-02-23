"""SuperAstro — Launcher.

Modos de ejecución:
  python main.py            → abre ventana PyWebView (app de escritorio)
  python main.py --server   → solo levanta FastAPI en http://localhost:8000 (dev)
  python main.py --dev      → FastAPI + abre navegador del sistema (sin PyWebView)
"""

import sys
import os
import threading
import time
import argparse

# Añadir directorio raíz al path para que funcionen los imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

PORT = 8765


def start_server(host="127.0.0.1", port=PORT):
    """Inicia FastAPI en un hilo."""
    config = uvicorn.Config(
        "api.app:app",
        host=host,
        port=port,
        log_level="warning",
        reload=False,
    )
    server = uvicorn.Server(config)
    server.run()


def wait_for_server(url, timeout=15):
    """Espera a que el servidor esté listo."""
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.1)
    return False


def run_webview():
    """Lanza la ventana PyWebView."""
    import webview

    url = f"http://127.0.0.1:{PORT}"

    # Iniciar servidor en hilo de fondo
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    print(f"Iniciando SuperAstro en {url} ...")
    wait_for_server(url + "/")

    window = webview.create_window(
        title="SuperAstro",
        url=url,
        width=1280,
        height=820,
        min_size=(900, 600),
        resizable=True,
    )
    webview.start(debug=False)


def run_server_only():
    """Solo levanta el servidor (modo --server)."""
    print(f"SuperAstro API corriendo en http://127.0.0.1:{PORT}")
    print(f"Docs: http://127.0.0.1:{PORT}/docs")
    uvicorn.run(
        "api.app:app",
        host="127.0.0.1",
        port=PORT,
        log_level="info",
        reload=True,
    )


def run_dev_browser():
    """Lanza servidor y abre el navegador del sistema."""
    import webbrowser

    url = f"http://127.0.0.1:{PORT}"
    t = threading.Thread(target=lambda: uvicorn.run(
        "api.app:app", host="127.0.0.1", port=PORT,
        log_level="info", reload=True,
    ), daemon=True)
    t.start()

    print(f"Esperando servidor en {url}...")
    if wait_for_server(url + "/"):
        webbrowser.open(url)
        print(f"SuperAstro abierto en: {url}")
    else:
        print("El servidor tardó demasiado en iniciar.")

    # Mantener vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SuperAstro launcher")
    parser.add_argument("--server", action="store_true", help="Solo FastAPI (modo dev con reload)")
    parser.add_argument("--dev",    action="store_true", help="FastAPI + navegador del sistema")
    parser.add_argument("--port",   type=int, default=PORT, help=f"Puerto (default: {PORT})")
    args = parser.parse_args()

    PORT = args.port

    if args.server:
        run_server_only()
    elif args.dev:
        run_dev_browser()
    else:
        run_webview()
