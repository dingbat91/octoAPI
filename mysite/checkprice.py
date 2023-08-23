import requests
import requests_cache
import math
import datetime

# URL for API request
apiURL = "https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-A/standard-unit-rates/"


# gets current time in ISO format
def get_time():
    now = datetime.datetime.now()
    now = now.isoformat("T", "seconds")
    now = now + "Z"
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
        newtime[0] = str(int(newtime[0]) + 1)

    newtime = ":".join(newtime)
    newtime = time.split("T")[0] + "T" + newtime

    data = {"startTime": time, "endTime": newtime}
    return data


# Pulls latest price from Octopus API and it's valid timing
# includes caching from requests_cache to save extreneous API calling
def get_price(url, times, **kwargs):
    params = {"period_from": times.get("startTime"), "period_to": times.get("endTime")}
    s = requests_cache.CachedSession("datacache", expire_after=datetime.timedelta(minutes=25))
    r = s.get(url, params=params)

    # Data Cache Debug
    if "debug" in kwargs.keys():
        if r.from_cache:
            print("Data from cache")
        else:
            print("Data from API")

    # check for valid return
    if r.status_code == 200:
        json = r.json()
        price: int = json["results"][0]["value_inc_vat"]
        price: int = math.ceil(price)
        valid_to: str = json["results"][0]["valid_to"]
        data = {"pricedata": {"price": price, "valid_to": valid_to}}
        return data
    else:
        data = {"code": r.status_code}
        return data
