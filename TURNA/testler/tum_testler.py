
import os
import sys
import subprocess
from pathlib import Path


ANA_KLASOR = Path(__file__).resolve().parent.parent

TESTLER = [
    "lexer_test.py",
    "lexer_ileri_test.py",
    "hata_test.py",
    "ast_test.py",
    "parser_test.py",
    "parser_ileri_test.py",
    "yorumlayici_test.py",
    "yorumlayici_hata_test.py",
    "kosul_test.py",
    "ic_ice_kosul_test.py",
]


def ana():

    print("=" * 45)
    print("          TURNA TEST SİSTEMİ")
    print("=" * 45)

    basarili = 0
    basarisiz = 0

    ortam = os.environ.copy()
    ortam["PYTHONIOENCODING"] = "utf-8"

    for dosya in TESTLER:

        yol = ANA_KLASOR / "testler" / dosya

        print()
        print("-" * 45)
        print(f"TEST: {dosya}")
        print("-" * 45)

        if not yol.exists():
            print("[BAŞARISIZ] Test dosyası bulunamadı.")
            basarisiz += 1
            continue

        try:
            sonuc = subprocess.run(
                [sys.executable, str(yol)],
                cwd=ANA_KLASOR,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=ortam,
                timeout=30,
            )

            if sonuc.stdout:
                print(sonuc.stdout, end="")

            if sonuc.stderr:
                print(sonuc.stderr, end="")

            if sonuc.returncode == 0:
                print(f"\n[BAŞARILI] {dosya}")
                basarili += 1

            else:
                print(f"\n[BAŞARISIZ] {dosya}")
                basarisiz += 1

        except subprocess.TimeoutExpired:
            print("[BAŞARISIZ] Test zaman aşımına uğradı.")
            basarisiz += 1

        except Exception as hata:
            print(f"[BAŞARISIZ] {hata}")
            basarisiz += 1

    print()
    print("=" * 45)
    print("             TEST SONUÇLARI")
    print("=" * 45)

    print(f"Toplam test : {basarili + basarisiz}")
    print(f"Başarılı    : {basarili}")
    print(f"Başarısız   : {basarisiz}")

    print("=" * 45)

    if basarisiz == 0:
        print("TÜM TEST PROGRAMLARI BAŞARIYLA ÇALIŞTI!")
    else:
        print("BAZI TESTLER BAŞARISIZ OLDU.")

    print("=" * 45)

    return 1 if basarisiz else 0


if __name__ == "__main__":
    sys.exit(ana())
