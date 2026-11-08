from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import ssl
ROOT = Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT/"repo"),**kwargs)
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","DENY")
        super().end_headers()
httpd=ThreadingHTTPServer(("127.0.0.1",8443),Handler)
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version=ssl.TLSVersion.TLSv1_2
ctx.load_cert_chain(str(ROOT/"localhost.pem"),str(ROOT/"localhost-key.pem"))
httpd.socket=ctx.wrap_socket(httpd.socket,server_side=True)
print("HTTPS https://localhost:8443/docs/visual/ (localhost only)",flush=True)
httpd.serve_forever()
