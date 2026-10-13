import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

import time

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    pass
    build_url("example.com", "login")

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    pass
url = "https://example.com/login"
if url.startswith("https"):
    print("True")
else:
    print("False")
## sintaxa corecta ar fi return, dar programul nu se ruleaza

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    pass
import requests
url = "https://example.com/login"
r = requests.get(url)
print(type)
print(r.status_code)


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    pass
my_dict = {"status": 200, "content_type": "text/html", "length": 1256, "server": "ECS"
           }

try:
    url
except:
    print({"status": None, "error": "Try again later"})
    ##sintaxa corecta ar fi return dar nu se ruleaza programul


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass
scanner = check_site("https://example.com" "https://httpbin.org/html"
    "https://httpbin.org/json"
    "https://httpbin.org/status/200"
    "https://httpbin.org/redirect/1"
    "https://httpbin.org/delay/2")
print(f"{scanner}")




def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass
r1 =


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
