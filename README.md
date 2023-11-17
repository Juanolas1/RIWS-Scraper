# RIWS-Scraper

## Configuraciones básicas

Antes de ejecutar el proyecto, hay que prepara las siguientes configuraciones:

### Scrapy

1. Es necesario tener instalado la librería `user_agent` y `elasticsearch` y `scrapyelasticsearch` en python.
 
2. En las líneas 112 y 113, del fichero [settings.py](https://github.com/Juanolas1/RIWS-Scraper/blob/1a16d3d5c8990e6ff198843b7391037506628f60/scrapperjuegos/scrapperjuegos/settings.py#L112), hay que cambiar el usuario y contraseña con los valores de tu Elasticsearch para que se indexen de manera correcta los datos.

```
ELASTICSEARCH_USERNAME = "elastic"              # Reemplaza con tu nombre de usuario de Elasticsearch
ELASTICSEARCH_PASSWORD = "VjcT4+K6O9FWc8lJO=hp" # Reemplaza con tu contraseña de Elasticsearch
```

3. Arrancar spider de instant-gaming:

```
scrapy crawl instant-gaming
```

4. Arrancar spider de GOG:

```
scrapy crawl gog  
```

### Elasticsearch

No permite hacer correctamente el intercambio de recursos entre su base de datos y la web cuando realiza las peticiones, devolviendo un error de **CORS** (*Cross-Origin Resource Sharing*). Este error se puede solucionar de la siguiente manera:

Permitir dentro del contenedor de Elasticsearch en el fichero `/usr/share/elasticsearch/config/elasticsearch.yml` y posteriormente realizar un reinicio.

```
http.cors.enabled: true
http.cors.allow-origin: "*"
```

### Web

Se ha realizado utilizando el framework "Angular", por lo que hay que tener instalado Angular y Node.js para su correcto funcionamiento.

 - Instalación de Angular:

    `npm install -g @angular/cli`

 - Levantar la web:

    `ng serve --open`
  
 - Dentro del fichero `/scrapperweb/scrapperweb/src/app/app.component.ts` es necesario especificar, en la parte de "Authorization", el usuario y contraseña de tu servidor de Elasticsearch ("usuario:contraseña"), para poder realizar las peticiones.

```
const headers = new HttpHeaders({
    'Authorization': 'Basic ' + btoa('elastic:VjcT4+K6O9FWc8lJO=hp'),
    'Content-Type': 'application/json'
});
```
