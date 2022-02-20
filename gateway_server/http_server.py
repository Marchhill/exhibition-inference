from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from datetime import datetime
import json
import database.database_main as db


# Reference: https://stackoverflow.com/a/22238613/7254995
def datetime_json_encoder(o):
  if isinstance(o, datetime):
    return o.isoformat()
  raise TypeError(f"Object of type {type(o)} is not JSON serializable")


class RequestHandler(BaseHTTPRequestHandler):
  def _set_success_headers(self):
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()

  def _set_failure_headers(self, err_code):
    self.send_response(err_code)
    self.end_headers()

  # curl localhost:8000/query
  def do_GET(self):
    if self.path != "/query":
      self._set_failure_headers(404)
      return

    self._set_success_headers()

    cnx = db.connect("delta_admin", "deltapw_admin")
    results = db.prototype_query(cnx)
    cnx.close()

    self.wfile.write(
      json.dumps({
        "status": "success", 
        "data": json.dumps(results, default=datetime_json_encoder)
      }).encode("utf-8")
    )

  # Reference: https://gist.github.com/nitaku/10d0662536f37a087e1b
  # curl -d '{"i":"2", "t":"2022-02-20T16:13:19.244900", "x":"12.3", "y":"5.88", "z":"1.0", "q":"98.9"}' -H "Content-Type: application/json" -X POST localhost:8000/submit
  def do_POST(self):
    if self.path != "/submit":
      self._set_failure_headers(404)
      return
    
    incoming_content_type, _ = cgi.parse_header(self.headers.get("content-type"))
    if incoming_content_type != "application/json":
      self._set_failure_headers(400)
      return
    
    incoming_data = json.loads(self.rfile.read(int(self.headers.get("Content-Length"))).decode("utf-8"))
    
    if len(incoming_data.keys()) != 6 or set(incoming_data.keys()) != {"i", "t", "x", "y", "z", "q"}:
      self._set_success_headers()
      self.wfile.write(
        json.dumps({
          "accepted": False,
          "reason": "malformed incoming JSON"
        }).encode("utf-8")
      )
      return
    
    cnx = db.connect("delta_uwb", "deltapw_uwb")
    accepted = db.insert_into_tag_data(
      cnx, 
      tagId=incoming_data["i"],
      ts=incoming_data["t"],
      x=incoming_data["x"],
      y=incoming_data["y"],
      z=incoming_data["z"],
      quality=incoming_data["q"]
    )
    cnx.close()

    self._set_success_headers()
    self.wfile.write(
      json.dumps({
        "accepted": accepted
      }).encode("utf-8")
    )
    

def main():
    PORT = 8000
    server = HTTPServer(("localhost", PORT), RequestHandler)
    print(f"Server running on port {PORT}")
    server.serve_forever()


if __name__ == "__main__":
  main()