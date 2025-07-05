import json
from operator import ge
import os
from typing import Counter
import requests
from tqdm.auto import tqdm
import urllib3

urllib3.disable_warnings()

DIR = os.path.dirname(os.path.abspath(__file__))


def get_total(sapnhap=False, recrawl=False):
    if sapnhap:
        url = "https://gis.vn/api/diachinh/Diachinhsapnhap_GetDMDiachinh_Tatca"
        OUT = os.path.join(DIR, f"data/satnhap_data.json")
    else:
        url = "https://gis.vn/api/diachinh/Diachinh_GetDMDiachinh_Tatca"
        OUT = os.path.join(DIR, f"data/data.json")

    if os.path.exists(OUT) and not recrawl:
        with open(OUT) as f:
            return json.load(f)

    res = requests.post(url, verify=False).json()
    res = res["result"]

    with open(OUT, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

    return res


def get_geojson(id, sapnhap=False, recrawl=False):
    if sapnhap:
        url = "https://gis.vn/api/diachinh/Diachinhsapnhap_banquyen_GetDMDiachinh_Geojson_byMadiachinh"
        OUT = os.path.join(DIR, f"data/satnhap_geojson/{id}.json")
    else:
        url = "https://gis.vn/api/diachinh/Diachinh_GetDMDiachinh_Geojson_byMadiachinh"
        OUT = os.path.join(DIR, f"data/geojson/{id}.json")

    if os.path.exists(OUT) and not recrawl:
        with open(OUT) as f:
            return json.load(f)

    payload = {"MA_DIACHINH": id}

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    res = requests.post(url, headers=headers, data=payload, verify=False).json()

    data = res["result"]
    if not data:
        # print(id, res)
        return data

    with open(OUT, "w") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    return data


if __name__ == "__main__":
    sapnhap = True
    data = get_total(sapnhap=sapnhap)
    print("Total:", len(data))
    # data = [d for d in data if d["CO_GEOJSON"]]
    print("CO_GEOJSON:", len(data))
    c = 0
    for d in tqdm(data):
        id = d["MA_DIACHINH"]
        res = get_geojson(id, sapnhap=sapnhap)
        if res:
            c += 1
    print("CO_GEOJSON:", c)
