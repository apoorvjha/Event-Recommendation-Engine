import sys
sys.path.append("../source")
from vector_database_builder import *
sys.path.pop()

def test_VectorDatabase_init():
    try:
        vector_db = VectorDatabase()
        assert True
    except Exception as e:
        assert False
def test_VectorDatabase_insert():    
    vector_db = VectorDatabase()
    try:
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
        assert True
    except Exception as e:
        assert False
def test_VectorDatabase_search():
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
    try:
        vector_db.search(np.random.rand(100).tolist(), k = 3)
        assert True
    except Exception as e:
        assert False