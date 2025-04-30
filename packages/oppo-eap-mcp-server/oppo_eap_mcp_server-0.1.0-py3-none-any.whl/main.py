from mcp.server.fastmcp import FastMCP

import requests
import json
from typing import Tuple, List

# Create an MCP server
mcp = FastMCP("oppo-eap-mcp-server")


def auth(account: str, password: str, area: str) -> Tuple[str, str]: 
    """
        Use account and password to authenticate a user to get two tokens splitted by line
        Args:
            account: Account name
            password: Password
            area: Area code, 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
        Returns:
            Tuple[str, str]: tuple of Two string-type tokens 
    """

    assert(area == "zh" or area == "yd" or area == "dny"), f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'"

    url = "http://thirdpart.myoas.com/thirdpart-leida/common/getSessionKey"

    payload = json.dumps({
            "username": account,
            "password": password,
            "area": area
        })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code != 200 or response.json()["code"] != 200:
        raise Exception(f"Error: username or password error, status code: {response.status_code}")
    response_json = response.json()
    
    if response_json["code"] != 200:
        raise Exception(f"Error: username or password error, status code: {response_json}")
    
    tgt = response_json["data"]["tgt"]
    token = response_json["data"]["token"]

    return (tgt, token)


def post(area: str, url: str, headers: dict = {}, data: dict = {}) -> str:
    """
        Send a request to the server
        Args:
            area: which area to query. 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
            url: URL of the server
            headers: Additional Header of the request
            data: Data of the request
        Returns:
            str: Response from the server
    """

    Authorization_qodp, SessionKey = auth(USERNAME, PASSWORD, area)

    default_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': Authorization_qodp,
        'Session-Key': SessionKey
    }

    default_headers.update(headers)
    payload = json.dumps(data)
    response = requests.request("POST", url, headers=default_headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"access {url} error with post request: status code {response.status_code}")
    response_json = response.json()
    if response_json["code"] != 200:
        raise Exception(f"access {url} error with post request: status code {response_json}")
    
    return response_json


@mcp.tool()
def get_models_information(area: str) -> str:
    """
        Get models information. You can use this function to get models information list.
        each line have information about model name, market name, series name and go to market time, seperated by ;
        model name format is like PKP110 and so on.
        market name format is like A5 Pro, A5 活力版 and so on.
        series name format is like A系列 and so on.
        go to market time format is like 2023-10-01 format.
        You can use this function to do the following tasks:
            given a model name, you can find the market name, series name and go to market time in the response.
            given a market name, you can find the model name, series name and go to market time in the response.
            given a series name, you can find all model names, market names and go to market time under this series in the response.
            given a market name , such as A5, you can find a last year model name, for example A3; you can find a next year model name, for example A6.
            given a market name , such as A5 活力版, you can find a last year model name , for example A3 活力版; you can find a next year model name, for example A6 活力版.
        Args:
            area: which area to query. 'zh' for china, 'yd' for india, 'dny' for southeast asia, 'om' for europe. don't accept other area code
        Returns:
            str: List of models information, seperated by lines. each line is a string of the format: model name; market name; series name; go to market time
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/indexBoard/getModelOta2"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/indexBoard/getModelOta2"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/indexBoard/getModelOta2"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    data = {
        "gifOta": False,
        "models":[],
        "userNum": USERNAME,
        "isAdmin":0
    }

    response_json = post(area, url, data=data)
    response_data =  response_json["data"]

    merged_data = []
    for series in response_data.values():
        for item in series:
            merged_item = {
                "model": item["model"],
                "marketName": item["marketName"],
                "series": item["series"],
                "marketTime": item["marketTime"]
            }
            merged_data.append(merged_item)
    
    return_data = []
    for series in response_data.values():
        for item in series:
            merged_item = f"{item['model']}; {item['marketName']}; {item['series']}; {item['marketTime']}"
            return_data.append(merged_item)

    return "\n".join(return_data)

@mcp.tool()
def get_ota_version_list_by_model_name(area: str, model_name: str) -> str:
    """
        Get OTA version list by model name. You can use this function to get OTA version list by model name.
        Args:
            area: which area to query. 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
            model_name: model name, such as PKP110 and so on.
        Returns:
            str: List of OTA version, seperated by lines. each line is a string of the format: otaVersion; versionDate; number of users in this ota version
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    data = {
            "models":[ model_name ],
            "isPre": None,
            "sort":1
        }

    response_json = post(area, url, data=data)
    version_list = response_json["data"][0]["otaConditionVos"]

    return_data = []
    for version in version_list:
        return_data.append(f"{version['otaVersion']}; {version['versionDate']}; {version['uv']}")

    return "\n".join(return_data)

@mcp.tool()
def get_today_datetime() -> str:
    """
        Get today's date and time. You can use this function to get today's date and time.
        Returns:
            str: Today's date and time in the format of YYYY-MM-DD
    """
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return today

@mcp.tool()
def get_active_users_number_by_model_and_time_range(area:str, model_name:str, startDate:str , endDate:str, ota_version:str = None) -> str:
    """
        Query active users trend. You can use this function to query active users trend by model name and OTA version.
        Args:
            area: which area to query. 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
            model_name: model name, such as PKP110 and so on. don't accept market name
            startDate: start date, format must be YYYY-MM-DD. such as 2023-10-01
            endDate: end date, format must be YYYY-MM-DD. such as 2023-10-30
            ota_version: OTA version, such as PKP110_11_A.11.1.1.1_2023-10-01. if not specified, it will query all OTA versions
        Returns:
            str: List of active users trend, seperated by lines. each line is a string of the format: date; active users
    """

    # set url
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    # set ota_version list
    if ota_version:
        ota_version_list = [ota_version]
    else:
        ota_version_list = []

    data = {
        "excepType": 0,
        "models": [
            {
                "model": model_name,
                "otaVerList": ota_version_list
            }
        ],
        "self": 3,  # 3 查询所有， 1 表示自研， 2 表示非自研
        "dateType": 8,
        "startDate": startDate,
        "endDate": endDate,
        "order": "asc",
        "dataType": 4,
        "systemType": 1,
        "download": 2,
        "isTotal": 0,
        "memoryDeviceVersionList": [],
        "storageDeviceVersionList": [],
        "storageSizeList": [],
        "availableRateList": [],
        "isCrashRestartTotal": 1
    }

    print(data)

    response_json = post(area, url, data=data)
    response_data = response_json["data"]
    activie_users = response_data["yAxisData"][0]
    datetime = response_data["xAxisData"]
    

    return_data = []
    for i in range(len(datetime)):
        return_data.append(f"{datetime[i]}; {activie_users[i]}")
    
    return "\n".join(return_data)

def main():

    # parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="FastMCP")
    parser.add_argument("--username", type=str, required=True, help="Username")
    parser.add_argument("--password", type=str, required=True, help="Password")
    args = parser.parse_args()

    # # save username and password to global variables
    global USERNAME
    global PASSWORD
    USERNAME = args.username
    PASSWORD = args.password


    # start the server by STDIO mode
    mcp.run(transport="stdio")

if __name__ == "__main__":
   
    main()