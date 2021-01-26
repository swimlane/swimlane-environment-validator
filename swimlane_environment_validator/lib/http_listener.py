#!/usr/bin/env python3
import lib.config as config
import lib.log_handler as log_handler

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

def start_listener_threads():
    k8s_thread = Thread(target=serve_on_port, args=[config.arguments.k8s_port])
    web_thread = Thread(target=serve_on_port, args=[config.arguments.web_port])
    spi_thread = Thread(target=serve_on_port, args=[config.arguments.spi_port])
    
    k8s_thread.daemon = True
    web_thread.daemon = True
    spi_thread.daemon = True

    k8s_thread.start()
    web_thread.start()
    spi_thread.start()

    return {
        'k8s' : k8s_thread,
        'web' : web_thread,
        'spi' : spi_thread
    }
