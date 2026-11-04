
import argparse
import sys
from pathlib import Path

from cekirdek.lexer import Lexer
from cekirdek.parser import Parser
from cekirdek.yorumlayici import Yorumlayici


SURUM = "0.1.0"


def turkce_konsol():
    """Windows konsolunda UTF-8 kullanmaya çalışır."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass


def kaynak_calistir(kaynak, yorumlayici):
    """TURNA kaynak kodunu yorumlar."""
    tokenlar = Lexer(kaynak).tara()
    program = Parser(tokenlar).program()

    return yorumlayici.calistir(program)


def dosya_calistir(dosya):
    yol = Path(dosya)

    if not yol.exists():
        print(f"TURNA Hatası: '{dosya}' dosyası bulunamadı.")
        return 1

    if not yol.is_file():
        print(f"TURNA Hatası: '{dosya}' bir dosya değil.")
        return 1

    try:
        kaynak = yol.read_text(encoding="utf-8")
        yorumlayici = Yorumlayici()
        kaynak_calistir(kaynak, yorumlayici)
        return 0

    except Exception as hata:
        print(hata, file=sys.stderr)
        return 1


def banner():
    print("=" * 40)
    print("         TURNA PROGRAMLAMA DİLİ")
    print("=" * 40)
    print(f"TURNA {SURUM}")
    print("Komutları yazabilir, kod çalıştırabilirsin.")
    print("Çıkmak için 'çıkış' yaz.")
    print("Çok satırlı blokları bitirmek için boş satır bırak.")
    print()


def interaktif():
    yorumlayici = Yorumlayici()
    kaynak_satirlari = []

    banner()

    while True:
        try:
            if kaynak_satirlari:
                satir = input("... ")
            else:
                satir = input(">>> ")

        except (EOFError, KeyboardInterrupt):
            print("\nTURNA konsolundan çıkılıyor.")
            break

        komut = satir.strip()

        if not kaynak_satirlari:
            if komut in ("çıkış", "exit", "quit"):
                print("Görüşürüz!")
                break

            if komut in ("temizle", "clear"):
                print("\033[2J\033[H", end="")
                continue

            if not komut:
                continue

        # Çok satırlı kodun boş satırla tamamlandığını kabul et.
        if kaynak_satirlari and not komut:
            kaynak = "\n".join(kaynak_satirlari) + "\n"
            kaynak_satirlari.clear()

            try:
                kaynak_calistir(kaynak, yorumlayici)
            except Exception as hata:
                print(hata, file=sys.stderr)

            continue

        kaynak_satirlari.append(satir)

        # Tek satırlık ifadeleri hemen çalıştır.
        if (
            len(kaynak_satirlari) == 1
            and not satir.rstrip().endswith(":")
        ):
            try:
                kaynak_calistir(satir + "\n", yorumlayici)
            except Exception as hata:
                print(hata, file=sys.stderr)

            kaynak_satirlari.clear()


def ana():
    turkce_konsol()

    ayrıştırıcı = argparse.ArgumentParser(
        prog="turna",
        description="TURNA programlama dili"
    )

    ayrıştırıcı.add_argument(
        "dosya",
        nargs="?",
        help="Çalıştırılacak .trn dosyası"
    )

    ayrıştırıcı.add_argument(
        "-c",
        "--code",
        help="Doğrudan TURNA kodu çalıştır"
    )

    ayrıştırıcı.add_argument(
        "--interactive",
        action="store_true",
        help="Etkileşimli konsolu aç"
    )

    ayrıştırıcı.add_argument(
        "--version",
        action="version",
        version=f"TURNA {SURUM}"
    )

    ayrıştırıcı.add_argument(
        "--run",
        dest="calistirilacak_dosya",
        help="Belirtilen TURNA dosyasını çalıştır"
    )

    args = ayrıştırıcı.parse_args()

    if args.code is not None:
        try:
            kaynak_calistir(args.code, Yorumlayici())
            return 0
        except Exception as hata:
            print(hata, file=sys.stderr)
            return 1

    if args.calistirilacak_dosya:
        return dosya_calistir(args.calistirilacak_dosya)

    if args.dosya:
        return dosya_calistir(args.dosya)

    interaktif()
    return 0


if __name__ == "__main__":
    sys.exit(ana())
