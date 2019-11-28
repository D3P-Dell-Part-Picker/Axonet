import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_dir)


def initiate(net_tuple, network_architecture, conn, no_prop):
    """ Called from the network injector when it receives a $[name]: flag"""
    from src.client.client import Client
    _client = Client()

    if network_architecture == "complete":
        _client.send(conn, no_prop + ':' + 'echo', sign=False)  # If received, send back
