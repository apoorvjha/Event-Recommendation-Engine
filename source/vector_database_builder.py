import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib

class VectorDatabase:
    def __init__(self):
        self.vector_db = self.create_empty_vector_db_instance()
    def create_empty_vector_db_instance(self, data = []):
        schema = ["Index", "Value", "Embedding"]
        return pd.DataFrame(data = data, columns = schema)
    def cosine_similarity(self, embedding1, embedding2):
        arr1 = np.array(embedding1).reshape(1, -1)
        arr2 = np.array(embedding2).reshape(1, -1)
        return np.sum(np.matmul(arr1, arr2.T))
    def create_index(self):
        date_component = datetime.now() + timedelta(days = np.random.randint(-100, 100))
        return hashlib.md5(date_component.strftime("%Y-%m-%d").encode()).hexdigest()[ : 16]
    def insert(self, values, embeddings):
        data = []
        for value, embedding in zip(values, embeddings):
            index = self.create_index()
            data.append([index, value, embedding])
        temp_df = self.create_empty_vector_db_instance(data)
        self.vector_db = pd.concat([self.vector_db, temp_df], axis = 0, ignore_index = True)
    def search(self, embedding, k = 10):
        temp_df = self.vector_db.copy()
        temp_df["Similarity_Score"] = temp_df["Embedding"].apply(lambda x : self.cosine_similarity(x, embedding))
        temp_df = temp_df.sort_values(by = "Similarity_Score", ascending = False).head(k)
        return temp_df

def test():
    vector_db = VectorDatabase()
    vector_db.insert([
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m"
    ], np.random.rand(13, 100).tolist())

    print(vector_db.search(np.random.rand(100).tolist(), k = 3))

if __name__ == '__main__':
    test()