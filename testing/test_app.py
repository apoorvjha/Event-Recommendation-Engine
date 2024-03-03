import requests

def test_set_context():
    base_url = "http://127.0.0.1:8080/"
    end_point = "/api/v1/set_context_phrases"
    body = {
        "context_phrases" : ["conference", "workshop", "seminar", "symposium", "summit", "expo","convention", "meetup", "networking", "webinar", "training", "retreat", "exhibition", "panel", "lecture", "forum", "showcase", "roundtable", "demo", "gala"]
    }
    header = {
        "Content-Type" : "application/json"
    }

    try:
        response = requests.post(base_url+end_point, json = body, headers = None, verify = False)
        print(response.text)
        assert True
    except:
        assert False

def test_get_k_closest_phrases():
    base_url = "http://127.0.0.1:8080/"
    end_point = "/api/v1/get_k_closest_phrases"
    body = {
        "query_phrases" : ["learning", "fun", "enjoyment"]
    }
    header = {
        "Content-Type" : "application/json"
    }

    try:
        response = requests.post(base_url+end_point, json = body, headers = None, verify = False)
        print(response.text)
        assert True
    except:
        assert False


if __name__ == '__main__':
    test_set_context()
    test_get_k_closest_phrases()