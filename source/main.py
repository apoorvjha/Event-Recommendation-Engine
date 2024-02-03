from utility import *
from embedding_model import *
from vector_database_builder import *

def orchestrator(context_words, query_word):
    print("[+] Initializing Orchestrator!")
    try:
        config = read_config()
        print(f"[+] Successfully read the configuration file!")
    except Exception as e:
        print(f"[-] Failed to read configuration due to {e}!")
    try:
        embedding_matrix = get_embedding(config, context_words)
        print(f"[+] Successfully computed the embedding matrix for context words!")
    except Exception as e:
        print(f"[-] Failed to compute embedding matrix for context words due to {e}!")
    try:
        vector_db = VectorDatabase()
        print(f"[+] Successfully initialized vector database instance!")
    except Exception as e:
        print(f"[-] Failed to Initialize vector database instance due to {e}!")
    try:
        vector_db.insert(
            context_words,
            embedding_matrix.cpu().numpy().tolist()   
        )
        print(f"[+] Successfully inserted records into vector database!")
    except Exception as e:
        print(f"[-] Failed to insert the embeddings into vector database due to {e}!")
    try:
        search_word_embedding = get_embedding(config, [query_word])
        print(f"[+] Successfully computed embedding for query word!")
    except Exception as e:
        print(f"[-] Failed to compute embedding matrix for query word due to {e}!")
    try:
        k = config["TOP_K"]
        matching_words = vector_db.search(search_word_embedding.cpu().numpy().tolist()[0], k = k)
        print(f"[+] Successfully computed the top {k} nearest context words with respect to query word!")
    except Exception as e:
        print(f"[-] Failed to compute the top {k} nearest context words with respect to query word!")
    
    print(f"\n[Result] Top {k} matching words in context words for {query_word} is : {', '.join(matching_words['Value'].tolist())}")

if __name__ == '__main__':
    context_words = ["king", "queen", "servant", "transformer", "bruteforce", "war"]
    query_word = "prince"
    orchestrator(context_words, query_word)    