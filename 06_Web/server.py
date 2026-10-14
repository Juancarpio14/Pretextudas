"""Prototipo LOCAL: descarga, contactos SQLite y configuración sin dependencias."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import sqlite3, json, os, re, time
from urllib.parse import urlparse
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
DB = BASE / 'datos' / 'contactos.sqlite3'
DB.parent.mkdir(exist_ok=True)
DB.parent.chmod(0o700)
def connect():
    con = sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, marketing INTEGER NOT NULL, requested_at TEXT NOT NULL, consent_version TEXT NOT NULL)')
    return con
with connect(): pass
DB.chmod(0o600)
CONFIG = json.loads((BASE / 'config.json').read_text())
HITS = {}
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Do not log names, emails, request bodies or query strings.
        pass
    def send(self, status, data, mime='application/json; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        self.end_headers(); self.wfile.write(data)
    def answer(self, status, value):
        self.send(status,json.dumps(value,ensure_ascii=False).encode())
    def do_GET(self):
        path=urlparse(self.path).path
        if path == '/api/config':
            self.answer(200,CONFIG); return
        if path == '/health':
            self.answer(200,{'status':'ok','mode':'local-prototype'});return
        files={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/privacidad':'privacidad.html','/guia.pdf':'../04_Material_workshop/Pretextuda_Cuaderno_Workshop.pdf'}
        if path not in files:
            self.answer(404,{'error':'No encontrado'});return
        file=BASE/files[path]
        mime='application/pdf' if path=='/guia.pdf' else ('text/javascript; charset=utf-8' if path.endswith('.js') else 'text/css; charset=utf-8' if path.endswith('.css') else 'text/html; charset=utf-8')
        self.send(200,file.read_bytes(),mime)
    def do_POST(self):
        if self.path != '/api/contacts':
            self.answer(404,{'error':'No encontrado'});return
        origin=self.headers.get('Origin')
        if origin and origin not in {f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}:
            self.answer(403,{'error':'Origen no autorizado'});return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=4096:raise ValueError()
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':raise ValueError()
            data=json.loads(self.rfile.read(n))
            if not isinstance(data,dict):raise ValueError()
            name=data.get('name',''); email=data.get('email',''); marketing=data.get('marketing',False)
            if not isinstance(name,str) or not isinstance(email,str) or type(marketing)!=bool:raise ValueError()
            name=name.strip();email=email.strip().lower()
            if not 1<=len(name)<=100 or any(ord(c)<32 for c in name):raise ValueError()
            if len(email)>254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):raise ValueError()
            if data.get('privacy') is not True:raise ValueError()
            if data.get('website'):raise ValueError()
        except (ValueError,TypeError,json.JSONDecodeError):
            self.answer(400,{'error':'Revisa nombre, correo y aviso de privacidad.'});return
        key=self.client_address[0];now=time.time()
        HITS[key]=[t for t in HITS.get(key,[]) if now-t<60]
        if len(HITS[key])>=15:
            self.answer(429,{'error':'Espera un minuto antes de volver a intentar.'});return
        HITS[key].append(now)
        timestamp=datetime.now(timezone.utc).isoformat()
        with connect() as con:
            # A new explicit choice replaces old consent, including withdrawal.
            con.execute('INSERT INTO contacts(name,email,marketing,requested_at,consent_version) VALUES(?,?,?,?,?) ON CONFLICT(email) DO UPDATE SET name=excluded.name, marketing=excluded.marketing, requested_at=excluded.requested_at, consent_version=excluded.consent_version',(name,email,int(marketing),timestamp,'pretextuda-local-v1'))
        self.answer(200,{'ok':True,'download':'/guia.pdf','message':'Consulta guardada. Reservas y pagos aún no están activos; este prototipo no envía correos.'})

if __name__=='__main__':
    port=int(os.environ.get('PRETEXTUDA_PORT','8000'))
    print(f'Pretextuda: prototipo local en puerto {port}. Ctrl+C para detener.',flush=True)
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
