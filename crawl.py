import json
import os
import requests
from tqdm.auto import tqdm
import urllib3

urllib3.disable_warnings()

DIR = os.path.dirname(os.path.abspath(__file__))


def get_total():
    url = "https://gis.vn/api/diachinh/Diachinh_GetDMDiachinh_Tatca"
    res = requests.post(url, verify=False).json()
    res = res["result"]

    with open(os.path.join(DIR, "data/data.json"), "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

    return res


def get_geojson(id, sapnhap=False):
    if sapnhap:
        url = "https://gis.vn/api/diachinh/Diachinhsapnhap_GetDMDiachinh_Geojson_byMadiachinh"
    else:
        url = "https://gis.vn/api/diachinh/Diachinh_GetDMDiachinh_Geojson_byMadiachinh"

    payload = {"MA_DIACHINH": id}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    res = requests.post(url, headers=headers, data=payload, verify=False).json()
    data = res["result"]
    if not data:
        print(res)
        return data

    if sapnhap:
        OUT = os.path.join(DIR, f"data/satnhap_geojson/{id}.json")
    else:
        OUT = os.path.join(DIR, f"data/geojson/{id}.json")
    with open(OUT, "w") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    return data


if __name__ == "__main__":
    data = get_total()
    for d in tqdm(data):
        if os.path.exists(os.path.join(DIR, f"data/geojson/{d['MA_DIACHINH']}.json")):
            continue
        id = d["CO_GEOJSON"]
        if not id:
            continue
        get_geojson(id, sapnhap=False)
