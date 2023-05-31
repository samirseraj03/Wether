import json
import pymongo
from datetime import *


def path_datos():
    return ("D:/DAM INFORMATICA/ACCES DE DADES/UF1/ACTIVITAT7/1/datos.json")

def path_precios():
    return ("D:/DAM INFORMATICA/ACCES DE DADES/UF1/ACTIVITAT7/1/precios.json")

def is_list_empty(list):
    # chekear la lista si esta vacia
    # entrada de lista
    # salida si esta vacia o esta llena
    if len(list) == 0:
        return True
    return False

def path_database():
    return pymongo.MongoClient(host = "mongodb+srv://mserajdam:<Aref1310>@projecte1.lvx9vsy.mongodb.net/?retryWrites=true&w=majority",
                              port=27017,
                             username="mserajdam",
                             password="Aref1310")

# def deploy_places():
#     data_base = path_database().gestio_parking
#     for i in range (1 , 48):        
#         data_base['Places'].insert_one({'plaza' : f'{i}' , 'ocupado' : 'NO'})


# def deploy_prices():
#     data_base = path_database().gestio_parking
#     price = 0.05
#     for i in range (1 , 13):
#         if i < 10:
#             data_base['Prices'].insert_one({'mes' : f'0{i}' , 'precio' : f'{round(price , 2)}'})
#         else : data_base['Prices'].insert_one({'mes' : f'{i}' , 'precio' : f'{round(price , 2)}'})
#         price += 0.02
#     path_database().close

def deploy_collection():  
    path_database().get_database('Wehter')
    path_database().Wehter.create_collection('inici')  


# def busqueda_vechiculo():  
#     datos = json.loads(open(path_datos()).read())
#     sortir = False
#     while (sortir == False):
#         matricula = input("introdeuix la matricula de la teva cotxe: ")
#         for informacion_vhiechulo in datos['vehicles']:
#             if informacion_vhiechulo ['matricula'] == matricula and comprovar_salida_coche(matricula) == 'dintre':
#                 return informacion_vhiechulo
#         if sortir != True:
#             print ("no se ha econtrado tu matricula en el aparcamento, vuelve a introducir")

# def busqeuda_precio_mes():
#     '''la busqeuda obtiene los precios coincidendo con el mes que estamos hoy en dia''' 
#     datos = json.loads(open(path_precios()).read())
#     datos = dict(datos)

#     #llamada de tiempo de ahora
#     ahora_buscar_mes = ahora() 
#     #obtener el mes de la fecha que estamos ahora
#     mes = ahora_buscar_mes.strftime('%m')
#     #busqeuda de precio a partir del mes que estamos
#     for i in datos['prices']:
#         if i[5:] == mes:
#             precio = (datos['prices'][i]['car'])
#             precio_min = precio['up_to_1_min']
#             break
#     return precio_min
            
def printmenu():
    '''imprimir un menu de la salida de parking'''
    print ("\n")
    print('hoy: ', ahora())
    print("has de seleccionar 1 o 2 o 3")
    print("1. Quan ha estat en el aparcament")
    print("2. Quan ha de pagar en total")
    print("3. Informacio dels preus")
    print("4. Sortir del menu")
    print()

# def ahora():
#     '''la funcion devuelve la fecha de ahora en formato de date
#     , se puede hacer calcuclo con la funcion'''    
#     var = str(datetime.now().replace(microsecond=0))
#     return datetime.strptime(var, '%Y-%m-%d %H:%M:%S')

def ahora():
    '''la funcion devuelve la fecha de ahora en formato de date
    , se puede hacer calcuclo con la funcion'''    
    var = str(date.today())
    #print (var)
    return var
    #print (date.strftime(var, '%Y-%m-%d'))
    #return date.strftime(var, '%Y-%m-%d')



def data_entrada(tiempo_entrada):
    '''convertir una fecha de string a tipo data'''
    return datetime.strptime( tiempo_entrada , '%Y-%m-%d')


def solo_data(tiempo):
    '''convierte el tiempo a solo data,
    se debe asginar una variable a la funcion para que de efecto'''
    data = (tiempo.replace(hour=0, minute=0, second=0, microsecond=0))
    data = tiempo.strftime('%Y-%m-%d')
    return data

def obtener_informacion_precios():
    '''la informacion devuelve en un dict los precios de cada mes'''
    
    datos = json.loads(open(path_precios()).read())
    datos = dict(datos)
    lista = []
    count = 1
    for i in datos['prices']:
        precio = (datos['prices'][i]['car'])
        precio_min = precio['up_to_1_min']
        lista.append({'mes ' + str(count) : str(precio_min) + '€'})
        count += 1
    return lista

# def comprovar_salida_coche(datos_matricula):
#     '''comprovar el coche si esta dentro o fuera'''
    
#     datos = json.loads(open(path_datos()).read())
#     datos = dict(datos)
#     datos_matricula_Comprovar = str(datos_matricula)
#     for i in datos['vehicles']:
#         if datos_matricula_Comprovar == i['matricula']:
#             comprovar = i['estado']
#             break            
#     return comprovar


def cambiar_estado(matricula):
    
    datos = json.loads(open(path_datos()).read() )
    
    estado = 'fuera'
    for i in datos['vehicles']:
        if matricula == i['matricula']:
            i['estado'] = 'fuera'
    with open (path_datos() , 'w') as guardar_archivo:
        json.dump(datos , guardar_archivo , indent=4)


# if __name__ == "__main__":
#     Salida_grande = False

#     while Salida_grande == False:
#         datos = busqueda_vechiculo()
#         print ("se encontro el la matricula de " , datos)
#         opcio_main = 0
#         salir = False
#         while opcio_main!=5 and salir == False:       
#             printmenu()
#             tiempo_entrada = datos['timestamp']

#             opcio=int(input())

#             if opcio == 1:   
                
#                 print("el tiempo que has estado en el parking es de  : "  , ahora() - data_entrada(tiempo_entrada))
#                 print("\n")

#             elif opcio == 2:
#                 precio = busqeuda_precio_mes()
#                 dias_en_aparcamiento = ahora() - data_entrada(tiempo_entrada)
#                 minutos = int(dias_en_aparcamiento.total_seconds() / 60)
#                 print ("has de pagar: " , minutos * precio , "€")
#                 cambiar_estado(datos['matricula'])
                
                

#             elif opcio == 3:
#                 print (obtener_informacion_precios())
#                 print("\n")
            
#             elif opcio == 4:
#                 print ("has salido, gracies per la teva visita")
#                 salir = True

#             else:
#                 print ("introduce una opcion que sea valida entre 1 y 3")