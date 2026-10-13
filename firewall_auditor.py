import os
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from dotenv import load_dotenv

# 1. Cargar credenciales de forma segura
load_dotenv()

FIREWALL = {
    'device_type': os.getenv('FW_TYPE', 'fortinet'),
    'host':        os.getenv('FW_IP'),
    'username':    os.getenv('FW_USER'),
    'password':    os.getenv('FW_PASS'),
    # 'global_delay_factor': 2, # Útil si el firewall responde lento
}

def backup_config(net_connect, hostname):
    # Descarga y guarda la configuración del firewall
    print(f"[*] Iniciando backup para {hostname}...")
    
    # El comando depende del fabricante.
    # Cisco: 'show running-config' | Fortinet: 'show' | Palo Alto: 'show config running'
    comando_backup = 'show' if 'fortinet' in FIREWALL['device_type'] else 'show running-config'
    
    output = net_connect.send_command(comando_backup)
    
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"backup_{hostname}_{fecha_actual}.txt"
    
    with open(nombre_archivo, 'w') as f:
        f.write(output)
        
    print(f"[+] Backup guardado exitosamente en: {nombre_archivo}")
    return nombre_archivo

def auditar_reglas(archivo_backup):
    # Analiza el archivo de configuración buscando malas prácticas
    print(f"[*] Auditando configuración de {archivo_backup}...")
    
    alertas = 0
    with open(archivo_backup, 'r') as f:
        lineas = f.readlines()
        
    for num, linea in enumerate(lineas, 1):
        linea_limpia = linea.strip().lower()
        
        # Ejemplo de auditoría básica: Buscar reglas que permitan todo (Any a Any)
        # La sintaxis exacta depende del firewall, esto es un concepto general.
        # Este es solo un ejemplo de auditoría sencilla, no sustituye a una auditoría real
      
        if "permit ip any any" in linea_limpia or ("set srcaddr all" in linea_limpia and "set dstaddr all" in linea_limpia):
            print(f"[!] ALERTA CRÍTICA: Regla 'Any-Any' detectada en la línea {num}: {linea.strip()}")
            alertas += 1
            
    if alertas == 0:
        print("[+] Auditoría finalizada: No se encontraron reglas 'Any-Any' evidentes.")
    else:
        print(f"[-] Auditoría finalizada con {alertas} alertas críticas.")

def main():
    print("=== Iniciando Script de Auditoría de Firewall ===")
    
    try:
        # 2. Conectar al dispositivo
        print(f"[*] Conectando a {FIREWALL['host']}...")
        with ConnectHandler(**FIREWALL) as net_connect:
            print("[+] Conexión SSH establecida.")
            
            # Obtener el nombre del dispositivo
            hostname = net_connect.find_prompt().strip('#> ')
            
            # 3. Hacer Backup
            archivo_generado = backup_config(net_connect, hostname)
            
            # 4. Auditar
            auditar_reglas(archivo_generado)
            
    except NetmikoAuthenticationException:
        print("[!] Error: Credenciales incorrectas.")
    except NetmikoTimeoutException:
        print(f"[!] Error: Tiempo de espera agotado. ¿El firewall en {FIREWALL['host']} está encendido y accesible por SSH?")
    except Exception as e:
        print(f"[!] Error inesperado: {e}")

if __name__ == "__main__":
    main()
