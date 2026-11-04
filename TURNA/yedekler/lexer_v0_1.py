
class Token:
    def __init__(self, tur, deger, satir, sutun):
        self.tur = tur
        self.deger = deger
        self.satir = satir
        self.sutun = sutun

    def __repr__(self):
        return (
            f"Token({self.tur}, {self.deger!r}, "
            f"satır={self.satir}, sütun={self.sutun})"
        )


class Lexer:
    ANAHTAR_KELIMELER = {
        "eğer",
        "değilse",
        "yoksa_eğer",
        "iken",
        "her",
        "içinde",
        "işlev",
        "döndür",
        "Doğru",
        "Yanlış",
        "Boş",
        "aktar",
        "durdur",
        "devam",
        "sınıf",
        "ve",
        "veya",
        "değil",
    }

    IKI_KARAKTERLI = {
        "==": "ESIT",
        "!=": "ESIT_DEGIL",
        ">=": "BUYUK_ESIT",
        "<=": "KUCUK_ESIT",
        "+=": "ARTI_ESIT",
        "-=": "EKSI_ESIT",
        "*=": "CARPI_ESIT",
        "/=": "BOL_ESIT",
        "//": "TAM_BOL",
        "**": "US",
    }

    TEK_KARAKTERLI = {
        "+": "ARTI",
        "-": "EKSI",
        "*": "CARPI",
        "/": "BOL",
        "%": "MOD",
        "=": "ATAMA",
        ">": "BUYUK",
        "<": "KUCUK",
        "(": "SOL_PARANTEZ",
        ")": "SAG_PARANTEZ",
        "[": "SOL_KOSE",
        "]": "SAG_KOSE",
        "{": "SOL_SUSLU",
        "}": "SAG_SUSLU",
        ":": "IKI_NOKTA",
        ",": "VIRGUL",
        ".": "NOKTA",
    }

    def __init__(self, kaynak):
        self.kaynak = kaynak
        self.konum = 0
        self.satir = 1
        self.sutun = 1
        self.tokenlar = []

    def ilerle(self):
        karakter = self.kaynak[self.konum]
        self.konum += 1

        if karakter == "\n":
            self.satir += 1
            self.sutun = 1
        else:
            self.sutun += 1

        return karakter

    def ekle(self, tur, deger, satir, sutun):
        self.tokenlar.append(
            Token(tur, deger, satir, sutun)
        )

    def hata(self, mesaj):
        raise SyntaxError(
            f"Lexer hatası: {mesaj} "
            f"(satır {self.satir}, sütun {self.sutun})"
        )

    def sayi_oku(self):
        baslangic = self.konum
        satir = self.satir
        sutun = self.sutun

        while (
            self.konum < len(self.kaynak)
            and self.kaynak[self.konum].isdigit()
        ):
            self.ilerle()

        if (
            self.konum < len(self.kaynak)
            and self.kaynak[self.konum] == "."
            and self.konum + 1 < len(self.kaynak)
            and self.kaynak[self.konum + 1].isdigit()
        ):
            self.ilerle()

            while (
                self.konum < len(self.kaynak)
                and self.kaynak[self.konum].isdigit()
            ):
                self.ilerle()

        deger = self.kaynak[baslangic:self.konum]
        self.ekle("SAYI", deger, satir, sutun)

    def kelime_oku(self):
        baslangic = self.konum
        satir = self.satir
        sutun = self.sutun

        while self.konum < len(self.kaynak):
            karakter = self.kaynak[self.konum]

            if karakter.isalnum() or karakter == "_":
                self.ilerle()
            else:
                break

        kelime = self.kaynak[baslangic:self.konum]

        if kelime in self.ANAHTAR_KELIMELER:
            tur = "ANAHTAR_KELIME"
        else:
            tur = "KIMLIK"

        self.ekle(tur, kelime, satir, sutun)

    def metin_oku(self):
        tirnak = self.ilerle()
        satir = self.satir
        sutun = self.sutun - 1
        sonuc = ""

        while self.konum < len(self.kaynak):
            karakter = self.ilerle()

            if karakter == tirnak:
                self.ekle("METIN", sonuc, satir, sutun)
                return

            if karakter == "\n":
                self.hata("Metin kapanmadan satır bitti")

            if karakter == "\\":
                if self.konum >= len(self.kaynak):
                    self.hata("Eksik kaçış karakteri")

                sonraki = self.ilerle()

                kacislar = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                }

                if sonraki not in kacislar:
                    self.hata("Bilinmeyen kaçış karakteri")

                sonuc += kacislar[sonraki]
            else:
                sonuc += karakter

        self.hata("Kapatılmamış metin")

    def tara(self):
        while self.konum < len(self.kaynak):
            karakter = self.kaynak[self.konum]

            if karakter in " \t\r":
                self.ilerle()
                continue

            if karakter == "\n":
                satir = self.satir
                sutun = self.sutun
                self.ilerle()
                self.ekle("SATIR_SONU", "\n", satir, sutun)
                continue

            if karakter == "#":
                while (
                    self.konum < len(self.kaynak)
                    and self.kaynak[self.konum] != "\n"
                ):
                    self.ilerle()
                continue

            if karakter.isdigit():
                self.sayi_oku()
                continue

            if karakter.isalpha() or karakter == "_":
                self.kelime_oku()
                continue

            if karakter in "\"'":
                self.metin_oku()
                continue

            ikili = self.kaynak[self.konum:self.konum + 2]

            if ikili in self.IKI_KARAKTERLI:
                satir = self.satir
                sutun = self.sutun
                self.ilerle()
                self.ilerle()
                self.ekle(
                    self.IKI_KARAKTERLI[ikili],
                    ikili,
                    satir,
                    sutun
                )
                continue

            if karakter in self.TEK_KARAKTERLI:
                satir = self.satir
                sutun = self.sutun
                self.ilerle()
                self.ekle(
                    self.TEK_KARAKTERLI[karakter],
                    karakter,
                    satir,
                    sutun
                )
                continue

            self.hata(f"Geçersiz karakter: {karakter!r}")

        self.ekle("DOSYA_SONU", None, self.satir, self.sutun)

        return self.tokenlar
