import argparse
import json
from collections import Counter
from parse_auth import citeste_esecuri

def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    # TODO: intoarce lista de (ip, n) cu n >= prag, 
    #       sortata descrescator dupa n 
    return sorted([(ip, n) for ip, n in counts.items() if n >= prag], key=lambda x: x[1], reverse=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)
    
    # TODO: cu --json, scoate json.dumps cu {esecuri, pe_ip, suspecti};
    #       fara, un rezumat cu "BRUTE FORCE" pe fiecare suspect 
    if a.json:
        rezultat = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": sus
        }
        print(json.dumps(rezultat, indent=2))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
            
        if sus:
            print(f"Suspecti (prag {a.prag}):")
            for ip, n in sus:
                print(f"  {ip}  ({n} incercari)  BRUTE FORCE")

if __name__ == "__main__":
    main()



    ##python -c "from detector import suspecti; suspecti({}, 0)" 