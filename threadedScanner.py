import socket
import threading
from queue import Queue

#########===**FUNCTIONS**===###########
def convPorts2Strings(portrange):
    bottom = int(portrange[0])
    top = (int(portrange[1]) + 1)
    return bottom, top

def pscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((server, port))
        with print_lock:
            print("Port {} is open!!!!".format(port))
            #print("Received from port:\n", (s.recv(4092).decode()))
        con.close()
    except:
        pass

def threader(): #This is essentially a task factory
    while True:
        worker = q.get()
        #print("PIcking up task for port {}\n".format(worker))
        pscan(worker)
        q.task_done()
##############setup Print_Lock and Queue################
print_lock = threading.Lock()
q = Queue()
##############################


### Start the threads as little daemons in the background which listen to the queue.
for x in range(100):  #This range value determines the number of threads
    t = threading.Thread(target=threader) #target = function being spun off into a thread
    t.daemon = True #Let it start and go into the background
    t.start()


server = str(input("What host would you like to scan?\n"))
portrange = (input("What port range to scan? (i.e. \"1-500\"):\n").split("-"))
base, top = convPorts2Strings(portrange)

for worker in range(base, top): #This determines the number of ports scanned
    #print("Pushing port {} to worker queue...\n".format(worker))
    q.put(worker)

#q.join()    #commenting this out returns prompt back to interpreter or exits to shell
