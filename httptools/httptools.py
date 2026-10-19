import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
server."""

    r = requests.get(BASE +"/get", params=params)
    return r.json()["args"]
    print(r.url) # https://httpbin.org/get?q=python&page=2
    print(r.json()["args"]) # {'q': 'python', 'page': '2'}


def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu
parametri."""
    r = requests.get(BASE + "/get", params = params)
    return r.url


# Partea 2: anteturi

def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
server."""
    r = requests.get(BASE + "/headers", headers = {"User-Agent": agent})
    return r.json()["User-Agent"]
    

def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""

    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]
    print(r.json()["headers"]["User-Agent"]) 

# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
server."""
    r = requests.post(BASE + "/post", json = data)
    return r.json()["json"]

def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de
server."""
    r = requests.post(BASE + "/post", data = data)
    return r.json()["form"]

    print(r.json()["json"]) 
    print(r.json()["form"]) 
    
# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau
'eroare server'."""
    r = requests.get(f"{BASE}/status/{code}")
    if 200 <= r.status_code <= 300:
        return   "succes"
    elif 400 <= r.status_code <= 500:
        return "eroare client"
    elif 500 <= r.status_code <= 600:
        return "eroare server"
    return "necunoscut"

def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
False."""
    print(r.status_code)
    try:
        r = requests.get(f"{BASE}/status/{code}")
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False
    print("a eșuat:", e)



# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost urmate."""
    r = requests.get(f"{BASE}/redirect/{n}")
    return len(r.history)

def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""        
    r = requests.get(f"{BASE}/redirect/{n}")
    return r.url

def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
Location."""    
    r = requests.get(f"{BASE}/redirect/{n}", allow_redirects = False)
    return r.headers.get("Location")

    print(r.status_code) # 302
    print(r.headers["Location"]) # unde voia serverul să te trimită


# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ sesiune."""
    with requests.Session() as s:
        s.get(f"{BASE}/cookies/set?{name}={value}")
        r = s.get(BASE + "/cookies")
        return r.json()["cookies"]

def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie-urile văzute de server."""
    requests.get(f"{BASE}/cookies/set?{name}={value}")
    r = requests.get(BASE + "/cookies")
    return r.json()["cookies"]


# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    url = BASE + path
    try:
        r = requests.get(url, timeout=3)
        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": round(r.elapsed.total_seconds(), 2),
            "content_type": r.headers.get("Content-Type", "").split(";")[0],
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}

def main():
    results = []
    success_count = 0
    fail_count = 0

    for path in PATHS:
        rep = report(path)
        rep["path"] = path
        results.append(rep)
        
        if rep.get("status") == 200:
            success_count += 1
            print(f"{path} -> 200, {rep['seconds']} secunde")
        else:
            fail_count += 1

    print(f"Reușite: {success_count} | Eșuate: {fail_count}")


# Partea 8 (Bonus): Autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel False."""
    try:
        r = requests.get(f"{BASE}/basic-auth/admin/secret", auth=(user, password))
        return r.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    main()
