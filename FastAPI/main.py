# FastAPI
from fastapi import FastAPI, Query
# Elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
# Others
import os
import glob

app = FastAPI()
es = Elasticsearch("http://localhost:9200")
DB_NAME = 'db_scrapper'

def create_index():
    try:
        es.indices.create( # ···> Solo debe ejecutarse una vez
            index=DB_NAME, # ···> db_scrapperDB_NAME
            settings={
                "index": {
                    "highlight": {
                        "max_analyzed_offset": 2_000_000 # <--- Esto es para limitar el tamaño del highlight
                    }
                }
            }
        )
        print('Index created')
        return { 'success': True, 'message': 'Index DB created' }

    except Exception as e:
        print('Index already exists')
        return { 'success': False, 'message': f'Index DB: {DB_NAME} already exists' }

def refresh_indexes():
    # Here we need to read /data/ folder, find .html files and create the indexes
    directory = "data"
    html_files = glob.glob(os.path.join(directory, "*.html")) # ···> Lista de archivos html [ 'falabella.html', 'ripley.html']

    # If file (from html_files) is not in the index, then create it

    # We need to create a response to know if all files were created or are already in the index
    response = {
        'already_exists': [],
        'successfully_indexed': []
    }

    try:
        # For each file in html_files [ 'falabella.html', 'ripley.html']
        for file in html_files:
            file_name = file.split('/')[1].split('.')[0] # ···> falabella | ripley

            try:
                es.get(index=DB_NAME, id=file_name)
                response['already_exists'].append({'file_name':file_name})

            except:
                with open(file, 'r') as f:
                    file_content = f.read()
                    es.index(index='db_scrapper', id=file_name, document={
                        'title': file_name,
                        'content': file_content,
                        'timestamp': datetime.now()
                    })
                    response['successfully_indexed'].append({'file_name':file_name})

        return response

    except Exception as e:
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong' }



@app.get("/")
def read_root():
    return {"Hello": "World"}

# /api/elasticsearch/create: Create the elasticsearch: db_scrapper
@app.get("/api/elasticsearch/create")
def create_root():
    return create_index()

# /api/elasticsearch/refresh: Refresh the elasticsearch indexes
# For example, if we have a new file in the folder, we need to refresh the indexes
@app.get("/api/elasticsearch/refresh")
def refresh_root():
    return refresh_indexes()

# /api/elasticsearch/search: Search in the elasticsearch indexes
@app.get("/api/elasticsearch/search")
def search_root(q: str = Query(None, min_length=3, max_length=50)):
    # q: str = Query(None, min_length=3, max_length=50)
    # ···> Query: None, min_length: 3, max_length: 50

    # We need to search in the index for the query
    # If we have a match, then return it
    # If we don't have a match, then return an error

    try:
        # NOTE: 'content' field is the field that we want to search (in the index)
        # query: It's the query that we want to search
        query = {
            "match": {
                "content": q,
            },
        }

        # highlight: It's the highlight (the text that we want to highlight)
        highlight = {
            "fields": {
                "content": {
                    "type": "unified",
                },
            },
        }

        # --- Searching in the index ---
        resp = es.search(index="db_scrapper", query=query, highlight=highlight)
        # Return full response
        return { 'success': True, 'data': resp }

    except Exception as e:
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong. Try adding a query ex: <search?q=audifonos>' }