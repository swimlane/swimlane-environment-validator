#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

from threading import Thread
from flask import Flask
import click
import ssl

from OpenSSL import crypto, SSL

logger = log_handler.setup_logger()

app = Flask(__name__)

def serve_on_port(port):
    logger.info("Starting http listener on {}...".format(port))

    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return '{ "status" : "ok" }'


    # Silence the Flask development server logging
    if config.arguments.debug == False:
        def secho(text, file=None, nl=None, err=None, color=None, **styles):
            pass

        def echo(text, file=None, nl=None, err=None, color=None, **styles):
            pass

        click.echo = echo
        click.secho = secho

    try:
        app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
    except Exception:
        logger.error('Couldnt start listener on port {}, is something already listening? Ports below 1024 can only be spawned by root.'.format(port))
        logger.debug("Caught exception while starting listener thread ", exc_info=True)

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
