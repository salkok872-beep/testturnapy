
import sys
from pathlib import Path

# TURNA ana klasörünü Python'un arama yoluna ekle
ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer


kaynak_kod = '''
isim = "Merhaba Turna!"
yaş = 25
aktif = Doğru

eğer yaş >= 18:
    yazdır(isim)
'''

print("=== TURNA LEXER TESTİ ===")

lexer = Lexer(kaynak_kod)
tokenlar = lexer.tara()

for token in tokenlar:
    print(token)

print("\n=== TEST TAMAMLANDI ===")
