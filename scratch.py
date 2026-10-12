import geoip2.database

with geoip2.database.Reader("data/geoip/dbip-city-lite.mmdb") as reader:
    r = reader.city("8.8.8.8")
    print(r.country.iso_code, r.country.name, r.city.name, r.location.latitude, r.location.longitude)

with geoip2.database.Reader("data/geoip/dbip-asn-lite.mmdb") as reader:
    r = reader.asn("8.8.8.8")
    print(r.autonomous_system_number, r.autonomous_system_organization)