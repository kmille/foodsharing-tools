from typing import Any
from pathlib import Path
import sys
import requests
from ics import Calendar, Event
import browser_cookie3
from ics.alarm import DisplayAlarm
import arrow
import argparse
import json

FOODSHARING_DOMAIN = "foodsharing.de"


def get_next_free_pickup(store_id: int) -> Any:
    cookies = browser_cookie3.load(domain_name=FOODSHARING_DOMAIN)
    if len(cookies) == 0:
        print("Error: Could not find any cookies.")
        sys.exit(1)
    resp = requests.get(f"https://foodsharing.de/api/stores/{store_id}/pickups", cookies=cookies)

    status = resp.status_code
    if status != 200:
        print(f"Error. Response code is not 200: {status}")
        sys.exit(1)

    content_type = resp.headers['content-type']
    if content_type != "application/json":
        print(f"Error. Content type is not application/json: {content_type}")
        sys.exit(1)
    pickups = resp.json()['pickups']
    for pickup in pickups:
        if pickup['isAvailable']:
            return pickup
        #date = arrow.get(pickup['date'])
        #is_available = pickup['isAvailable']
        #print(f"{date.format('DD.MM (ddd)')}: {is_available}")


def get_own_pickups() -> Any:
    cookies = browser_cookie3.load(domain_name=FOODSHARING_DOMAIN)
    if len(cookies) == 0:
        print("Error: Could not find any cookies.")
        sys.exit(1)
    resp = requests.get("https://foodsharing.de/api/pickup/registered", cookies=cookies)

    status = resp.status_code
    if status != 200:
        print(f"Error. Response code is not 200: {status}")
        sys.exit(1)

    content_type = resp.headers['content-type']
    if content_type != "application/json":
        print(f"Error. Content type is not application/json: {content_type}")
        sys.exit(1)
    pickups = resp.json()
    for pickup in pickups:
        begin = arrow.get(pickup['date'])
        name = f"Foodsharing: {pickup['store']['name']}"
        alarm1 = DisplayAlarm(display_text=name,
                              trigger=begin.shift(hours=-1))
        alarm2 = DisplayAlarm(display_text=name,
                              trigger=begin.shift(days=-1))
        cal = Calendar()
        e = Event()
        e.name = name
        e.begin = begin
        e.end = begin.shift(hours=+2)
        e.alarms = (alarm1, alarm2)
        cal.events.add(e)
        p = Path(f"~/Downloads/Foodsharing-Abholung-{begin.format('ddd-DD.MM')}.ics").expanduser()
        p.write_text(cal.serialize())
        print(f"Wrote ics file to {p}")


def main():
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("-e", "--export", action="store_true", help="Export ics file for all of pickups to ~/Downloads")
    parser.add_argument("-s", "--store", type=int, help="Show info about next free slot for given store_id")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.export:
        get_own_pickups()
    elif args.store:
        pickup = get_next_free_pickup(int(args.store))
        if pickup:
            print(json.dumps(pickup, indent=4))
        else:
            print("No free pickup available")


if __name__ == '__main__':
    main()
