from __future__ import print_function
import httplib2
import os
import gspread
import numpy as np
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

try:

    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



class drive:

    class hoja:
        def __init__(self):
            self.nombre = str()
            self.paginas = list()
            self.objeto = object()

    class documento:
        def __init__(self):
            self.nombre = str()
            self.formato = str()

    

    def __init__(self):
        
        self.get_credentials()
        self.lista_hojas = list()
        self.lista_documentos = list()
        
  
        
      

    def get_credentials(self):

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        SCOPES= ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/spreadsheets']
        
        CLIENT_SECRET_FILE = 'panojita.json'
        APPLICATION_NAME = 'Google Sheets API Python Quickstart'

        """Gets valid user credentials from storage.
            
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
        Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~/Escritorio/')
        credential_dir = os.path.join(home_dir, 'credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python.json')

        store = Storage(credential_path)
        credentials = store.get()
            
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME

            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)

            print('Storing credentials to ' + credential_path)


        """le da permisos a la API gspread para utilizar Drive"""
    
        self.gc = gspread.authorize(credentials)

        """Perimos para drive cloud"""
        self.http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive','v3',http=self.http)


    def subir_archivo(self, nombre_archivo,formato):
        archivo = self.documento()
        archivo.nombre = nombre_archivo
        archivo.formato = formato
        user_permission = {
    	    'type': 'anyone',
    	    'role': 'reader'}	


        #dir ="../"
        dir =nombre_archivo

        if formato == 'Documento':

            file_metadata = {'name' : nombre_archivo,'mimeType': 'application/vnd.google-apps.document'}

           
            media = discovery.MediaFileUpload(dir,
                                              mimetype='text/plain',resumable=True)
        else:

            file_metadata = {'name' : nombre_archivo, 'mimeType' : 'application/vnd.google-apps.document'}

            
        
            media = discovery.MediaFileUpload(dir,
                                          mimetype='image/jpeg',resumable=True)

        
        archivo = self.service.files().create(body=file_metadata,media_body=media,fields='id').execute()
        file_id = archivo.get('id')
        batch=self.service.new_batch_http_request()
        batch.add(self.service.permissions().create(fileId=file_id,body=user_permission,fields='id'))
        batch.execute()



        self.lista_documentos.append(nombre_archivo)

        return archivo


    def nueva_hoja(self, nombre_hoja):
        """crea una hoja y la añade a una lista de hojas"""
        hoja = self.hoja()
        hoja.nombre = nombre_hoja
        hoja.objeto = self.gc.create(nombre_hoja)
        hoja.paginas.append("Hoja 1")
        self.lista_hojas.append(hoja)
        return  self.abrir_hoja(nombre_hoja)

    def nueva_pagina(self, nombre_hoja ,nombre_pagina, n_fil, n_col):
        """crea una nueva pagina de una hoja"""
    
        
        for hojas in self.lista_hojas:
           if hojas.nombre == nombre_hoja:
               hojas.objeto.add_worksheet(title=nombre_pagina,rows=n_fil,cols=n_col)
               if hojas.paginas.count("Hoja 1")!= 0:
                   self.eliminar_pagina(nombre_hoja, "Hoja 1")

        return  self.abrir_pagina(nombre_hoja,nombre_pagina)
        
               
    

    def abrir_hoja(self, nombre_hoja):
        """Abre una hoja de calculo"""

        for hojas in self.lista_hojas:
            if hojas.nombre == nombre_hoja:
                hojas.objeto = self.gc.open(nombre_hoja)
                return hojas.objeto

        hoja = self.hoja()
        hoja.nombre = nombre_hoja
        hoja.objeto = self.gc.open(nombre_hoja)
        
        paginas = hoja.objeto.worksheets()

        for nombre in paginas:
            hoja.paginas.append(nombre.title)
        self.lista_hojas.append(hoja)
        
        # print(hoja.paginas)
        #print(hoja.objeto.id)
        return hoja.objeto
        

    def abrir_pagina(self, nombre_hoja, nombre_pagina):
        """Selecciona una pagina de la hoja de calculo"""

        hoja = self.abrir_hoja(nombre_hoja)
        
        worksheet = hoja.worksheet(nombre_pagina)

        for hojas in self.lista_hojas:
           if hojas.nombre == nombre_hoja and hojas.paginas.count(nombre_pagina)==0:
               hojas.paginas.append(nombre_pagina)

        return worksheet



    def actualizar_pagina(self, matriz,pagina):

        n_fil = matriz.shape[0]
        n_col = matriz.shape[1]

        cell_list = pagina.range(1,1,n_fil,n_col)
        
        for cell in cell_list:
            if cell.col == 1:
                cell.value = matriz[cell.row-1,0]

            else:
                cell.value = matriz[cell.row-1,cell.col-1]

        pagina.update_cells(cell_list)
            
    def eliminar_pagina(self, nombre_hoja, nombre_pagina):

        for hojas in self.lista_hojas:
            if hojas.nombre == nombre_hoja:
                    pagina = self.abrir_pagina(nombre_hoja,nombre_pagina)
                    hojas.objeto.del_worksheet(pagina)
                    ubicacion = hojas.paginas.index(nombre_pagina)
                    hojas.paginas.remove(nombre_pagina)
            

    def get_url_hoja(self, hoja):

        url = "https://docs.google.com/spreadsheets/d/" + hoja.id

        return url

    def get_url_documento(self, documento):
        url ="https://docs.google.com/document/d/"
        url+=str(documento.get('id'))
        # he modificado esto
        return url

    def def_public(self, hoja):
        hoja.share("None",perm_type="anyone",role="reader")

    def get_pagina(self, pagina):
    
        lista = pagina.get_all_values()
        return lista
  


   



  
        
