# Elasticsearch

Testeando **elasticsearch**

## Instalación

Se instaló de la página oficial la versión 8.7 de **elasticsearch** para Linux, además de instalar la versión para Python 3.8.10.

**config/elasticsearch.yml**

```yml
cluster.routing.allocation.disk.threshold_enabled: true
cluster.routing.allocation.disk.watermark.flood_stage: 200mb
cluster.routing.allocation.disk.watermark.low: 500mb
cluster.routing.allocation.disk.watermark.high: 300mb
xpack.security.enabled: false
```

## Dejamos activo el servicio de elasticsearch

```bash
./bin/elasticsearch
```

## Ejecutamos

Crear el índice, y leer los archivos de **data** para indexarlos.

```bash
python3 ./create.py
```

Buscar en las palabras **(query)** utilizando **highlight** (esto retorna el texto "cercano" a la palabra buscada)

```bash
python3 ./search our_query_to_search
python3 ./search Audifonos
```
