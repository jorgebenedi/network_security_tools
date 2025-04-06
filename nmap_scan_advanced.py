import os
import sys
import time

class TextColor:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def switcher(opcion):
    if opcion == 1:  # SCAN COMPLETO -p- "todos los puertos"
        nmap_cadena = " -p- -A"
        return nmap_cadena
    elif opcion == 2:  # SCAN LIGHT
        nmap_cadena = " -T5 --top-ports 10"
        return nmap_cadena
    elif opcion == 3:  # SCAN HOST DISCOVERY
        nmap_query = " -sn"
        return nmap_query
    elif opcion == 4:  # SCAN VULN
        nmap_query = " --script vuln"
        return nmap_query
    elif opcion == 5:  # SCAN OS
        nmap_query = " -O"
        return nmap_query
    elif opcion == 6:  # SCAN VERSION
        nmap_query = " -sV"
        return nmap_query
    else:
        print("Opción no válida, regresando al menú principal...")
        return None 

def parser(modo, nmap_query, ip):
    print("-" * 50)
    print(f"Escaneando {ip} con consulta: {nmap_query}")

    results = os.popen(nmap_query).read()  
    if modo == 1 or modo == 2 or modo == 6: 
        print(results)
    elif modo == 3:  # Para el Host Discovery
        results = results.split("address (")
        if len(results) > 1:
            results = results[1].split(" ho")
            if results[0] == "1":
                print("El host se encuentra encendido")
            else:
                print("El host se encuentra apagado")
    elif modo == 4:  
        if "VULNERABILITY" in results:
            print("Vulnerabilidades encontradas: ")
            print(results)

def option(opcion, mode, modo):
    if opcion == 1:  
        print("Indique la IPv4")
        target = input("=> ")
        consulta = "nmap " + target + mode
        parser(modo, consulta, target)
    elif opcion == 2:
        print("Indica el nombre del archivo de texto con las IPs => [example: ips.txt]")
        archivo = input("=> ")
        try:
            with open(archivo, "r") as file:
                ips = file.read().splitlines()
            for ip in ips:
                if ip.strip():
                    consulta = "nmap " + ip + mode
                    parser(modo, consulta, ip)
                else:
                    print("Se saltó una línea vacía.")
        except FileNotFoundError:
            print(f"El archivo {archivo} no se encontró.")
    elif opcion == 3:  
        return False
    else:
        return False  

def main():
    while True:
        print(TextColor.RED + "Bienvenidos a NMAP by BLACK_CODE" + TextColor.RESET)
        time.sleep(1)
        print("Elige un modo de ejecución:")
        print(
            "[1]. Scan Completo\n[2]. Scan Light\n[3]. Host Discovery\n[4]. Scan Vuln\n[5]. Scan OS\n[6]. Scan Version\n[#]. Salir")
        try:
            modo = int(input("=> "))
            if modo == 7:  # Salir
                sys.exit()
            mode = switcher(modo)
            if mode is None:
                continue  
        except ValueError:
            print("Opción inválida. Por favor, ingresa un número del 1 al 6.")
            continue  

        time.sleep(1)
        print("-" * 50)
        print("Elige una opción para ingresar las IPs:\n[1]. IPv4\n[2]. Lista de IPs\n[3]. Regresar al menú principal")
        try:
            opcion = int(input("=> "))
            if opcion == 3:  # Opción para regresar al menú principal
                continue  # Esto hace que vuelva al principio del ciclo 'while'
            if not option(opcion, mode, modo):  # Procesar la opción
                continue  # Esto hace que vuelva al principio del ciclo 'while'
        except ValueError:
            print("Opción inválida. Por favor, ingresa un número del 1 al 2.")
            continue  # Regresar al ciclo para volver a intentarlo

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nFinalizando...")
        sys.exit()
