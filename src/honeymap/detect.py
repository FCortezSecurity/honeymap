from collections import defaultdict
from datetime import timedelta

from .models import Alert


def find_brute_force(events, threshold=10, window=timedelta(minutes=5)):
    # Group login attempts by (who, which service)
    groups = defaultdict(list)
    for event in events:
        if event.event_type == "login_attempt":
            groups[(event.src_ip, event.service)].append(event)

    alerts = []
    for (ip, service), attempts in groups.items():
        attempts.sort(key=lambda e: e.ts)  # oldest first

        i = 0
        while i < len(attempts):
            # Find how many attempts fall within `window` of attempt i
            j = i
            while j + 1 < len(attempts) and attempts[j + 1].ts - attempts[i].ts <= window:
                j += 1

            count = j - i + 1
            if count >= threshold:
                alerts.append(
                    Alert(
                        rule="brute_force",
                        severity="high" if count >= 50 else "medium",
                        src_ip=ip,
                        service=service,
                        first_seen=attempts[i].ts,
                        last_seen=attempts[j].ts,
                        event_count=count,
                        source=attempts[i].source,
                    )
                )
                i = j + 1  # skip past this burst so it's one alert, not many
            else:
                i += 1

    return alerts