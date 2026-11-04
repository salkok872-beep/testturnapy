
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.turna_ast import (
    Program,
    Atama,
    Sayi,
    IkiliIslem
)

ifade = Atama(
    "sonuç",
    IkiliIslem(
        Sayi(10),
        "ARTI",
        Sayi(20)
    )
)

program = Program([ifade])

print("TURNA AST TESTİ")
print("Program oluşturuldu.")
print("İfade sayısı:", len(program.ifadeler))
print("Değişken:", ifade.isim)
print("İşlem:", ifade.deger.operator)
print("Sol sayı:", ifade.deger.sol.deger)
print("Sağ sayı:", ifade.deger.sag.deger)
