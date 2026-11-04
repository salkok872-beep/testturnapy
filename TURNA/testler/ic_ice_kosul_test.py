
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici


kaynak = """
yaş = 25

eğer yaş >= 18:

    eğer yaş >= 25:
        yazdır("25 veya daha büyük")
    değilse:
        yazdır("18 ile 24 arasında")

değilse:
    yazdır("18 yaşından küçük")
"""

tokenlar = Lexer(kaynak).tara()
program = Parser(tokenlar).program()

Yorumlayici().calistir(program)
