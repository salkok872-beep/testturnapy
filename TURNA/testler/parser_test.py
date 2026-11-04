
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser


kaynak = """
sonuç = 10 + 20 * 3
"""

print("=== TURNA PARSER TESTİ ===")

lexer = Lexer(kaynak)
tokenlar = lexer.tara()

parser = Parser(tokenlar)
program = parser.program()

print("Program başarıyla ayrıştırıldı.")
print("İfade sayısı:", len(program.ifadeler))

atama = program.ifadeler[0]

print("Değişken:", atama.isim)
print("Ana işlem:", atama.deger.operator)
print("Sol taraf:", atama.deger.sol.deger)
print(
    "Sağ taraftaki işlem:",
    atama.deger.sag.operator
)
print(
    "Çarpma işlemi:",
    atama.deger.sag.sol.deger,
    "*",
    atama.deger.sag.sag.deger
)

print("\n=== TEST TAMAMLANDI ===")
