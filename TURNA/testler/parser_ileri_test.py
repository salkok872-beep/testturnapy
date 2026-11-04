
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.turna_ast import (
    Atama,
    IkiliIslem,
    Sayi,
    Mantiksal
)


def agaci_goster(dugum):
    if isinstance(dugum, Sayi):
        return str(dugum.deger)

    if isinstance(dugum, Mantiksal):
        return str(dugum.deger)

    if isinstance(dugum, IkiliIslem):
        return (
            f"{dugum.operator}("
            f"{agaci_goster(dugum.sol)}, "
            f"{agaci_goster(dugum.sag)})"
        )

    return str(dugum)


kaynak = """
a = 10 + 20 * 3
b = (10 + 20) * 3
c = 5 >= 3
d = Doğru ve Yanlış
e = Doğru veya Yanlış
"""

print("=== TURNA İLERİ PARSER TESTİ ===")

tokenlar = Lexer(kaynak).tara()
program = Parser(tokenlar).program()

for ifade in program.ifadeler:
    print(
        ifade.isim,
        "=",
        agaci_goster(ifade.deger)
    )

print("\n=== TEST TAMAMLANDI ===")
