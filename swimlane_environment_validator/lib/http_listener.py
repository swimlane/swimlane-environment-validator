#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = log_handler.setup_logger()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{ "status" : "ok" }', 'utf-8'))

    def log_message(self, format, *args):
        return

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def serve_on_port(port):
    logger.info("Starting http listener on {}...".format(port))

    try:
        server = ThreadingHTTPServer(("",port), Handler)
        server.serve_forever()
    except:
        logger.error('Couldnt start listener on port {}, is something already listening? Ports below 1024 can only be spawned by root.'.format(port))

def start_lb_listener_threads():
    for port in config.LB_CONNECTIVITY_PORTS:
        thread = Thread(target=serve_on_port, args=[port])
        thread.daemon = True
        thread.start()

def start_intra_cluster_listener_threads():

    for listener in config.INTRA_CLUSTER_PORTS:
        listener_thread = Thread(target=serve_on_port, args=[listener])
        listener_thread.daemon = True

        listener_thread.start()
