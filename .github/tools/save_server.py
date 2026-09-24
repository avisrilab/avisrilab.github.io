# Local-only helper: serves this folder and accepts one PNG upload, written to a fixed path.
import http.server, os, sys
OUT = sys.argv[1]  # absolute path of the single file this server may write
class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/save':
            self.send_error(404); return
        n = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(n)
        if not data.startswith(b'\x89PNG') or n > 5_000_000:
            self.send_error(400); return
        with open(OUT, 'wb') as f: f.write(data)
        self.send_response(200); self.end_headers(); self.wfile.write(b'saved %d bytes' % n)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
http.server.ThreadingHTTPServer(('127.0.0.1', 8766), H).serve_forever()
