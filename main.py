from curses import meta
from time import timezone
import requests
import json
import datetime
import os
import copy
from dotenv import load_dotenv


class Result:
    def __init__(self, json, shiftType, stageId, startTime, weaponList):
        self.stage_id = stageId
        self.salmon_id = json["id"]
        self.shift_type = shiftType
        self.danger_rate = json["danger_rate"]
        self.golden_eggs = json["golden_egg_delivered"]
        self.power_eggs = json["power_egg_collected"]
        self.members = json["members"]
        self.start_time = startTime
        self.weapon_list = weaponList
        self.wave = list(map(lambda x: Wave(x).__dict__, json["waves"]))


class Wave:
    def __init__(self, json):
        self.event_type = self.getEventType(json["event_id"])
        self.water_level = self.getWaterLevel(json["water_id"])
        self.golden_ikura_num = json["golden_egg_delivered"]
        self.ikura_num = json["power_egg_collected"]

    def getEventType(self, eventType):
        if eventType == 0:
            return "-"
        if eventType == 1:
            return "cohock-charge"
        if eventType == 2:
            return "fog"
        if eventType == 3:
            return "goldie-seeking"
        if eventType == 4:
            return "griller"
        if eventType == 5:
            return "the-mothership"
        if eventType == 6:
            return "rush"

    def getWaterLevel(self, waterLevel):
        if waterLevel == 1:
            return "low"
        if waterLevel == 2:
            return "normal"
        if waterLevel == 3:
            return "high"


class Metadata:
    def __init__(self, json):
        self.clear = json["results"]["clear"]
        self.failure = json["results"]["fail"]
        self.golden_eggs = json["total"]["golden_eggs"]
        self.power_eggs = json["total"]["power_eggs"]
        self.rescue = json["total"]["rescue"]
        self.help = json["total"]["death"]


class Schedule:
    def __init__(self, json):
        self.stage_id = json["stage_id"]
        self.shift_type = "normal"
        if json["weapon_list"].count(-1) == 1:
            self.shift_type = "random1"
        if json["weapon_list"].count(-1) == 4:
            self.shift_type = "random4"
        if json["weapon_list"].count(-2) == 4:
            self.shift_type = "grizzco"
        self.start_time = json["start_time"]
        self.rare_weapon = json["rare_weapon"]
        self.weapon_list = json["weapon_list"]


class Record:
    def __init__(self, json, salmon_id, shift_type, weapon_list, start_time, danger_rate, members, stage_id):
        self.stage_id = stage_id
        self.salmon_id = salmon_id
        self.shift_type = shift_type
        self.danger_rate = danger_rate
        self.golden_ikura_num = json["golden_ikura_num"]
        self.ikura_num = json["ikura_num"]
        self.members = sorted(members)
        self.water_level = json["water_level"]
        self.event_type = json["event_type"]
        self.start_time = start_time
        self.weapon_list = weapon_list


if __name__ == "__main__":
    # ディレクトリの作成
    try:
        os.makedirs("results")
    except:
        pass
    with open("src/assets/json/schedule.json", mode="r") as f:
        currentTime = datetime.datetime.now().timestamp()
        schedules = list(filter(lambda x: x["start_time"] < currentTime, json.load(f)))
        schedules = list(map(lambda x: Schedule(x), schedules))

        # プレイヤーのIDを入力
        player_ids = os.environ.get("PLAYER_ID")

        for player_id in player_ids:
            # メタデータの取得
            url = f"https://salmon-stats-api.yuki.games/api/players/metadata/?ids={player_id}"
            metadata = Metadata(requests.get(url).json()[0])
            results = os.listdir(f"src/assets/json/results")
            min_page_id = int(len(results) / 200) + 1
            max_page_id = int((metadata.failure + metadata.clear) / 200) + 1

            # 差分のリザルトを取得する
            for page_id in range(min_page_id, max_page_id + 1):
                print(f"Getting {page_id} / {max_page_id} records")
                url = f"https://salmon-stats-api.yuki.games/api/players/{player_id}/results?raw=0&count=200&page={page_id}"

                results = requests.get(url, timeout=(3.0, 30.0)).json()["results"]
                for result in results:
                    schedule_id = int(datetime.datetime.strptime(result["schedule_id"],
                                      "%Y-%m-%d %H:00:00").replace(tzinfo=datetime.timezone.utc).timestamp())
                    schedule = list(filter(lambda x: x.start_time == schedule_id, schedules))[0]
                    stage_id = schedule.stage_id
                    shift_type = schedule.shift_type
                    start_time = schedule.start_time
                    weapon_list = schedule.weapon_list
                    result = Result(result, shift_type, stage_id, start_time, weapon_list)
                    with open(f"src/assets/json/results/{result.salmon_id}.json", mode="w") as w:
                        json.dump(result.__dict__, w)

    # 全記錄を読み込んで編成ごとに最も良いものを計算する
    results = os.listdir("src/assets/json/results")

    waves = []
    for result in results:
        with open(f"src/assets/json/results/{result}", mode="r") as f:
            result = json.load(f)
            salmon_id = result["salmon_id"]
            stage_id = result["stage_id"]
            shift_type = result["shift_type"]
            weapon_list = result["weapon_list"]
            start_time = result["start_time"]
            danger_rate = result["danger_rate"]
            members = result["members"]
            # 金イクラWAVE記錄
            waves.extend(list(map(lambda x: Record(x, salmon_id, shift_type, weapon_list,
                         start_time, danger_rate, members, stage_id), result["wave"])))
    records = {}
    for stage_id in [5000, 5001, 5002, 5003, 5004]:
        shift_records = {}
        for shift_type in ["normal", "random1", "random4", "grizzco"]:
            golden_eggs = []
            power_eggs = []
            # try:
            #     total = [
            #         copy.deepcopy(max(list(filter(lambda x:
            #                                       x.shift_type == shift_type and
            #                                       x.stage_id == stage_id, totals[0])), key=lambda x: x.golden_eggs)).__dict__,
            #         copy.deepcopy(max(list(filter(lambda x:
            #                                       x.shift_type == shift_type and
            #                                       x.stage_id == stage_id, totals[0])), key=lambda x: x.power_eggs)).__dict__
            #     ]
            #     no_night_total = [
            #         copy.deepcopy(max(list(filter(lambda x:
            #                                       x.shift_type == shift_type and
            #                                       x.stage_id == stage_id, totals[1])), key=lambda x: x.golden_eggs)).__dict__,
            #         copy.deepcopy(max(list(filter(lambda x:
            #                                       x.shift_type == shift_type and
            #                                       x.stage_id == stage_id, totals[1])), key=lambda x: x.power_eggs)).__dict__
            #     ]
            # except ValueError:
            #     pass

            for water_level in ["low", "normal", "high"]:
                for event_type in ["-", "rush", "goldie-seeking", "griller", "the-mothership", "fog", "cohock-charge"]:
                    try:
                        # ディープコピーしないと上書きされてしまう
                        golden_eggs_result = copy.deepcopy(max(list(filter(lambda x:
                                                                           x.shift_type == shift_type and
                                                                           x.stage_id == stage_id and
                                                                           x.water_level == water_level and
                                                                           x.event_type == event_type, waves)), key=lambda x: x.golden_ikura_num).__dict__)
                        power_eggs_result = copy.deepcopy(max(list(filter(lambda x:
                                                                          x.shift_type == shift_type and
                                                                          x.stage_id == stage_id and
                                                                          x.water_level == water_level and
                                                                          x.event_type == event_type, waves)), key=lambda x: x.ikura_num).__dict__)
                        # 不要な項目の削除
                        golden_eggs_result.pop("stage_id")
                        golden_eggs_result.pop("shift_type")
                        power_eggs_result.pop("stage_id")
                        power_eggs_result.pop("shift_type")
                    except ValueError:
                        if (event_type == "rush" or event_type == "goldie-seeking" or event_type == "griller") and water_level == "low":
                            pass
                        if event_type == "cohock-charge" and water_level != "low":
                            pass
                        golden_eggs_result = {
                            "salmon_id": 0,
                            "danger_rate": "0.0",
                            "golden_ikura_num": 0,
                            "ikura_num": 0,
                            "members": [
                            ],
                            "water_level": water_level,
                            "event_type": event_type,
                            "start_time": 0,
                            "weapon_list": [
                            ]
                        }
                        power_eggs_result = {
                            "salmon_id": 0,
                            "danger_rate": "0.0",
                            "golden_ikura_num": 0,
                            "ikura_num": 0,
                            "members": [
                            ],
                            "water_level": water_level,
                            "event_type": event_type,
                            "start_time": 0,
                            "weapon_list": [
                            ]
                        }
                    power_eggs.append(power_eggs_result)
                    golden_eggs.append(golden_eggs_result)
            # 総合記錄の不要な項目の削除
            # total[0].pop("stage_id")
            # total[0].pop("shift_type")
            # total[0].pop("event_type")
            # total[0].pop("water_level")
            # total[1].pop("stage_id")
            # total[1].pop("shift_type")
            # total[1].pop("event_type")
            # total[1].pop("water_level")
            # 編成区分ごとの記錄
            shift_records[shift_type] = {
                "golden_eggs": {
                    # "total": total[0],
                    # "no_night_event": no_night_total[0],
                    "waves": golden_eggs,
                },
                "power_eggs": {
                    # "total": total[1],
                    # "no_night_event": no_night_total[1],
                    "waves": power_eggs,
                },
            }
        # ステージごとの記錄
        records[stage_id] = shift_records
    with open("src/assets/json/records.json", mode="w") as f:
        json.dump(records, f)
