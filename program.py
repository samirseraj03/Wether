import requests
from funcions import *
import os
import datetime

#mostrar imagen 
import pandas as pd
import json
from staticmap import StaticMap , IconMarker , CircleMarker


client = path_database()
data_base = client.Wehter


def check_exist_database():
    #Fem que una variable, guardi els noms de les coleccións de la base de dades 
    #si existeix retornem True perque surti sino desplega la coleccio finalment fa una altre volta per sortir.
    while (True):
        dbnames = client.list_database_names()
        #print (dbnames)
        if 'Wehter' in dbnames:
                return True
        else :
                deploy_collection()

def check_exist_collection():
    '''chekear si existe collecion de hoy sino busca en api'''
    collection = client.Wehter.list_collection_names()
    if str(ahora()) in collection:
        return True
    else:
        search_api()



def list_country(option):
    '''opciones de para listar cuidades '''
    if option == 1:
        girona = ["Salt","Girona","Quart","Banyoles",]
        return girona
    elif option == 2:
        barcelona = ["Sant Cugat del Vallès","Barcelona","Mataró","Badalona"]
        return barcelona
    elif option == 3:  
        lleida = ["la Bordeta","Lleida","Alpicat","Torrefarrera"]
        return lleida
    elif option == 4:
        tarragona = ["Tarragona","Reus","La Canonja","Mont-roig"]
        return tarragona


def consult_api(country):
    '''consulta de api'''
    api_key="6885ca183cdf5a80102910cd67d9ff7a"
    parametros={"q":f"{country}","mode":"json","units":"metric","APPID":api_key}
    r=requests.get("http://api.openweathermap.org/data/2.5/weather",params=parametros)
    r.status_code
    r.url
    r.json()
    datos=r.json()
    return datos

def search_api():
    '''consulta de api y hacer un update '''
    for y in range (1 ,5):
        for i in list_country(y):       
            update_database(consult_api(i + ",ES"))

def update_database(datos):
    '''hacer update i insertat a la base de datos'''
    data_base[f"{ahora()}"].insert_one(datos)

def menu():
    lista = [
                "1. Introduir les ciutats d'on es vol consultat la temperatura",
                "2. Consultar les temperatures a la web de OpenWeatherMap",
                "3. Llistar les temperatures de totes les ciutats",
                "4. Llistar les temperatures d'una ciutat entre dues dates",
                "5. Generar un mapa de les tempertaures con iconos"
            ]
    print ()
    for i in lista:
        print (i)

def consult_country():
    '''consultar las cuidades que estan en las provincias , consulta a la funcion countrylist'''
    print ()
    lista = ["1. girona" , "2. barcelona" , "3. lleida" , "4. tarragona"]
    for i in lista:
        print (i)
    option = int (input ("Tria la provincia que vols consultar: "))
    print ()
    for i , y in enumerate(list_country(option) , 1):
        print (str(i)+". "+str(y))
    country = int (input ("Tria la la cuitat que vols consultar la temperatura: "))
    countries = list_country(option)
    return countries[country - 1]

def consult_temperature_database(country  , print_ = 0 , hour = ahora() ):
    '''hacer consultas a la base de datos , puedes con print o sin print poniendo 1 para imprimir''' 
    if print_ == 0:
        return data_base[f'{hour}'].find_one({"name" : f"{country}"})
    elif print_ == 1:
       document = data_base[f'{hour}'].find_one({"name" : f"{country}"})
       print (f"{country} te una tempertura de : {document['main']['temp']} ºC")
       print ()


if __name__ == "__main__":
    while (True):
        input ("pulsa Qualsevol teclat... ")
        try:
        
            check_exist_database()
            check_exist_collection()
            menu()

            option = int(input("tria: "))
            if (option == 1):
                while True:
                    try:
                        consult_temperature_database(consult_country() , 1)
                        break
                    except: 
                        print ("no se ha encontrado ") 
                        break
                
            elif option == 2:
                while True:
                    try:
                        option = input ("Quina cuitat vols consultar: ")
                        datos = consult_api(option)
                        print()
                        print (f"{datos['name']} te una tempertura de {datos['main']['temp']} ºC \n")
                    except:
                        print ("no se ha encontrado la cuidad")
                        break

            elif option == 3:
                print ()
                for listed_country in range (1 , 5):
                    count = 1
                    for i in list_country(listed_country):            
                        document = consult_temperature_database(i)
                        if count % 2 == 0:
                            print (f"{str(document['name'])}: {document['main']['temp']}ºC \n")
                        else : print (f"{str(document['name'])}: {document['main']['temp']}ºC" , end= " -||- ")
                        count += 1
                print ()
                    
                    
            elif option == 4:
                try:
                    country = consult_country()        
                    print ("nota: la data es compara entre la data de avui !!")
                    print ("|||   la data ha de ser de aquest format : 2023-05-13       |||")
                    print ("|||   pots fer nomes click per comparar amb la data de ahir |||")
                    print ("|||          Nomes hi ha registres desde 2023-05-11         |||")
                    data = input("per quina data els vols comparar: ")

                    if data == "":
                        data = data_entrada(ahora()) - datetime.timedelta(days=1)
                        data = solo_data(data)
                        
                    document_not_today = consult_temperature_database(country , 0 , data)
                    document_today = consult_temperature_database(country , 0)
                    print (f"la tempertura entre aquesta data {data} es : {document_not_today['main']['temp']}ºC i avui {document_today['main']['temp']}ºC")
                except: print ("ha habido un error")
                
            elif option == 5:
                try:
                    print ()
                    print ("nota: la data es compara entre la data de avui !!")
                    print ("|||   la data ha de ser de aquest format : 2023-05-13       |||")
                    print ("|||   pots fer nomes click per mostrar amb la data de avui  |||")
                    print ("|||   pots posar 'ahir' per mostrar el mapa de data ahir    |||")
                    print ("|||          Nomes hi ha registres desde 2023-05-11         |||")
                    print ()
                    data = input("per quina data els vols comparar: ")

                    if data == "ahir":
                        data = data_entrada(ahora()) - datetime.timedelta(days=1)
                        data = solo_data(data)
                    if data == "":
                        data = ahora()

                    document = data_base[f'{data}'].find()

                    listdict = []
                    for i in document:
                        add = {'name' : f"{i['name']}" , "temp" : f"{i['main']['temp']}"  , "lon" : f"{i['coord']['lon']}" , 'lat' : f"{i['coord']['lat']}" , 'weather' : f"{i['weather'][0]['main']}" , 'icon' : f"{i['weather'][0]['icon']}"  }
                        listdict.append(add)
                
                    with open("./data.json","w",encoding="utf8") as outfile:
                        json.dump(listdict , outfile , indent=4)
                    outfile = open("./data.json","r",encoding="utf8")
                    datos = json.load(outfile)

                    df = pd.DataFrame.from_records(datos)
                    m_bcn = StaticMap(600, 600)
                    
                    for index, row in df.iterrows():
                        if row['weather'] == "Clouds":
                            marker = IconMarker([float(row['lon']) , float(row['lat'])] , './fotos_tiempo/nublado.png' , 5 ,25 )
                        elif row['weather'] == "Rain":
                            marker = IconMarker([float(row['lon']) , float(row['lat'])] , './fotos_tiempo/lluvia.png' ,5 ,25 )
                        elif row['weather'] == "Clear":
                            marker = IconMarker([float(row['lon']) , float(row['lat'])] , './fotos_tiempo/soleado.png' ,5 ,25 )
            
                        m_bcn.add_marker(marker)
                    image = m_bcn.render() 
                    image.save('./map.png')
                    ruta = os.getcwd()
                    print ("pots consultar la mapa desde aqui : " ,  ruta + '\map.png') 
                except : print ("ha habido un error")
                
            else:
                print ("no existeix tal opcio , torna a triar")
        except: print ("no existe opcion")
            

