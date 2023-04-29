from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")


# --- Crear almacenamiento en ES ---

print('────────  Creating index... ────────')
try:
    es.indices.create( # ···> Solo debe ejecutarse una vez
        index='db_scrapper',
        settings={
            "index": {
                "highlight": {
                    "max_analyzed_offset": 2_000_000 # <--- Esto es para limitar el tamaño del highlight
                }
            }
        }
    )
    print('Index created')

except Exception as e:
    print('Index already exists')



print('\n────────  Reading data... ────────')
# --- Lectura de archivos scrappeados
# - Ejemplo tenemos /data/falabella.html y /data/ripley.html ---

data = []
names = ['falabella', 'ripley']

for name in names:
    with open(f'data/{name}.html', 'r') as f:
        print('Reading file: ', name+'.html')
        data.append(f.read())



print('\n──────── Indexing data... ────────')
for i, name in enumerate(names):
    current_timestamp = datetime.now()
    print(f'Indexing: \n\tname: {name}.html \n\tid: {i} \n\thtml (length): {len(data[i])}\n\ttimestamp: {current_timestamp}') # backslash: \n
    es.index(index='db_scrapper', id=i, document={
        'name': name,
        'html': data[i],
        'timestamp': current_timestamp
    })
