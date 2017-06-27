import zmq
import os
import tweepy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import tkinter
import pickle
import paginas_drive.classy as gs

from threading import Thread
from time import sleep

consumer_key = "Q6HMq78yGu7nQ9t4pR82Yt9Yu"
consumer_secret = "JgqpWE6CJLubR63d7JyVy6U0qT71mmp1lw4hHLQgN91ZxfIZVo"
access_key = "851710799458512896-xuJBrzWyGQaB0PxYYM5HW8KZWigcKCl"
access_secret = "pDz6r47N4fSUAD6su6ouU9aIMu4ORq4LFY0RxwWMc7VSO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

my_tweets = api.user_timeline()
tweets = api.home_timeline()

num_tweets = 10
num_retweets = 0
contador = 0
vector = []
vector_esp = []
vector_ale = []
vector_bel = []
vector_ame = []
limpia_vector = []


def espanolas():
    return vector_esp;

def alemanas():
    return vector_ale;

def belgas():
    return vector_bel;

def americanas():
    return vector_ame;

# ---------------------------------------------- tipos de datos que usa Jeff


vec = []
#matriz = np.empty(shape=[0,2], dtype=np.str)
cervezas = ['#Cruzcampo','#EstrellaGalicia','#Mahou','#Amstel','#EstrellaDamm','#VollDamm','#Franziskaner','#Paulaner',
                '#Becks','#Erdinger','#LeffeBlond','#laChouffe','#AffligemBlonde','#Budweiser','#Coronita','#Molson']

proyecto_1 = gs.drive() # instancia drive abstrae el drive. Esta variable es esencial para comunicarse con el drive,
#actualizar las paginas, subir archivos, obtener urls.

hoja=proyecto_1.abrir_hoja("Birras") # se crea la hoja donde se actualizaran las paginas.

# --------------------------------------------------------------------------

# map the inputs to the function blocks
options = {"espanolas" : espanolas(),
           "alemanas" : alemanas(),
           "belgas" : belgas(),
           "americanas" : americanas(),
}

def contar_retweets(consulta, vector):
    results = api.search(q=consulta)
    tweets = 8
    num_retweets = tweets  
    for result in results:
        if(tweets > 0):
            num_retweets = num_retweets + result.retweet_count
            tweets = tweets - 1 
    
    vector.append(consulta)
    vector.append(num_retweets)


def crear_archivos(vector, msg):
    lista = []

    j=0
    size = int(len(vector)/2)
    lista.append(('Cerveza', 'Retweets'))

    for i in range(0, size):
        lista.append((vector[j], vector[j+1]))
        j += 2

    array = np.asarray(lista)

    df = pd.DataFrame(data=array[1:, 1], index=array[1:, 0], columns=array[0, 1:], dtype=int)


    grafica=df.plot.barh(figsize=(12,6));
    fig = grafica.get_figure()
    figure_name = "grafica_" + msg + ".jpeg"
    fig.savefig(figure_name)

    file = proyecto_1.subir_archivo(figure_name,"Imagen")
    url = proyecto_1.get_url_documento(file)
    return url

def vector_to_matrix(vector, matriz):
    
    iterator = 0
    for i in range(16):
        matriz = np.append(matriz,[[vector[iterator][1:],vector[iterator+1]]], axis=0)
        iterator +=2
    

    return matriz

def rellenar_vectores(matriz):
    list_mat = matriz.tolist()
    print(list_mat)

    for i in range (16):
        for j in range(2):
            if i < 6:
                vector_esp.append(list_mat[i][j])
            if i >5 and i < 10:
                vector_ale.append(list_mat[i][j])
            if i >10 and i <13:
                vector_bel.append(list_mat[i][j])
            if i >13:
                vector_ame.append(list_mat[i][j])

def actualizar_drive():

    vect= []
     # se obtiene los nombres y los rt
    for cerveza in cervezas:
        contar_retweets(cerveza,vec)

    # los pasa a la matriz que necesito para rellenar el excel
    matriz = np.empty(shape=[0,2], dtype=np.str)

    matriz = vector_to_matrix(vec,matriz)


    Españolas = proyecto_1.abrir_pagina("Birras","Españolas")
    proyecto_1.actualizar_pagina(matriz[0:6], Españolas)

    Alemanas = proyecto_1.abrir_pagina("Birras","Alemanas")
    proyecto_1.actualizar_pagina(matriz[6:10], Alemanas)

    Belgas = proyecto_1.abrir_pagina("Birras","Belgas")
    proyecto_1.actualizar_pagina(matriz[10:13], Belgas)

    Americanas = proyecto_1.abrir_pagina("Birras","Americanas")
    proyecto_1.actualizar_pagina(matriz[13:], Americanas)

    pagina_todas = proyecto_1.abrir_pagina("Birras","Todas")
    proyecto_1.actualizar_pagina(matriz, pagina_todas)
    
    
def tarea_espanol():
    contar_retweets("#Cruzcampo", vector_esp)
    contar_retweets("#EstrellaGalicia", vector_esp)
    contar_retweets("#Mahou", vector_esp)
    contar_retweets("#Amstel", vector_esp)
    contar_retweets("#EstrellaDamm", vector_esp)
    contar_retweets("#VollDamm", vector_esp)

def tarea_aleman():
    contar_retweets("#Franziskaner", vector_ale)
    contar_retweets("#Paulaner", vector_ale)
    contar_retweets("#Becks", vector_ale)
    contar_retweets("#Erdinger", vector_ale)

def tarea_belga():
    contar_retweets("#LeffeBlond", vector_bel)
    contar_retweets("#LaChouffe", vector_bel)
    contar_retweets("#AffligemBlonde", vector_bel)

def tarea_americano():
    contar_retweets("#Budweiser", vector_ame)
    contar_retweets("#Coronita", vector_ame)
    contar_retweets("#Molson", vector_ame)
    

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.REP) 
receiver.connect("tcp://localhost:4546")


# Process tasks forever
while True:
    print("Worker preparado")
    # Worker starts working by receiving the msg from server
    msg = receiver.recv(4096).decode("utf-8")

    print("Actualizando datos...")
    thread_drive = Thread(target = actualizar_drive, args = ())
    thread_esp = Thread(target = tarea_espanol, args = ())
    thread_ale = Thread(target = tarea_aleman, args = ())
    thread_bel = Thread(target = tarea_belga, args = ())
    thread_ame = Thread(target = tarea_americano, args = ())
    
    thread_drive.start()

    thread_esp.start()
    thread_ale.start()
    thread_bel.start()
    thread_ame.start()

    thread_esp.join()
    thread_ale.join()
    thread_bel.join()
    thread_ame.join()
    
    thread_drive.join()
    print("Datos actualizados")

    vector = options[msg]
    url = crear_archivos(vector, msg)
    print("Archivo creado")
    receiver.send_string(str(url))

    num_tweets = 10
    num_retweets = 0
    contador = 0
    vector = []
    vector_esp = []
    vector_ale = []
    vector_bel = []
    vector_ame = []
