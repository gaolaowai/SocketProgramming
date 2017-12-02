#!/usr/bin/python

import socket
import signal
import time

class Server:

 def __init__(self, port = 80):
     self.host = ''
     self.port = port 
     self.www_dir = 'www' # Directory where webpage files are stored
    
  
 def server_start(self):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try: # user provided in the __init__() port may be unavaivable
         print("Trying to launch server on ", self.host, ":",self.port)
         self.socket.bind((self.host, self.port)) 
         
     except Exception as e:
         print ("Failed to bind to port:",self.port,"\n")
         print ("Trying 8080 or other specified port instead")
         user_port = self.port 
         self.port = 8080
         
         try:
             print("Trying to bind to host/port: ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))
             
         except Exception as e:
             print("ERROR: Failed to bind to port: ", user_port, " and 8080. ")
             self.shutdown()
             import sys
             sys.exit(1)
            
     print ("Server started on port: ", self.port)
     self.server_wait()
 
 def make_response_headers(self, code):
     
     # determine response code
     header = ''
     if (code == 200):
        header = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        header = 'HTTP/1.1 404 Not Found\n'
     
     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) 
     header += 'Date: ' + current_date +'\n'
     header += 'Server: Roll-A-Server\n'
     header += 'Connection: close\n\n'

     return header

 def shutdown(self):   
     try:
         svr.socket.shutdown(socket.SHUT_RDWR)
         
     except Exception as e:
         print("Encountered error while closing socket: ",e)

 def server_wait(self):
     while True:
         print ("Server successfully started.\nCurrently listening for connections.")
         self.socket.listen(5) # maximum number of queued connections
         
         conn, addr = self.socket.accept()
         #conn ---> socket to client
         #addr ---> clients address
	############ Getting requests   ##################
         print("Received connection request from:", addr)         
         string = conn.recv(1024).decode()        
         #determine request method  (HEAD and GET are supported)
         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         print ("Request body: ", string)

	########### Interpretting and handling ############
         if (request_method == 'GET') | (request_method == 'HEAD'):

             file_requested = string.split(' ')
             file_requested = file_requested[1]
    	     # NO CGI is implemented. Discard any attempts to pass params.
             file_requested = file_requested.split('?')[0]  
     
             if (file_requested == '/'):
                 file_requested = '/index.html'             

             file_requested = self.www_dir + file_requested
             print ("Serving web page [",file_requested,"]")

             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):  #only read the file when GET
                     response_content = file_handler.read() 
                       
                 file_handler.close()
                 
                 response_headers = self.make_response_headers(200)          
                 
             except Exception as e:
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self.make_response_headers(404)
             
                 if (request_method == 'GET'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"  
                 
             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content

             conn.send(server_response)
             print ("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)

############### End of server class #######################

def shutdown_signal(sig, dummy):
    svr.shutdown()
    import sys
    sys.exit(1)



###########################################################
#shut down server on ctrl+c
signal.signal(signal.SIGINT, shutdown_signal)

print ("Starting web server")
svr = Server(80)  # Pass desired port number; if not specified, will default to 80
svr.server_start()
    

