# Birrapp
Subject: "Sistemas Distribuidos" - "Distributed Systems"
Authors: Javier Barroso Canto,	Jorge Gutiérrez Vila, [Yefry Manuel Pallarés Núñez](https://github.com/Jeffresh)

Description:
Our program makes a zeromq conversation with the client, he makes a request to the server and the server ask the worker. The worker, with threads, will produce an array with data from social network Twitter and it will generate some graphics that will be stored in Google Drive and an excel file that will be available only for Google Drive's admin. 

Nuestro programa se resume en una conversación zeromq en el que el cliente hace una petición al servidor y éste se la remite al worker. Éste, mediante hilos, generará un vector con datos extraídos de Twitter y, cuando acaben todos, se generará una gráfica que será almacenada en Drive (cuya url se le pasará al cliente) y un excel solo visible por el administrador del Google Drive. Se pueden ver las salidas en la presentación.

Set up:
	1) 	Run server.py and wait for "Servidor preparado" (Server ready)
	2) 	Run worker.py and wait for "Worker preparado" (Worker ready)
	1) 	Run client.py and pass an argue (alemanas, espanolas, americanas, belgas) (German, Spanish, Americans, Belgian)
	
Forma de lanzarlo:
	1)	Correr el server.py y esperar a Servidor preparado
	2) 	Correr el worker.py y esperar a Worker preparado
	3)	Correr el client.py y pasar un parámetro de estudio (alemanas, espanolas, americanas, belgas)

Note: In first try, it will generate some credentials in a Desktop file.

Nota: En la primera ejecución, se generará las credenciales necesarias, las cuales se almancenarán automáticamente en un fichero en el escritorio.
