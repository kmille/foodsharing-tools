# python + foodsharing

This module uses your browser cookies, so you need to be logged in to Foodsharing. There are two features:

```bash
kmille@linbox:foodsharing poetry run python foodsharing/__init__.py -h
usage: foodsharing/__init__.py [-h] [-e] [-s STORE]

options:
  -h, --help            show this help message and exit
  -e, --export          Export ics file for all of pickups to ~/Downloads
  -s STORE, --store STORE
                        Show info about next free slot for given store_id
```

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


TODO: export

I use it in py3status:

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
