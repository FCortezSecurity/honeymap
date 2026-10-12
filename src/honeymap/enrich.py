import ipaddress


def is_public(ip):
    """True if this is a normal internet address that could have a location."""
    try:
        return ipaddress.ip_address(ip).is_global
    except ValueError:
        return False