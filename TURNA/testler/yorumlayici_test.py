
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici


kaynak = """
isim = "Turna"
sayı = 10 + 20 * 3
sonuç = sayı >= 50

yazdır(isim)
yazdır(sayı)
yazdır(sonuç)
"""

print("=== TURNA PROGRAMI ÇALIŞIYOR ===")

tokenlar = Lexer(kaynak).tara()

program = Parser(tokenlar).program()

yorumlayici = Yorumlayici()

yorumlayici.calistir(program)

print("=== PROGRAM TAMAMLANDI ===")
