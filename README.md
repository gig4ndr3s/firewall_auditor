# Firewall Security Auditor & Backup Tool
![python](https://www.readmecodegen.com/api/social-icon?name=python)
![dotenv](https://www.readmecodegen.com/api/social-icon?name=dotenv)
![cisco](https://www.readmecodegen.com/api/social-icon?name=cisco)
![fortinet](https://www.readmecodegen.com/api/social-icon?name=fortinet)
![paloaltonetworks](https://www.readmecodegen.com/api/social-icon?name=paloaltonetworks)

**Automatización de tareas repetitivas y auditoría básica de seguridad para firewalls perimetrales.**

Este proyecto es un script desarrollado en **Python** utilizando la librería `netmiko` para conectarse de forma segura (SSH) a dispositivos de red (Firewalls/Routers). Su objetivo es automatizar dos de las tareas más comunes en un equipo de Seguridad Perimetral:

1. **Backup Automatizado:** Descarga y guarda la configuración actual del equipo con un sello de tiempo (timestamp), asegurando que siempre hay un punto de restauración antes de un cambio de red.
2. **Auditoría de Reglas (Compliance):** Parsea el archivo de configuración descargado en busca de malas prácticas de seguridad, específicamente detectando reglas permisivas críticas como las políticas "Any-Any" (`permit ip any any`).

## Tecnologías Utilizadas
* **Python 3.x**
* **Netmiko:** Para la gestión de conexiones SSH con equipos de red multimarca.
* **Dotenv:** Para la carga segura de credenciales mediante variables de entorno, evitando exponer contraseñas en el código fuente.

## Caso de Uso
Ideal para entornos de **Centro de Operaciones de Red (NOC)** o equipos de **Ingeniería Perimetral (Nivel 1 / Nivel 2)** donde se requiere verificar la postura de seguridad de un firewall tras ventanas de mantenimiento o implementaciones de nuevas arquitecturas.

Esto no deja de ser un proyecto personal con motivos de aprendizaje. Para un verdadero uso de forma profesional habría que extender las funciones de auditoría ya que este script solo confirma normas muy generales.
