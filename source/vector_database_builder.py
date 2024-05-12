import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
from utility import *
import sqlite3

class VectorDatabase:
    def __init__(self, db_name = "../data/vector_db.db", table_name = "VECTOR_EMBEDDING_STORE"):
        self.con = sqlite3.connect(db_name)
        self.table_name = table_name
        self.vector_db = self.create_vector_db_instance()
    def create_vector_db_instance(self, data = [], mode = 0):
        schema = ["Index", "Value", "Embedding"]
        if mode != 0:
            data = pd.DataFrame(data = data, columns = schema)
            return data
        else:
            try:
                return pd.read_sql_query(f"SELECT * FROM {self.table_name}", con = self.con)
            except:
                cur = self.con.cursor()
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name}(
                    "Index", 
                    "Value", 
                    "Embedding"
                )""")
                self.con.commit()
                return pd.DataFrame(data = data, columns = schema)
    def cosine_similarity(self, embedding1, embedding2):
        arr1 = np.array(embedding1).reshape(1, -1).astype(float)
        arr2 = np.array(embedding2).reshape(1, -1).astype(float)
        return np.sum(np.matmul(arr1, arr2.T))
    def create_index(self):
        date_component = datetime.now() + timedelta(days = np.random.randint(-100, 100))
        return hashlib.md5(date_component.strftime("%Y-%m-%d").encode()).hexdigest()[ : 16]
    def insert(self, values, embeddings):
        data = []
        for value, embedding in zip(values, embeddings):
            if self.is_already_exists(value.lower()) == True:
                continue
            index = self.create_index()
            data.append([index, value.lower(), embedding])
        temp_df = self.create_vector_db_instance(data, mode = 1)
        self.vector_db = pd.concat([self.vector_db, temp_df], axis = 0, ignore_index = True)
    def search(self, embedding, k = 10, exclude_list = []):
        temp_df = self.vector_db.copy()
        if len(exclude_list) > 0 :
            temp_df = temp_df[~temp_df["Value"].isin(exclude_list)]
        try:
            temp_df["Similarity_Score"] = temp_df["Embedding"].apply(lambda x : self.cosine_similarity(str_to_list_cvtr(x), embedding))
        except:
            temp_df["Similarity_Score"] = temp_df["Embedding"].apply(lambda x : self.cosine_similarity(x, embedding))
        if k!=-1:
            temp_df = temp_df.sort_values(by = "Similarity_Score", ascending = False).head(k)
        else:
            temp_df = temp_df.sort_values(by = "Similarity_Score", ascending = False)
        return temp_df
    def save_vector_db(self):
        in_db_data = self.create_vector_db_instance()
        idx = in_db_data["Index"].unique().tolist()
        data_to_save = self.vector_db[~self.vector_db["Index"].isin(idx)]
        data_to_save["Embedding"] = data_to_save["Embedding"].astype(str)
        data_to_save.to_sql(name = self.table_name, con = self.con, if_exists = "append", index = False)
        self.con.commit()
    def is_already_exists(self, value):
        return self.vector_db[self.vector_db["Value"] == value].shape[0] != 0
    def destruct(self):
        self.con.commit()
        self.con.close()
    def get_word_indexes(self, words):
        words = list(map(lambda x: x.lower(), words))
        return self.vector_db[self.vector_db["Value"].isin(words)]["Index"].tolist()
    def get_words(self, word_indexes):
        return self.vector_db[self.vector_db["Index"].isin(word_indexes)]["Value"].tolist()

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