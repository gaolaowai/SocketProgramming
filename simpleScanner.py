import socket

#########===**FUNCTIONS**===###########
def convPorts2Strings(portrange):
    bottom = int(portrange[0])
    top = int(portrange[1]) + 1)
    return bottom, top

def pscan(port):
    try:
        s.connect((server, port))
        return True
    except:
        return False
##############################


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = str(input("What host would you like to scan?\n"))
portrange = (input("What port range to scan? (i.e. \"1-500\").").split("-"))
base, top = convPorts2Strings(portrange)

for x in range(base, top):
    if pscan(x):
        print("Port {} is open".format(x))
        print("Received from port:\n", (s.recv(4092).decode()))
    else:
        print("Port {} is closed.".format(x))
