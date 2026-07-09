import requests
import json
import pandas as pd

HISTORICAL_URL = (
    "https://www.niftyindices.com/BackPage/getHistoricaldatatabletoString"
)

TRI_URL = (
    "https://www.niftyindices.com/BackPage/getTotalReturnIndexString"
)

HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.niftyindices.com/reports/historical-data",
    "Origin": "https://www.niftyindices.com",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}


def get_index_data(
    name,
    index_name,
    start_date,
    end_date,
    data_type
):

    if data_type == "Historical Index Data":

        url = HISTORICAL_URL

        payload = {
            "cinfo": (
                f"{{'name':'{name}',"
                f"'startDate':'{start_date}',"
                f"'endDate':'{end_date}',"
                f"'indexName':'{index_name}'}}"
            )
        }

    else:

        url = TRI_URL

        payload = {
            "cinfo": (
                f"{{'name':'{index_name}',"
                f"'startDate':'{start_date}',"
                f"'endDate':'{end_date}',"
                f"'indexName':'{index_name}'}}"
            )
        }

    session = requests.Session()

    session.headers.update(HEADERS)

    # Get cookies first
    session.get(
        "https://www.niftyindices.com/reports/historical-data",
        timeout=30
    )

    response = session.post(
        url,
        json=payload,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print(response.text[:1000])

    response.raise_for_status()

    try:
        outer = response.json()
    except Exception:
        raise Exception(
            f"NSE did not return JSON.\n\n"
            f"Status: {response.status_code}\n\n"
            f"{response.text[:1000]}"
        )

    try:
        records = json.loads(outer["d"])
    except Exception:
        raise Exception(
            f"Unable to parse response.\n\n"
            f"{outer}"
        )

    return pd.DataFrame(records)
