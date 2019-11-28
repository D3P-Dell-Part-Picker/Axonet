# Python 3.6.2
# Script automating the starting of the client individually.
# Initialize the client
from src.client.client import Client
port = 3705


def init(network_architecture):
    x = Client()
    x.initialize(port=port, net_architecture=network_architecture, remote_addresses=None,
                 command_execution=True, default_log_level="Debug", modules=["corecount"],
                 net_size=9)


if __name__ == "__main__":
    init("mesh")
