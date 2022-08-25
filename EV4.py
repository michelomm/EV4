import json
import time
import os
import requests
import conf

# GET https://IP_Sambox/api/aaaLogin.json
def obtener_token(usuario, clave):
    url = conf.sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": usuario,
                "pwd": clave
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    try:
        respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    except Exception as err:
        print("Error al consumir el API por problema de conectividad")
        exit(1)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return token

# GET https://IP_Sambox/apic-ip-address/api/class/topSystem.json
def top_system():

    # Limpiar pantalla para monitoreo limpio
    def limpiar_print():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    limpiar_print()

    cabecera = {
        "Content-Type": "application/json"
    }
    clavetoken = {
        "APIC-Cookie": obtener_token(conf.usuario, conf.clave)
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(conf.sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=clavetoken, verify=False)
    total_nodos = int(respuesta.json()["totalCount"])

    print("Cantidad de dispositivos conectados: " + respuesta.json()["totalCount"])

    for i in range(0, total_nodos):
        ip_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["address"]
        name = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["name"]
        mac = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["fabricMAC"]
        estado = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["state"]
        uptime = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["systemUpTime"]

        print("Nombre: " + name + "\t" + "\t" +
              "|    IP Address: " + ip_local + "   " + "\t" +
              "|    MAC Address: " + mac + "\t" + "\t" +
              "|    Estado: " + estado + "\t" + "\t" +
              "|    Tiempo de actividad: " + uptime)

#Generar un bucle de consulta cada 60 segundos
while True:
    try:
        top_system()
        time.sleep(60)
    except KeyboardInterrupt:
        print("  >>Ha finalizado el programa<<  ")
        exit(1)


top_system()
