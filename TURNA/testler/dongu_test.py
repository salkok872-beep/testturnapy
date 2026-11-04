
from pathlib import Path
import sys

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici

kaynak = """
sayı = 1

iken sayı <= 5:
    yazdır(sayı)
    sayı = sayı + 1

yazdır("Döngü tamamlandı!")
"""

tokenlar = Lexer(kaynak).tara()
program = Parser(tokenlar).program()

yorumlayici = Yorumlayici()
yorumlayici.calistir(program)
