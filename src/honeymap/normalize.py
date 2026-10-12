LOGTYPES = {
    4002: "ssh",
    3001: "http",
    2000: "ftp",
    6001: "telnet",
    8001: "mysql",
}


def service_for(logtype):
    return LOGTYPES.get(logtype, "other")