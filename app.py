from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

def readfile(name, binary=False, base="./pub/"):
  mode = "r"
  if binary:
    mode = "rb"
  return file(base+name, mode).read()

template = readfile("index.htm")
icon = readfile("favicon.png", True)
css = readfile("styler.css")
blank = readfile("blank1600x1200.gif")
js = readfile("script.js")

static_routes = { '/favicon.ico': icon, "/": template, "/styler.css": css, "/blank": blank, "/script.js": js }

lock = False
cur_image = blank
def snap():
  global lock, cur_image
  if lock:
    return cur_image

  lock = True
  print "oh hi"
  from subprocess import call
  import datetime
  display = "%Y-%m-%d-%H-%M-%S"
  timestamp = datetime.datetime.now()
  timestamp = timestamp.strftime(display)
  print timestamp

  call(["raspistill", "-o", "./snapshots/"+timestamp+".jpg"])
  cur_image = readfile(timestamp+".jpg", True, "./snapshots/")
  lock = False
  return cur_image

dyn_routes = {'/snapshot': snap}


class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()

    content = "Um.."

    path = self.path.split("?")[0]

    if path in static_routes:
      content = static_routes[path]

    if path in dyn_routes:
      content = dyn_routes[path]()

    self.wfile.write(content)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

if __name__ == '__main__':
  server = ThreadedHTTPServer(('0.0.0.0', 8080), Handler)
  print 'Starting server. Hit ctl+c to stop.'
  server.serve_forever()
