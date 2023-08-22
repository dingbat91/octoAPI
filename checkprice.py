import requests
import math
import datetime

# URL for API request
apiURL = "https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-A/standard-unit-rates/"


# gets current time in ISO format
def get_time():
    now = datetime.datetime.now()
    now = now.isoformat("T", "seconds")
    now = now + "Z"
    print(now)
    return now


# get time to the nearest half hour
def get_time_half_hour():
    time = get_time()
    time = time.split(":")
    if int(time[1]) < 30:
        time[1] = "00"
    else:
        time[1] = "30"

    time[2] = "00Z"
    time = ":".join(time)
    print(time)
    return time


# collects half hour and returns both that and the time half an hour later
def get_full_time():
    time = get_time_half_hour()
    newtime = time.split("T")
    newtime = newtime[1].split(":")
    if newtime[1] == "00":
        newtime[1] = "30"
    else:
        newtime[1] = "00"
        print(newtime[0])
        newtime[0] = str(int(newtime[0]) + 1)

    newtime = ":".join(newtime)
    newtime = time.split("T")[0] + "T" + newtime

    data = {"startTime": time, "endTime": newtime}
    print(data)
    return data


# Pulls latest price from Octopus API and it's valid timing
def get_price(url, times):
    params = {"period_from": times.get("startTime"), "period_to": times.get("endTime")}
    r = requests.get(url, params=params)
    json = r.json()
    print(json)
    price: int = json["results"][0]["value_inc_vat"]
    price: int = math.ceil(price)
    valid_to: str = json["results"][0]["valid_to"]
    data = {"price": price, "valid_to": valid_to}
    return data


# print(get_time_half_hour())
get_price(apiURL, get_full_time())
