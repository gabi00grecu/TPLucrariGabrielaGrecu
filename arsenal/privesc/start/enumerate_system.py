
import argparse, json, os 

  

def citeste_linii(cale): 
	with open(cale, encoding="utf-8") as f: 

        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #  

		return[linie.strip() for linie in f if linie.strip() and not linie.strip().startswith("#")]  

cai = citeste_linii("start/suid.txt") 

print("linii SUID:", len(cai)) 
