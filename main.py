import requests
import json
import datetime
import os
import copy


class Stats:
    def __init__(self, json, shiftType, stageId, startTime, weaponList):
        self.stage_id = stageId
        self.shift_type = shiftType
        self.golden_eggs = json["golden_eggs"]
        self.power_eggs = json["power_eggs"]
        self.members = []
        self.start_time = startTime
        self.weapon_list = weaponList
        self.event_type = json["event_type"]
        self.water_level = json["water_level"]


class Record:
    def __init__(self, json):
        try:
            self.id = json["id"]
            self.golden_eggs = json["golden_eggs"]
            self.power_eggs = json["power_eggs"]
            self.members = sorted(json["members"])
            try:
                self.water_level = self.getWaterLevel(json["water_id"])
                self.event_type = self.getEventType(json["event_id"])
            except TypeError:
                self.water_level = None
                self.event_type = None
        except KeyError:
            self.water_level = None
            self.event_type = None
        except TypeError:
            pass

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


if __name__ == "__main__":
    with open("public/assets/json/schedule.json", mode="r") as f:
        print(f"Getting latest records from Salmon Stats")
        currentTime = datetime.datetime.now().timestamp()
        # schedules = list(filter(lambda x: x["start_time"] >= 1568246400 and x["start_time"] < currentTime, json.load(f)))
        schedules = list(filter(lambda x: x["start_time"] > currentTime - 3600 * 24 * 7 and x["start_time"] < currentTime, json.load(f)))
        print(f"Getting {len(schedules)} records")
        scheduleRecords = []

        for schedule in schedules:
            # 元データからコピー
            stageId = schedule["stage_id"]
            startTime = schedule["start_time"]
            endTime = schedule["end_time"]
            rareWeapon = None
            if -1 in schedule["weapon_list"]:
                rareWeapon = schedule["rare_weapon"]
            scheduleId = datetime.datetime.fromtimestamp(startTime, datetime.timezone.utc).strftime("%Y%m%d%H")
            weaponList = schedule["weapon_list"]
            shiftType = "normal"
            if weaponList.count(-1) == 1:
                # 単緑編成
                shiftType = "random1"
            if weaponList.count(-1) == 4:
                # 単緑編成
                shiftType = "random4"
            if weaponList.count(-2) == 4:
                # 単緑編成
                shiftType = "grizzco"

            url = f"https://salmon-stats-api.yuki.games/api/schedules/{scheduleId}"
            print(f"Getting {scheduleId} records")
            records = requests.get(url).json()["records"]

            # データがあれば抽出
            if records is not None:
                # 夜のみ記錄
                totals = [
                    Record(records["totals"]["golden_eggs"]).__dict__,
                    Record(records["totals"]["power_eggs"]).__dict__
                ]
                # 昼のみ記錄
                no_night_totals = [
                    Record(records["no_night_totals"]["golden_eggs"]).__dict__,
                    Record(records["no_night_totals"]["power_eggs"]).__dict__
                ]
                waves = [
                    list(map(lambda x: Record(x).__dict__, records["wave_records"]["golden_eggs"])),
                    list(map(lambda x: Record(x).__dict__, records["wave_records"]["power_eggs"]))
                ]

                dict = {
                    "stage_id": stageId,
                    "start_time": startTime,
                    "shift_type": shiftType,
                    "end_time": endTime,
                    "weapon_list": weaponList,
                    "rare_weapon": rareWeapon,
                    "records": {
                        "golden_eggs": {
                            "total": totals[0],
                            "no_night_event": no_night_totals[0],
                            "waves": waves[0]
                        },
                        "power_eggs": {
                            "total": totals[1],
                            "no_night_event": no_night_totals[1],
                            "waves": waves[1]
                        },
                    }
                }
                with open(f"public/assets/json/records/{startTime}.json", mode="w") as w:
                    json.dump(dict, w)
                scheduleRecords.append(dict)

    # 全記錄を読み込んで編成ごとに最も良いものを計算する
    records = os.listdir("public/assets/json/records")

    waves = [[], []]
    totals = [[], []]
    for record in records:
        with open(f"public/assets/json/records/{record}", mode="r") as f:
            record = json.load(f)
            stageId = record["stage_id"]
            shiftType = record["shift_type"]
            weaponList = record["weapon_list"]
            startTime = record["start_time"]
            # 金イクラWAVE記錄
            waves[0].extend(list(map(lambda x: Stats(x, shiftType, stageId, startTime, weaponList), record["records"]["golden_eggs"]["waves"])))
            waves[1].extend(list(map(lambda x: Stats(x, shiftType, stageId, startTime, weaponList), record["records"]["power_eggs"]["waves"])))
            totals[0].append(Stats(record["records"]["golden_eggs"]["total"], shiftType, stageId, startTime, weaponList))
            totals[1].append(Stats(record["records"]["golden_eggs"]["no_night_event"], shiftType, stageId, startTime, weaponList))

    records = {}
    for stage_id in [5000, 5001, 5002, 5003, 5004]:
        shift_records = {}
        for shift_type in ["normal", "random1", "random4", "grizzco"]:
            golden_eggs = []
            power_eggs = []
            try:
                total = [
                    copy.deepcopy(max(list(filter(lambda x:
                                                  x.shift_type == shift_type and
                                                  x.stage_id == stage_id, totals[0])), key=lambda x: x.golden_eggs)).__dict__,
                    copy.deepcopy(max(list(filter(lambda x:
                                                  x.shift_type == shift_type and
                                                  x.stage_id == stage_id, totals[0])), key=lambda x: x.power_eggs)).__dict__
                ]
                no_night_total = [
                    copy.deepcopy(max(list(filter(lambda x:
                                                  x.shift_type == shift_type and
                                                  x.stage_id == stage_id, totals[1])), key=lambda x: x.golden_eggs)).__dict__,
                    copy.deepcopy(max(list(filter(lambda x:
                                                  x.shift_type == shift_type and
                                                  x.stage_id == stage_id, totals[1])), key=lambda x: x.power_eggs)).__dict__
                ]
            except ValueError:
                pass

            for water_level in ["low", "normal", "high"]:
                for event_type in ["-", "rush", "goldie-seeking", "griller", "the-mothership", "fog", "cohock-charge"]:
                    try:
                        # ディープコピーしないと上書きされてしまう
                        golden_eggs_result = copy.deepcopy(max(list(filter(lambda x:
                                                                           x.shift_type == shift_type and
                                                                           x.stage_id == stage_id and
                                                                           x.water_level == water_level and
                                                                           x.event_type == event_type, waves[0])), key=lambda x: x.golden_eggs).__dict__)
                        power_eggs_result = copy.deepcopy(max(list(filter(lambda x:
                                                                          x.shift_type == shift_type and
                                                                          x.stage_id == stage_id and
                                                                          x.water_level == water_level and
                                                                          x.event_type == event_type, waves[1])), key=lambda x: x.power_eggs).__dict__)
                        # 不要な項目の削除
                        golden_eggs_result.pop("stage_id")
                        golden_eggs_result.pop("shift_type")
                        power_eggs_result.pop("stage_id")
                        power_eggs_result.pop("shift_type")
                        power_eggs.append(power_eggs_result)
                        golden_eggs.append(golden_eggs_result)
                    except ValueError:
                        pass
            # 総合記錄の不要な項目の削除
            total[0].pop("stage_id")
            total[0].pop("shift_type")
            total[0].pop("event_type")
            total[0].pop("water_level")
            total[1].pop("stage_id")
            total[1].pop("shift_type")
            total[1].pop("event_type")
            total[1].pop("water_level")
            # 編成区分ごとの記錄
            shift_records[shift_type] = {
                "golden_eggs": {
                    "total": total[0],
                    "no_night_event": no_night_total[0],
                    "waves": golden_eggs,
                },
                "power_eggs": {
                    "total": total[1],
                    "no_night_event": no_night_total[1],
                    "waves": power_eggs,
                },
            }
        # ステージごとの記錄
        records[stage_id] = shift_records
    with open("public/assets/json/records.json", mode="w") as f:
        json.dump(records, f)
