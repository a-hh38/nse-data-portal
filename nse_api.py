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
    response = requests.post(
    url,
    json=payload,
    headers=HEADERS,
    timeout=30
    )
    
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Response:")
    print(response.text[:1000])
    
    response.raise_for_status()
    
    try:
        outer = response.json()
    except Exception:
        raise Exception(
            f"NSE did not return JSON.\n\n"
            f"Status: {response.status_code}\n\n"
            f"{response.text[:500]}"
        )
    
    try:
        records = json.loads(outer["d"])
    except Exception:
        raise Exception(
            f"Unable to parse outer['d'].\n\n"
            f"{outer}"
        )
    
    return pd.DataFrame(records)
    
