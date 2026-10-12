# Exercitiul 7. Student: Grecu Gabriela

def tip_real(cale): 
    cap = open(cale, "rb").read(8) 

    # TODO: daca cap incepe cu b"%PDF" -> "pdf" 

    #       b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg" 

    #       b"PK\x03\x04" -> "zip/docx" 
    if cap.startswith(b"%PDF"):
        return "pdf"    
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex() 

print(tip_real("probe/foto.jpg")) 

# Exercitiul 2. Student: Grecu Gabriela

import re 

date = open("probe/ascuns.png", "rb").read() 

# TODO: for m in re.findall(rb"[ -~]{4,}", date): 

#           print(m.decode()) 

# cauta un indiciu: o cale, un mesaj, un nume de fisier 

for m in re.findall(rb"[ -~]{4,}", date): 
    print(m.decode(errors = "ignore"))

# Exercitiul 3. Student: Grecu Gabriela

from PIL import Image 

from PIL.ExifTags import TAGS 

exif = Image.open("probe/foto.jpg")._getexif() or {} 

for id, val in exif.items(): 

    print(TAGS.get(id, id), "=", val) 

# TODO: ia blocul GPS (tag 34853) si tipareste 

#       latitudinea si longitudinea 
index_gps = 34853
if index_gps in exif:
    gps_info = exif[index_gps]
    lat = gps_info[2]  # Latitude
    lon = gps_info[4]  # Longitude
    print("Latitude:", lat)
    print("Longitude:", lon)



# Exercitiul 4. Student: Grecu Gabriela

date = open("probe/ascuns.png", "rb").read() 

i = date.find(b"PK\x03\x04") 

# TODO: daca i != -1: 

#   open("gasit.zip","wb").write(date[i:]) 

#   print("arhiva extrasa de la octetul", i) 

# apoi dezarhiveaza si vezi ce era inauntru 
if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)


# Exercitiul 5. Student: Grecu Gabriela

from PIL import Image 

img = Image.open("probe/foto.jpg").convert("RGB") 
px = list(img.getdata()) 
mesaj = b"FLAG{ascuns_in_pixeli}" 
biti = "".join(f"{x:08b}" for x in mesaj) 

# TODO: pentru fiecare bit, ia un canal si pune 
#   canal = (canal & ~1) | int(bit) 
px_nou = []
bit_idx = 0

for r, g, b in px:
    if bit_idx < len(biti):
        r = (r & ~1) | int(biti[bit_idx])
        bit_idx += 1
    if bit_idx < len(biti):
        g = (g & ~1) | int(biti[bit_idx])
        bit_idx += 1
    if bit_idx < len(biti):
        b = (b & ~1) | int(biti[bit_idx])
        bit_idx += 1
    px_nou.append((r, g, b))

# TODO: img.putdata(px_nou); img.save("stego.png") 
img.putdata(px_nou) 
img.save("stego.png")


# Exercitiul 6. Student: Grecu Gabriela

from PIL import Image

px = list(Image.open("stego.png").convert("RGB").getdata()) 

biti = "" 

for (r, g, b) in px: 
    # Adună ultimii biți (r&1, g&1, b&1) 
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

# Grupează câte 8 biți -> octeți -> text, oprindu-te la primul octet 0
octeti = bytearray()
for i in range(0, len(biti), 8):
    octet = int(biti[i:i+8], 2)
    if octet == 0:
        break
    octeti.append(octet)

print("Mesaj decodat:", octeti.decode(errors="ignore"))
