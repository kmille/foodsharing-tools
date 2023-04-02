# foodsharing tools

This module uses your browser cookies, so you need to be logged in to Foodsharing.

### Installation

```bash
kmille@linbox:foodsharing poetry build
...
kmille@linbox:foodsharing pip install --user dist/foodsharing-0.1.0-py3-none-any.whl
...
```

```bash
kmille@linbox:foodsharing poetry run python foodsharing/__init__.py -h
usage: foodsharing/__init__.py [-h] [-e] [-s STORE]

options:
  -h, --help            show this help message and exit
  -e, --export          Export ics file for all of pickups to ~/Downloads
  -s STORE, --store STORE
                        Show info about next free slot for given store_id
```

### Export ics file for every pickup
```bash
kmille@linbox:foodsharing ~/.local/bin/foodsharing -e
/home/kmille/.local/lib/python3.10/site-packages/ics/component.py:85: FutureWarning: Behaviour of str(Component) will change in version 0.9 to only return a short description, NOT the ics representation. Use the explicit Component.serialize() to get the ics representation.
  warnings.warn(
Wrote ics file to /home/kmille/Downloads/Foodsharing-Abholung-Wed-12.04.ics
Wrote ics file to /home/kmille/Downloads/Foodsharing-Abholung-Sat-15.04.ics
Wrote ics file to /home/kmille/Downloads/Foodsharing-Abholung-Sat-22.04.ics
kmille@linbox:foodsharing cat /home/kmille/Downloads/Foodsharing-Abholung-Wed-12.04.ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:ics.py - http://git.io/lLljaA
BEGIN:VEVENT
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Foodsharing: Fruchthof Berlin
TRIGGER;VALUE=DATE-TIME:20230412T035000Z
END:VALARM
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Foodsharing: Fruchthof Berlin
TRIGGER;VALUE=DATE-TIME:20230411T045000Z
END:VALARM
DTEND:20230412T065000Z
DTSTART:20230412T045000Z
SUMMARY:Foodsharing: Fruchthof Berlin
UID:f48e0981-138a-40ca-a6ff-041f97eee0d7@f48e.org
END:VEVENT
END:VCALENDAR%
kmille@linbox:foodsharing
```

### When is the next free slot for a store?
```bash
kmille@linbox:foodsharing poetry run python foodsharing/__init__.py -s 2418
No free pickup available
kmille@linbox:foodsharing poetry run python foodsharing/__init__.py -s 1082
{
    "date": "2023-04-07T19:50:00+02:00",
    "totalSlots": 1,
    "occupiedSlots": [],
    "isAvailable": true
}
```

### Monitoring with py3status


```python
import foodsharing
import arrow

DELAY_SECONDS = 60 * 30


class Py3status:

    def monitor_host(self):

        store_id = "2418" # Donuts
        #store_id = "1082"  # LeCrobag

        next_free_pickup = foodsharing.get_next_free_pickup(store_id)
        if not next_free_pickup:
            return {'full_text': "🍩 noslot",
                    'color': self.py3.COLOR_BAD,
                    'cached_until': self.py3.time_in(seconds=DELAY_SECONDS)
                    }
        pickup_date = arrow.get(next_free_pickup['date'])
        now = arrow.now()
        next_free_slot_in_days = (pickup_date - now).days

        return {'full_text': f"🍩 {next_free_slot_in_days}d",
                'color': self.py3.COLOR_GOOD,
                'cached_until': self.py3.time_in(seconds=DELAY_SECONDS)
                }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
```
