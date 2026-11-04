
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici
from cekirdek.hatalar import TurnaHatasi


programlar = {
    "Tanımsız değişken": """
yazdır(bilinmeyen)
""",
    "Sıfıra bölme": """
sonuç = 10 / 0
"""
}

for baslik, kaynak in programlar.items():
    print(f"\n=== {baslik} TESTİ ===")

    try:
        tokenlar = Lexer(kaynak).tara()
        program = Parser(tokenlar).program()

        yorumlayici = Yorumlayici()
        yorumlayici.calistir(program)

        print("Beklenmeyen şekilde başarılı.")

    except TurnaHatasi as hata:
        hata.raporla()

print("\n=== HATA TESTLERİ TAMAMLANDI ===")
