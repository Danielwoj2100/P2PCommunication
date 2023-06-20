# from curses import window
from Resource import Resource
from UserInterface import UserInterface
from CommunicationNode import CommunicationNode

cn = CommunicationNode(port=1026)
cn.start_communication()
cn.add_resource(Resource(name="er2.txt", data=bytearray([0, 0, 0, 0])))
window = UserInterface(cn, 'server 26 p2p', 'White')
window.update()
# cn2.sendResource(resource1, '127.0.0.1', 10001)

window.mainloop()

# POPRAWIĆ PORTY ALBO IP NWM
