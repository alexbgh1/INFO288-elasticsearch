# Elasticsearch

Testeando **elasticsearch**

## Instalación

Se instaló de la página oficial la versión 8.7 de **elasticsearch** para Linux, además de instalar la versión para Python 3.8.10.

Se agregó a la configuración el siguiente contenido, referente a espacio de utilización y seguridad desactivada.

**config/elasticsearch.yml**

```yml
cluster.routing.allocation.disk.threshold_enabled: true
cluster.routing.allocation.disk.watermark.flood_stage: 200mb
cluster.routing.allocation.disk.watermark.low: 500mb
cluster.routing.allocation.disk.watermark.high: 300mb

xpack.security.enabled: false
```

## Dejamos activo el servicio de elasticsearch

**DEFAULT PORT: 9200**

**PATH: elasticsearch-8.7.0**

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

## Links te utilidad

Elasticsearch [installation for Linux](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)

Elasticsearch [security settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html)

Elasticsearch [Highlights config](https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html)

Stackoverflow [low-disk-watermark](https://stackoverflow.com/questions/33369955/low-disk-watermark-exceeded-on)

[Gist example configuration](https://gist.github.com/zsprackett/8546403)
