# info de la materia: 
 ST0263 Topicos de Telematica
# Estudiante(s): 
 Juan Sebastian Camacho, jscamachop@eafit.edu.co
# Profesor: 
# Edwin Nelson Montoya, emontoya@eafit.brightspace.com
# nombre del proyecto, lab o actividad
Reto #1 Telematica
# 1. breve descripción de la actividad
La actividad esta centrada en la implementacion de una red P2P descentralizada utilizando diferentes tecnologías de comunicación entre nodos, como API REST y gRPC. Esta comunicacion entre los nodos debe permitir la transferencia eficiente de archivos. La red debe estar diseñada para funcionar sin servidores centralizados o superpeers, en este caso cada nodo desempeña el rol de cliente y servidor
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Primero se logro que la arquitectura del trabajo fuera descentralizada, cada nodo era cliente y servidor lo que ayudaba a que no tuviera que haber un superpeer o un servidor. Aparte de esto la comunicacion entre los nodos se logro exitosamente con API REST, los nodos pueden descubrirse mutuamente y compartir informacion como el ip utilizando API REST. Los nodos intercambiaron actualizaciones de peers, y se verificó que cada nodo pudiera mantener una lista actualizada de peers activos en la red.
Tambien se logro exitosamente la configuracion de varios nodos en la red, cada uno con su propio archivo de configuracion que incluye informacion sobre la direccion IP, puerto gRPC y directorio compartido. Se hizo un poco de manejo de errores  con mensajes para facilitar la identificacion de problemas durante el codigo. Se definio un archivo .proto que describe la transferencia de archivos y los mensajes necesarios.
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Si bien la arquitectura que se realizo cumple hasta cierta parte los requisitos, no se logro la arquitectura ideal de CHORD, se intento pero siempre se tuvo problemas con la fingertable y nunca se dieron las conexiones entre los nodos.
Si bien antes mencione que se hizo una buena implementacion del archivo .proto, la conectividad gRPC para la simulacion de transferencia de archivos tuvo un grande error y por eso no fue efectiva, la verdad no se de que fue el error, pero diria que puede ser por el puerto
# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
## Info general: 
El reto implementa una arquitectura de red P2P con servicios de transferencia de archivos mediante gRPC
## Arquitectura 
### Red P2P:
Cada nodo en la red actúa como un peer, sin un servidor centralizado que controle las comunicaciones. Los nodos pueden conectarse entre sí, descubrirse mutuamente y mantener una lista de peers activos.
### Servicios Distribuidos: 
La arquitectura está distribuida, con servicios desplegados en cada nodo que permiten la comunicación y la transferencia de archivos entre los peers.
## Patrones de diseño  
### Singleton: 
Se asegura que cada nodo gestione su propia instancia única de cliente P2P y servidor, evitando problemas de estado compartido en la red distribuida.
### Factory Method: 
Utilizado para crear las instancias del servidor gRPC y REST, asegurando que las configuraciones específicas de cada nodo se respeten.
### Observer:
Implementado de manera implícita en la forma en que los nodos actualizan su lista de peers. Cuando un nodo descubre un nuevo peer, notifica a los otros nodos para que actualicen su lista.
## Mejores practicas aplicadas
### Desacoplamiento de Componentes: 
La funcionalidad del servidor REST y gRPC se mantiene separada, lo que facilita la escalabilidad y el mantenimiento. Cada servicio tiene responsabilidades claras y limitadas.}
### Manejo de Errores:
Se implementaron mecanismos para manejar errores comunes en redes P2P, como la falta de disponibilidad de un peer o la desconexión inesperada de un nodo.
### Uso de gRPC para Transferencias de Archivos: 
gRPC es preferido sobre REST para transferir archivos debido a su eficiencia en la transmisión de datos binarios y su soporte para streaming, lo que mejora el rendimiento y la confiabilidad en la red P2P.
# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
## Lenguaje de programacion:
 Todo el proyecto está desarrollado en Python 3.10, un lenguaje de alto nivel que es ampliamente utilizado en el desarrollo de aplicaciones distribuidas, redes y sistemas de scripting. Python ofrece una amplia gama de bibliotecas y herramientas que facilitan el desarrollo de aplicaciones de red.
## librerias: 
gRPC (grpcio)
gRPC Tools (grpcio-tools)
Protobuf (google,protobuf)
Flask
Requests
Concurrent Futures
Signal
Json
Time
## como se compila y ejecuta.
Lo primero es instalar todas las librerias necesarias con pip
Ya luego viene la compilacion del archivo protobuf (config.proto), tienes que ejecutar este comando en el mismo directorio donde tienes el archivo config.proto: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. config.proto. Este comando va a generar 2 arcchivos .PY que son necesarios para que el gRPC funcione correctamente en Python
Luego sigue la configuracion de cada nodo, antes de los comandos tienes que asegurar que tengas los 3 archivos de configuraron .json
ya al momento de ejecutar los comandos para ver el codigo seria: python main.py --config=configX.json, siendo X el numero del archivo, si es el nodo 1 entonces seria config1
Para la transferencia de archivos simplemente corres el archivo  simulate_files de la siguiente forma: python simulate_files.py
## detalles del desarrollo.
### Definición del Protocolo (config.proto):
Se definieron mensajes y servicios para la transferencia de archivos (UploadRequest, DownloadRequest) y para la administración de peers (UpdatePeersRequest).
Implementación de Servidores y Clientes gRPC:
Se creó una clase servidora en p2p_server.py que implementa los métodos definidos en el .proto para manejar la subida y descarga de archivos.
### Actualización Dinámica de Peers:
Los nodos se comunican entre sí para actualizar sus listas de peers en tiempo real. Este proceso es manejado mediante solicitudes REST entre los nodos.
### Depuración y Pruebas:
Durante el desarrollo, se agregaron mensajes de depuración para rastrear el estado de las conexiones y las transferencias de archivos.
Se realizaron pruebas para asegurar que los nodos pudieran conectarse entre sí, actualizar sus listas de peers y simular correctamente la transferencia de archivos.
Estos son los aspectos principales del desarrollo del proyecto y la implementación del sistema de red P2P con gRPC en Python.
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambente, parámetros, etc)
La mayoria de las cosas para el proyecto vienen configuradas con el archivo .json, donde esta toda la informacion de cada uno de los nodos
## opcionalmente - si quiere mostrar resultados o pantallazos 
LINK DEL VIDEO: https://eafit-my.sharepoint.com/:v:/g/personal/jscamachop_eafit_edu_co/EXHvVHmhLJdGuNZPbNFhvrYBqpG8zZOd4XMP83ni1YMGGA?referrer=Teams.TEAMS-ELECTRON&referrerScenario=MeetingChicletGetLink.view
# IP o nombres de dominio en nube o en la máquina servidor.
Esto lo tendre mas adelante
## como se lanza el servidor.
tambien lo tendre mas adelante (explicacion en los comentarios finales)
# 5. otra información que considere relevante para esta actividad.
Profe yo soy la persona que le escribio por el tema de AWS, entonces todavia no he podido montar el reto a la plataforma, yo le escribi un correo y en verdad le queria pedir el favor si me podia volver a meter al curso para subirlo a AWS
# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto
