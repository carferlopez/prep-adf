"""
Servidor Web Local y Red Wi-Fi para el Sistema de Test Adaptativo ADIF OEP 2026.
- Escucha en 0.0.0.0:8826 (ThreadingHTTPServer) para permitir acceso simultáneo desde Mac y Móvil (iPhone/Android).
- Incluye recarga en caliente automática de motor_adaptativo.py y detección de IP local para código QR móvil.
"""

from __future__ import annotations

import importlib
import json
import mimetypes
import socket
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import motor_adaptativo as motor

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
APP_SIGNATURE = "ADIF_OEP_2026_TRAINER"
DEFAULT_PORT = 8826
_ACTIVE_PORT = DEFAULT_PORT
_MOTOR_MTIME = (BASE_DIR / "motor_adaptativo.py").stat().st_mtime


def _ensure_fresh_motor() -> None:
    global _MOTOR_MTIME
    try:
        current_mtime = (BASE_DIR / "motor_adaptativo.py").stat().st_mtime
        if current_mtime != _MOTOR_MTIME:
            importlib.reload(motor)
            _MOTOR_MTIME = current_mtime
    except Exception:
        pass


def obtener_ip_local() -> str:
    """Obtiene la IP en la red Wi-Fi local (ej. 192.168.x.x) para conectarse desde el móvil."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


class OposicionRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _serve_file(self, filepath: Path) -> None:
        if not filepath.exists() or not filepath.is_file():
            self.send_error(404, "Archivo no encontrado")
            return
        mime, _ = mimetypes.guess_type(str(filepath))
        content_type = mime or "application/octet-stream"
        if content_type.startswith("text/") or content_type in ("application/javascript", "application/json"):
            content_type += "; charset=utf-8"
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        bloque = qs.get("bloque", ["PERFIL_GESTION"])[0]
        documento = qs.get("documento", ["TODOS"])[0]

        if path == "/api/app-id":
            self._send_json({"app": APP_SIGNATURE})
            return

        if path == "/api/info-movil":
            ip_lan = obtener_ip_local()
            hostname = socket.gethostname()
            self._send_json(
                {
                    "ip_lan": ip_lan,
                    "puerto": _ACTIVE_PORT,
                    "url_movil": f"http://{ip_lan}:{_ACTIVE_PORT}",
                    "url_bonjour": f"http://{hostname}:{_ACTIVE_PORT}",
                }
            )
            return

        if path == "/" or path == "/index.html":
            self._serve_file(STATIC_DIR / "index.html")
            return

        if path.startswith("/static/"):
            rel = path.removeprefix("/static/")
            safe_path = (STATIC_DIR / rel).resolve()
            if str(safe_path).startswith(str(STATIC_DIR.resolve())):
                self._serve_file(safe_path)
                return
            self.send_error(403, "Acceso denegado")
            return

        if path == "/api/estado":
            _ensure_fresh_motor()
            self._send_json(motor.obtener_estado_global(bloque, documento))
            return

        if path == "/api/siguiente-pregunta":
            _ensure_fresh_motor()
            self._send_json(motor.obtener_siguiente_pregunta(bloque, documento))
            return

        self.send_error(404, "Ruta no encontrada")

    def do_POST(self) -> None:
        _ensure_fresh_motor()
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", "0"))
        body_bytes = self.rfile.read(length) if length > 0 else b"{}"

        try:
            payload = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            self._send_json({"error": "JSON inválido"}, status=400)
            return

        if path == "/api/responder":
            pregunta_id = int(payload.get("pregunta_id", 0))
            opcion_elegida = int(payload.get("opcion_elegida", -1))
            resultado = motor.registrar_respuesta_y_ramificar(pregunta_id, opcion_elegida)
            self._send_json(resultado)
            return

        if path == "/api/sincronizar":
            res = motor.sincronizar_carpetas_adif()
            bloque = str(payload.get("bloque", "PERFIL_GESTION"))
            documento = str(payload.get("documento", "TODOS"))
            estado = motor.obtener_estado_global(bloque, documento)
            self._send_json({"sincronizacion": res, "estado": estado})
            return

        if path == "/api/configurar-key":
            api_key = str(payload.get("api_key", "")).strip()
            motor.guardar_api_key(api_key)
            self._send_json({"ok": True, "tiene_api_key": bool(motor.obtener_api_key())})
            return

        if path == "/api/diagnostico-feynman":
            import coach_feynman
            api_key = motor.obtener_api_key()
            if not api_key:
                self._send_json({"error": "No has configurado tu API Key de Gemini. Añádela arriba a la derecha."}, status=400)
                return
            try:
                reporte = coach_feynman.generar_diagnostico_feynman(api_key)
                self._send_json({"markdown": reporte})
            except Exception as e:
                self._send_json({"error": f"Error al generar diagnóstico: {str(e)}"}, status=500)
            return

        self._send_json({"error": "Endpoint desconocido"}, status=404)

    def log_message(self, format: str, *args) -> None:
        return


def _check_existing_adif_server(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/app-id", timeout=0.8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("app") == APP_SIGNATURE
    except Exception:
        return False


def _is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def run_server(preferred_port: int = DEFAULT_PORT, open_browser: bool = True) -> None:
    global _ACTIVE_PORT
    motor.init_db()
    ip_lan = obtener_ip_local()

    for candidate in range(preferred_port, preferred_port + 15):
        if not _is_port_free(candidate):
            if _check_existing_adif_server(candidate):
                _ACTIVE_PORT = candidate
                url = f"http://127.0.0.1:{candidate}"
                print(f"Entrenador ADIF OEP 2026 ya activo en Mac: {url}")
                print(f"Acceso desde tu Móvil (Wi-Fi): http://{ip_lan}:{candidate}")
                if open_browser:
                    webbrowser.open(url)
                return
            continue

        _ACTIVE_PORT = candidate
        server = ThreadingHTTPServer(("0.0.0.0", candidate), OposicionRequestHandler)
        url = f"http://127.0.0.1:{candidate}"
        print(f"Entrenador Oficial ADIF OEP 2026 activo en Mac: {url}")
        print(f"📱 Para abrir en tu Móvil (conectado al mismo Wi-Fi): http://{ip_lan}:{candidate}")
        if open_browser:
            webbrowser.open(url)
        server.serve_forever()
        return


if __name__ == "__main__":
    run_server()
