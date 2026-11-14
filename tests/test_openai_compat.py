import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lessongen.llm import OpenAICompatLLM  # noqa: E402


def test_openai_compat_roundtrip():
    seen = {}

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen["path"], seen["auth"], seen["body"] = self.path, self.headers["Authorization"], body
            out = json.dumps({"choices": [{"message": {"content": "hello"}}]}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(out)

        def log_message(self, *a): pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    llm = OpenAICompatLLM(f"http://127.0.0.1:{srv.server_port}/v1", "KEY123")
    assert llm.complete("generator", "sys", "usr", "m1") == "hello"
    srv.shutdown()
    assert seen["path"] == "/v1/chat/completions" and seen["auth"] == "Bearer KEY123"
    assert seen["body"]["messages"][0] == {"role": "system", "content": "sys"}
