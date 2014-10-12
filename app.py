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

def timestamp():
  import datetime
  display = "%Y-%m-%d-%H-%M-%S"
  cur_time = datetime.datetime.now()
  cur_time = cur_time.strftime(display)
  return cur_time

def snap(rotation):
  global lock, cur_image
  if lock:
    return cur_image

  lock = True
  print "oh hi"
  from subprocess import call

  stamp = timestamp()
  call(["raspistill", "-o", "./snapshots/"+stamp+".jpg", "--rotation", rotation])
  cur_image = readfile(stamp+".jpg", True, "./snapshots/")
  lock = False
  return cur_image

dyn_routes = {'/snapshot': snap}

def parameter(name, path):
  from urlparse import urlparse
  query = urlparse(path).query
  for param in query.split("&"):
    p = param.split("=")
    if p[0]==name:
      return str(p[1])
  return ""

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()

    content = "Um.."

    path = self.path.split("?")[0]
    rotation = parameter("rotation", self.path)

    if path in static_routes:
      content = static_routes[path]

    if path in dyn_routes:
      content = dyn_routes[path](rotation)

    self.wfile.write(content)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

if __name__ == '__main__':
  server = ThreadedHTTPServer(('0.0.0.0', 8080), Handler)
  print 'Starting server. Hit ctl+c to stop.'
  server.serve_forever()
