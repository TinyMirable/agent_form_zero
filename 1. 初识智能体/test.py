from main import get_weather,get_attraction

import json



def test_get_weather():
    city = "广州"
    responce = get_weather(city)

    print(json.dumps(responce,indent=2,ensure_ascii=False))

def test_get_attraction():
    r = get_attraction(city="广州",weather="clear")
    print(json.dumps(r,indent=2,ensure_ascii=False))

if __name__ == "__main__":
    test_get_weather()
    test_get_attraction()