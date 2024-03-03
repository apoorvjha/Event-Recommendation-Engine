from flask import Flask, request
from embedding_model import *
from utility import *
from vector_database_builder import *
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Landing page of Event Recommendation Engine!</h1>"

@app.route("/api/v1/set_context_phrases", methods = ["POST"])
def set_context_phrases():
    if request.method == 'POST':
        context_words = request.get_json()["context_phrases"]
        try:
            config = read_config()
            vector_database = VectorDatabase(config["VECTOR_DB"], config["VECTOR_STORE_TABLE_NAME"])
            embedding_matrix = get_embedding(config, context_words)
            vector_database.insert(
                context_words,
                embedding_matrix.cpu().numpy().tolist()
            )
            vector_database.save_vector_db()
            return f"Context words has been inserted successfully into vector DB!", 200
        except Exception as e:
            return f"Failed to set context words into vector DB due to {e}", 400
    else:
        return f"HTTP method {request.method} not allowed!", 404

@app.route("/api/v1/get_k_closest_phrases", methods = ["POST"])
def get_k_closest_phrases():
    if request.method == 'POST':
        query_words = request.get_json()["query_phrases"]
        try:
            config = read_config()
            vector_database = VectorDatabase(config["VECTOR_DB"], config["VECTOR_STORE_TABLE_NAME"])
            search_word_embedding = get_embedding(config, query_words)
            k = config["TOP_K"]
            response = {}
            for i in range(len(query_words)):
                matching_words = vector_database.search(search_word_embedding.cpu().numpy().tolist()[i], k = k)
                response[query_words[i]] = matching_words['Value'].tolist()
            return json.dumps(response), 200
        except Exception as e:
            print(e)
            return f"Failed to set context words into vector DB due to {e}", 400
    else:
        return f"HTTP method {request.method} not allowed!", 404 


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        port = 8080,
        debug = True
    )