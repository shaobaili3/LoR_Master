from PyQt5.QtCore import QThread
import zmq
import json

class UIThread(QThread):
    def __int__(self):
        super().__init__()
        self.ui = None

    def run(self):
        port = "9621"
        
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % port)
            
        while True:
            #  Wait for next request from client
            message = socket.recv()
            print("Received request: ", message)
            # time.sleep(3) #  Immediately send the data to avoid receive message stuck
            jsonStr = json.dumps(self.ui.__dict__)
            socket.send(str(jsonStr).encode('ascii'))