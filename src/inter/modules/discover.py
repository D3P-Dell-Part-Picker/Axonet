import os
import sys
import secrets
import src.server.inject as inject

this_dir = os.path.dirname(os.path.realpath(__file__))

os.chdir(this_dir)

def initiate(net_tuple):
    """ Called from the network injector when it receives a $discover: flag"""
    os.chdir(this_dir)

    op_id = secrets.token_hex(8)
    print("Discover -> Info: Initiating peer discovery (ring --> mesh bootstrapping stage 1)")

    injector = inject.NetworkInjector()
    injector.broadcast("vote:discovery-"+op_id, net_tuple)


def respond_start(net_tuple, op_id, cluster_rep):
    """Called by the client's listener_thread after the 'discovery' election is complete"""

    print('Current directory: '+this_dir)

    os.chdir(this_dir)
    if cluster_rep:
        injector = inject.NetworkInjector()
        injector.broadcast("newpage:"+op_id, net_tuple)  # Create a pagefile to store peer addresses in
        injector.broadcast("sharepeers:"+op_id, net_tuple)  # Instruct nodes to append peer addresses to this pagefile


def start(net_tuple, op_id, cluster_rep):
    """Called after addresses are written to page [op-id] """

    from src.client.client import Client
    _client = Client()

    # Synchronise discovered addresses across distributed filesystem...
    if cluster_rep:
        print("!?!?!?!?! We are cluster rep!!!")
        _client.broadcast(_client.prepare("fetch:" + op_id + ":discovery"), do_mesh_propagation=False)

