import requests
import json

if __name__ == "__main__":
    with open("assets/json/lanplay.json", mode="w") as f:
        url = "https://script.googleusercontent.com/macros/echo?user_content_key=2Z7uc0kRKMaHO1WEHNN7__4yx-d23y1QfvxmmXyGNWI4FikNGfBY-tqXlBV-jop7oGnG3-Rq25XjQyvjla_AStky6AE-TnEUm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnNODCIGpCvTIG_y73l0eN6DXTL7am_LUGn2yZvQU_kJ211U6kHKox2FF9vc0kMk0UwA5oRoKKJbw&lib=MM2j9I9WqXTpiAIT5WzJb5jD0sxkqxnr0"
        res = requests.get(url)
        json.dump(res.json(), f, indent=4)