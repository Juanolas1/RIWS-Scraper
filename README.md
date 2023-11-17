# RIWS-Scraper

## Configuraciones básicas

Antes de ejecutar el proyecto hay que prepara las siguientes configuraciones:

1. Scrapy
- Es necesario tener instalado la librería de "user agent", el elasticsearch de python, en las líneas 112 y 113 de la configuración hay que poner el usuario y contraseña de tu Elasticsearch para que se indexen de manera correcta los datos.

  ```
    ELASTICSEARCH_USERNAME = "elastic"  # Reemplaza con tu nombre de usuario de Elasticsearch
    ELASTICSEARCH_PASSWORD = "VjcT4+K6O9FWc8lJO=hp"  # Reemplaza con tu contraseña de Elasticsearch

Arrancar spider de instant-gaming:

  ```
    scrapy crawl instant-gaming
  ```
    
Arrancar spider de GOG:

  ```
    scrapy crawl gog  
  ```
  

2. Elasticsearch
- Elasticsearch no permite hacer correctamente el intercambio de recursos entre su base de datos y la web cuando realiza las peticiones, devolviendo un error de CORS (Cross-Origin Resource Sharing). Este error se puede solucionar de la siguiente manera:
    
  Permitir dentro del contenedor de Elasticsearch en el fichero "/usr/share/elasticsearch/config/elasticsearch.yml" y posteriormente realizar un reinicio.


  ```
    http.cors.enabled: true
    http.cors.allow-origin: "*"
  ```

2. Web
- La web se ha realizado utilizando el framework "Angular" por lo que hay que tener instalado Angular y Node para el correcto funcionamiento.


  Instalación de Angular:
    
  
  ```
    npm install -g @angular/cli
  ```

  Levantar la web:

  ```
    ng serve --open
  ```
  
  Dentro del fichero "scrapperweb\src\app\app.component.ts" para poder realizar las peticiones es necesario especificar en la parte de "Authorization" el usuario y la contraseña de tu servidor de Elasticsearch (formato "usuario:contraseña").
  
  ```
    const headers = new HttpHeaders({
      'Authorization': 'Basic ' + btoa('elastic:VjcT4+K6O9FWc8lJO=hp'), 
      'Content-Type': 'application/json'
    });
  ```











