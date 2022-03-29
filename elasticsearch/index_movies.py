from elasticsearch import Elasticsearch
import csv
from progress.bar import Bar

INDEX_NAME = "movies"

client = Elasticsearch(
    hosts=["https://es01:9200"],
    basic_auth=('elastic', 'elasticpass'),
    ca_certs='/usr/certs/ca/ca.crt'
)

index_exists = client.indices.exists(index=INDEX_NAME)

if not index_exists:
    client.indices.create(
        index=INDEX_NAME,
        settings={
            'index': {
                'analysis': {
                    'analyzer': {
                        'custom_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'standard',
                            'filter': [
                                'lowercase',
                                'custom_edge_ngram'
                            ]
                        }
                    },
                    'filter': {
                        'custom_edge_ngram': {
                            'type': 'edge_ngram',
                            'min_gram': 2,
                            'max_gram': 10
                        }
                    }
                }
            }

        },
        mappings={
            'properties': {
                'movie': {
                    'type': 'text',
                    'analyzer': 'custom_analyzer',
                    'search_analyzer': 'standard'
                }
            }
        }
    )

    total_lines = len(open('elasticsearch/movies.csv').readlines()) - 1
    csv_reader = csv.reader(open('elasticsearch/movies.csv'))
    next(csv_reader)
    progress_bar = Bar('Indexing movies...', max=total_lines)

    for row in csv_reader:
        client.index(
            index=INDEX_NAME,
            document={
                'movie': row[1]
            }
        )
        progress_bar.next()