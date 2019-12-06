import requests
import pprint
import pytz
import html
import sys
import datetime

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be MM-YYYY")

month = sys.argv[-1]

validate(month)

url = "https://www.socialists.nyc/api/open/GetItemsByMonth?month=%s&collectionId=57a26db33e00be2197c966ad" % month
print(url)
# % dict(
#     url="https://www.socialists.nyc/api/open",
#     endpoint="/GetItemsByMonth",
#     month="04-2019")

timezoneLocal = pytz.timezone('America/New_York')
def convert_ts(ts):
    utc = pytz.utc
    return pytz.utc.localize(datetime.datetime.utcfromtimestamp(ts / 1000)).astimezone(timezoneLocal)

str_temp ="""%s
%s
%s - %s
%s
"""
results = [
    str_temp %
    (html.unescape(r["title"]),
    convert_ts(r["startDate"]).strftime("%A %B %-d %Y"),
    convert_ts(r["startDate"]).strftime("%-l:%M%p"),
    convert_ts(r["endDate"]).strftime("%-l:%M%p"),
    "\n".join(filter(None,
    [r["location"].get("addressTitle"),
    r["location"].get("addressLine1"),
    r["location"].get("addressLine2")]
    )))
    for r in
    sorted(requests
    .get(url)
    .json(), key=lambda x:x["startDate"])]
print("\n".join(results))
