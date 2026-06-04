import requests
import json
import pandas as pd

URL = "https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString"

HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}


def get_index_data(name, index_name, start_date, end_date):

    cinfo = (
        f"{{'name':'{name}',"
        f"'startDate':'{start_date}',"
        f"'endDate':'{end_date}',"
        f"'indexName':'{index_name}'}}"
    )

    payload = {
        "cinfo": cinfo
    }

    response = requests.post(
        URL,
        json=payload,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    outer = response.json()

    data = json.loads(outer["d"])

    return pd.DataFrame(data)