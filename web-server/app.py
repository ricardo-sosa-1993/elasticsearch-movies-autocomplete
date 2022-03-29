from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

elasticsearch_client = Elasticsearch(
    hosts=["https://es01:9200"],
    basic_auth=('elastic', 'elasticpass'),
    ca_certs='/usr/certs/ca/ca.crt'
)

INDEX_NAME = "movies"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search-movie')
def search_movie():
    movie_to_search = request.args.get('name')
    response = elasticsearch_client.search(
        index=INDEX_NAME,
        query={"match": {"movie": {"query": movie_to_search, "fuzziness": 1}}}
    )
    movies = [item['_source']['movie'] for item in response['hits']['hits']]
    return jsonify(movies)
