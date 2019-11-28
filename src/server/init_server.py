# Python 3.6.2
# Script automating the starting of the client individually.

from src.server.server import Server
port = 3705


def init(network_architecture="complete"):
    x = Server()
    x.initialize(port=port, network_architecture=network_architecture, method="socket",
                 listening=True, network_injection=True, default_log_level="Debug",
                 modules=["corecount"])


if __name__ == "__main__":
    init(network_architecture="mesh")
