
class TurnaHatasi(Exception):
    def __init__(
        self,
        kod,
        baslik,
        mesaj,
        satir=None,
        sutun=None,
        dosya=None,
        oneriler=None
    ):
        self.kod = kod
        self.baslik = baslik
        self.mesaj = mesaj
        self.satir = satir
        self.sutun = sutun
        self.dosya = dosya
        self.oneriler = oneriler or []

        super().__init__(mesaj)

    def raporla(self):
        print()
        print("=" * 45)
        print(f"TURNA HATASI - {self.kod}")
        print(self.baslik)
        print("=" * 45)

        if self.dosya:
            print(f"Dosya: {self.dosya}")

        if self.satir is not None:
            print(f"Satır: {self.satir}")

        if self.sutun is not None:
            print(f"Sütun: {self.sutun}")

        print()
        print(self.mesaj)

        if self.oneriler:
            print()
            print("Çözüm önerileri:")

            for oner in self.oneriler:
                print(f"- {oner}")

        print("=" * 45)


class LexerHatasi(TurnaHatasi):
    pass


class ParserHatasi(TurnaHatasi):
    pass


class CalismaZamaniHatasi(TurnaHatasi):
    pass
