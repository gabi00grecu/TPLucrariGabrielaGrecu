import base64
import re
from urllib.parse import unquote

s = "Salut"

b = s.encode()          # bytes

print(b, b[0])          # b"Salut" 83

# Exercitiul 1. Student: Grecu Gabriela
# TODO: tipareste b.hex() si refa bytes din hex
# cu bytes.fromhex(...)

h = b.hex()
print(h)
print(bytes.fromhex(h))


# Exercitiul 2. Student: Grecu Gabriela

def ghici_strat(s):
    # TODO: daca are %xx -> "url"
    if "%" in s:
        return "url"

    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"

    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"

    return "necunoscut"


print(ghici_strat("%2Fetc"))   # url
print(ghici_strat("48656c6c6f"))  # hex


# Exercitiul 3. Student: Grecu Gabriela

def desfa(s):
    strat = ghici_strat(s)

    # TODO: pentru fiecare strat, decodeaza
    if strat == "base64":
        rezultat_bytes = base64.b64decode(s)
    elif strat == "hex":
        rezultat_bytes = bytes.fromhex(s)
    elif strat == "url":
        rezultat_bytes = unquote(s).encode()
    else:
        rezultat_bytes = s.encode()

    return strat, rezultat_bytes


# Exercitiul 4. Student: Grecu Gabriela

def citibil(b): 
    # TODO: True daca toti octetii sunt 32..126 
    return all(32 <= c < 127 for c in b) 

val = "NTM1OTU3NTk=" 

for _ in range(8): 
    strat, b = desfa(val) 
    
    # TODO: daca citibil(b): opreste si tipareste
    if citibil(b):
        print("Gasit:", b.decode())
        break
    #       altfel val = b.decode(); continua 
    else:
        val = b.decode()


# Exercitiul 5. Student: Grecu Gabriela

def citibil(b):
    return all(32 <= c < 127 for c in b)

date = open("probe/xor.bin", "rb").read() 

for k in range(256): 
    clar = bytes(b ^ k for b in date) 
    
    # Dacă textul decodat arată a text citibil, afișează cheia și mesajul
    if citibil(clar): 
        print("cheie:", k, clar.decode(errors="ignore"))
        break


# Exercitiul 6. Student: Grecu Gabriela

import hashlib 

tinta = open("probe/hashuri.txt").readline().strip() 

print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256 

for cuv in open("probe/wordlist.txt", encoding="latin1"): 

    cuv = cuv.strip() 

    # TODO: daca hashlib.md5(cuv.encode()).hexdigest() 

    #       == tinta: print("gasit:", cuv); break 
    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break

# Exercitiul 7. Student: Grecu Gabriela

import argparse 
import json 
import base64 
from urllib.parse import unquote 

def ghici_strat(s): 
    if '%' in s: 
        return "url" 
    if len(s) % 2 == 0:
        try:
            bytes.fromhex(s)
            return "hex"
        except ValueError:
            pass
    try:
        # Verificare simplă base64
        if all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in s):
            return "base64"
    except Exception:
        pass
    return "necunoscut"

def desfa(s): 
    strat = ghici_strat(s) 
    if strat == "base64":
        rezultat_bytes = base64.b64decode(s)
    elif strat == "hex":
        rezultat_bytes = bytes.fromhex(s)
    elif strat == "url":
        rezultat_bytes = unquote(s).encode()
    else:
        rezultat_bytes = s.encode()
    return strat, rezultat_bytes

p = argparse.ArgumentParser() 
p.add_argument("intrare")          # sir sau cale 
p.add_argument("--fisier", action="store_true") 
a = p.parse_args() 

# TODO: daca a.fisier, citeste octetii din cale; altfel trateaza intrarea ca sir 
if a.fisier:
    with open(a.intrare, "rb") as f:
        continut_bytes = f.read()
    # Dacă citim dintr-un fișier binar, putem stoca reprezentarea hex sau text
    strat = "fisier_binar"
    rezultat = continut_bytes.hex()
else:
    strat, rezultat_bytes = desfa(a.intrare)
    rezultat = rezultat_bytes.decode(errors="ignore")

# TODO: salveaza {strat, rezultat} in arsenal/forensics/fisa.json 
data_de_salvat = {
    "strat": strat,
    "rezultat": rezultat
}

import os
os.makedirs("arsenal/forensics", exist_ok=True)
with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
    json.dump(data_de_salvat, f, indent=4)

print("Rezultat salvat cu succes în arsenal/forensics/fisa.json")