# from curses import window
from Resource import Resource
from UserInterface import UserInterface
from CommunicationNode import CommunicationNode
from sys import argv
from ErrorGenerator import ErrorGenerator

if __name__ == '__main__':
    given_port = int(argv[1])

    ErrorGenerator = ErrorGenerator(udp_error_rate=0.0, broken_connection_rate=0.0)
    communication_node = CommunicationNode(port=given_port, error_generator=ErrorGenerator)
    communication_node.start_broadcasting()
    communication_node.start_communication()
    window = UserInterface(
        communication_node,
        f'Node: {given_port}',
        'White',
        f'node_{given_port}_downloads'
    )
    window.update()
    window.mainloop()
    window.quit()
    exit(0)