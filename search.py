from elasticsearch import Elasticsearch
from datetime import datetime
# Importamos sys para poder recibir argumentos desde la terminal
import sys

# --- Verificamos que el largo de los argumentos sea el correcto ---
if len(sys.argv) != 2:
    print("Error, debe ingresar un argumento")
    sys.exit()



# --- El argumento será el query ---
query = sys.argv[1]
# --- Conexión a Elasticsearch ---
es = Elasticsearch("http://localhost:9200")



# --- Posible conexión para recibir el query ---


query = {
    "match": {
        "html": query,
    },
}


highlight = {
    "fields": {
        "html": {
            "type": "unified",
        },
    },
}



# --- Información de la respuesta (sin highlight) ---

# resp['hits]['hits']
# └─ ['_index', '_id', '_score', '_ignored', '_source']
#                                                └─ ['name', 'html', 'timestamp']
#


# --- Buscar información almacenada ---
print("───────── Buscando información ─────────")
resp = es.search(index="db_scrapper", query=query, highlight=highlight)
print("Got %d Hits:" % resp['hits']['total']['value'])
print("Keys from resp: ", resp.keys())
print("Keys from resp['hits']: ", resp['hits'].keys(), "\n")
print("───────── Respuesta ─────────")

for hit in resp['hits']['hits']:
    # print(hit.keys()) # verificamos que tenemos 'highlight'
    # Mostramos el highlight ( Elementos encontrados )
    print(f"───────── Highlight: {hit['_source']['name']} ─────────")
    print("Tamaño del highlight: ", len(hit['highlight']['html']))
    for i, element in enumerate(hit['highlight']['html']):
        print(f'Elemento {i}: ', element)
    print("\n")