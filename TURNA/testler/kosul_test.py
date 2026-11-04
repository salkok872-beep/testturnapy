
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici


kaynak = """
yaş = 20

eğer yaş >= 18:
    yazdır("Yetişkinsin!")
değilse:
    yazdır("Henüz yetişkin değilsin.")
"""

print("=== TURNA KOŞUL TESTİ ===")

tokenlar = Lexer(kaynak).tara()

program = Parser(tokenlar).program()

yorumlayici = Yorumlayici()

yorumlayici.calistir(program)

print("=== TEST TAMAMLANDI ===")
