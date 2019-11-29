# Python 3.6.2
# Script automating the starting of the server individually.

port = 3705


def init(network_architecture="complete"):
    from server import Server

    x = Server()
    x.initialize(port=port, network_architecture=network_architecture, method="socket",
                 listening=True, network_injection=True, default_log_level="Debug",
                 modules=["corecount"])


if __name__ == "__main__":
    init(network_architecture="mesh")
