import sys
sys.path.append("../source")
import embedding_model as model
sys.path.pop()

def test_embedding_model():
    try:
        words = ["transformer", "getter", "c++", "setter"]
        config = {
            "MODEL_PATH" : "bert-base-uncased",
            "BATCH_SIZE" : 4,
            "MAX_SEQUENCE_LENGTH" : 16
        }

        embedding_matrix = model.get_embedding(config, words)
        assert True
    except Exception as e:
        print(f"Embedding model failed due to {e}")
        assert False

