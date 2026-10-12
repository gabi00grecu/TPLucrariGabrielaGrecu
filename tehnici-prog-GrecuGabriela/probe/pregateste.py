"""Genereaza probele pentru laboratorul de forensics.

Necesita Pillow: python -m pip install pillow
Ruleaza din radacina proiectului: python probe/pregateste.py
"""

from __future__ import annotations

import base64
import hashlib
import io
import zipfile
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote

from PIL import ExifTags, Image


PROBE_DIR = Path(__file__).resolve().parent


def genereaza_mesaj() -> None:
    mesaj = "Mesaj secret: probele functioneaza!"
    strat_hex = mesaj.encode("utf-8").hex()
    strat_base64 = base64.b64encode(strat_hex.encode("ascii")).decode("ascii")
    strat_url = quote(strat_base64, safe="")
    (PROBE_DIR / "mesaj.txt").write_text(strat_url + "\n", encoding="ascii")


def genereaza_xor() -> None:
    mesaj = "Felicitari! Ai descifrat mesajul XOR."
    cheie = 0x5A
    criptat = bytes(octet ^ cheie for octet in mesaj.encode("utf-8"))
    (PROBE_DIR / "xor.bin").write_bytes(criptat)


def genereaza_hashuri() -> None:
    mesaje = ("parola", "gabriela", "secret", "forensics")
    linii = [
        f"sha256:{hashlib.sha256(mesaj.encode('utf-8')).hexdigest()}"
        for mesaj in mesaje
    ]
    (PROBE_DIR / "hashuri.txt").write_text("\n".join(linii) + "\n", encoding="ascii")


def coordonate_gps(degrees: int, minutes: int, seconds: int) -> tuple:
    return (Fraction(degrees), Fraction(minutes), Fraction(seconds))


def genereaza_foto() -> None:
    imagine = Image.new("RGB", (320, 200), color=(68, 128, 180))
    exif = Image.Exif()
    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    gps_ifd[1] = "N"
    gps_ifd[2] = coordonate_gps(44, 26, 0)
    gps_ifd[3] = "E"
    gps_ifd[4] = coordonate_gps(26, 6, 0)
    exif[315] = "Laborator forensics"
    imagine.save(PROBE_DIR / "foto.jpg", format="JPEG", exif=exif)


def genereaza_png_cu_arhiva() -> None:
    imagine = Image.new("RGB", (240, 160), color=(210, 190, 120))
    png = io.BytesIO()
    imagine.save(png, format="PNG")

    arhiva = io.BytesIO()
    with zipfile.ZipFile(arhiva, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "mesaj_ascuns.txt",
            "Ai gasit arhiva adaugata dupa finalul fisierului PNG!\n",
        )

    (PROBE_DIR / "ascuns.png").write_bytes(png.getvalue() + arhiva.getvalue())


def main() -> None:
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    genereaza_mesaj()
    genereaza_xor()
    genereaza_hashuri()
    genereaza_foto()
    genereaza_png_cu_arhiva()
    print(f"Probe create in: {PROBE_DIR}")
    for nume in ("mesaj.txt", "xor.bin", "hashuri.txt", "foto.jpg", "ascuns.png"):
        cale = PROBE_DIR / nume
        print(f"  {nume}: {cale.stat().st_size} bytes")


if __name__ == "__main__":
    main()
