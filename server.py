#!/usr/bin/python2

import zmq
import os
import tweepy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import tkinter
import pickle
import time
import paginas_drive.classy as gs


proyecto_1 = gs.drive() # instancia drive abstrae el drive. Esta variable es esencial para comunicarse con el drive,
#actualizar las paginas, subir archivos, obtener urls.

hoja=proyecto_1.nueva_hoja("Birras") # se crea la hoja donde se actualizaran las paginas.
proyecto_1.nueva_pagina("Birras","Españolas",6,2)
proyecto_1.nueva_pagina("Birras","Alemanas",4,2)
proyecto_1.nueva_pagina("Birras","Belgas",3,2)
proyecto_1.nueva_pagina("Birras","Americanas",3,2)
proyecto_1.nueva_pagina("Birras","Todas",16,2)


def server():
    # Set up the zeromq context and REP socket
    context = zmq.Context(1)
    sock = context.socket(zmq.REP) # REP
    sock.bind('tcp://*:4545')

    # Conection with worker
    worker = context.socket(zmq.REQ) # PUSH
    worker.bind("tcp://*:4546")
  
    # Start the server loop
    while True:
        # Recieve the option and we set the location of the file to serve
        msg = sock.recv()
        msg = msg.decode("utf-8")
        print("Campo de estudio: " , msg)
        if(msg == "espanolas" or msg == "americanas" or msg == "belgas" or msg == "alemanas"):
            worker.send_string(msg)
            url = worker.recv() 
            url = url.decode("utf-8")
            print("url: " + url)
 
        else:
            url = "Error."

        # We share the path and we end comunications
        sock.send_string(url, zmq.SNDMORE)
        sock.send_string("fin")
            

if __name__ == '__main__':
    print("Servidor preparado")
    server()
