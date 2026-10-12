import urllib.error
import urllib.parse
import urllib.request

URL = "http://localhost:8080/index.html"
USERS = ["root", "admin", "test", "ubuntu", "user"]
PASSWORDS = ["123456", "password", "admin", "qwerty"]

sent = 0
for user in USERS:
    for pw in PASSWORDS:
        data = urllib.parse.urlencode({"username": user, "password": pw}).encode()
        try:
            urllib.request.urlopen(URL, data=data).read()
        except urllib.error.URLError as error:
            print(f"request failed: {error}")
        sent += 1

print(f"sent {sent} login attempts")