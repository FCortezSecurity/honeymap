import ipaddress
from dataclasses import replace

import geoip2.database
import geoip2.errors


def is_public(ip):
    """True if this is a normal internet address that could have a location."""
    try:
        return ipaddress.ip_address(ip).is_global
    except ValueError:
        return False


class GeoLookup:
    """Looks up an IP in the DB-IP databases. Anything missing comes back absent."""

    def __init__(self, city_db_path, asn_db_path):
        self.city_reader = geoip2.database.Reader(city_db_path)
        self.asn_reader = geoip2.database.Reader(asn_db_path)

    def lookup(self, ip):
        result = {}
        try:
            r = self.city_reader.city(ip)
            result["country"] = r.country.name
            result["city"] = r.city.name
            result["lat"] = r.location.latitude
            result["lon"] = r.location.longitude
        except geoip2.errors.AddressNotFoundError:
            pass
        try:
            r = self.asn_reader.asn(ip)
            result["asn"] = r.autonomous_system_number
            result["org"] = r.autonomous_system_organization
        except geoip2.errors.AddressNotFoundError:
            pass
        return result


def enrich_event(event, lookup):
    """Return a copy of the event with location data, or the event itself if private."""
    if not is_public(event.src_ip):
        return event
    return replace(event, **lookup(event.src_ip))