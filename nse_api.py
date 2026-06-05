import requests
import json
import pandas as pd

HISTORICAL_URL = (
"https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString"
)

TRI_URL = (
"https://www.niftyindices.com/Backpage.aspx/getTotalReturnIndexString"
)

HEADERS = {
"Content-Type": "application/json; charset=UTF-8",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": "Mozilla/5.0"
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
    print("URL =", url)
    print("PAYLOAD =", payload)


    response = requests.post(
        url,
        json=payload,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    outer = response.json()

    records = json.loads(outer["d"])

    return pd.DataFrame(records)

