
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.lexer import Lexer


def test_et(baslik, kaynak):
    print(f"\n=== {baslik} ===")

    try:
        tokenlar = Lexer(kaynak).tara()

        for token in tokenlar:
            print(token)

        print("TEST BAŞARILI")

    except SyntaxError as hata:
        print("BEKLENEN HATA:" if "HATA" in baslik else "HATA:")
        print(hata)


test_et(
    "İÇ İÇE GİRİNTİ",
    '''eğer Doğru:
    eğer Doğru:
        yazdır("İçeride")
    yazdır("Dışarıda")
yazdır("Bitti")
'''
)

test_et(
    "BOŞ SATIR VE YORUM",
    '''sayı = 10

# Bu bir yorumdur
yazdır(sayı)
'''
)

test_et(
    "HATALI GİRİNTİ",
    '''eğer Doğru:
   yazdır("Hata")
'''
)

test_et(
    "BOŞ DOSYA",
    ""
)
