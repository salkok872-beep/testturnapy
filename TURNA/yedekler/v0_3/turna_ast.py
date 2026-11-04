
class Dugum:
    """Tüm AST düğümlerinin temel sınıfı."""
    pass


class Program(Dugum):
    def __init__(self, ifadeler):
        self.ifadeler = ifadeler


class Sayi(Dugum):
    def __init__(self, deger):
        self.deger = deger


class Metin(Dugum):
    def __init__(self, deger):
        self.deger = deger


class Mantiksal(Dugum):
    def __init__(self, deger):
        self.deger = deger


class Bos(Dugum):
    pass


class Degisken(Dugum):
    def __init__(self, isim):
        self.isim = isim


class IkiliIslem(Dugum):
    def __init__(self, sol, operator, sag):
        self.sol = sol
        self.operator = operator
        self.sag = sag


class TekliIslem(Dugum):
    def __init__(self, operator, ifade):
        self.operator = operator
        self.ifade = ifade


class Atama(Dugum):
    def __init__(self, isim, deger):
        self.isim = isim
        self.deger = deger


class Cagri(Dugum):
    def __init__(self, isim, argumanlar):
        self.isim = isim
        self.argumanlar = argumanlar


class Kosul(Dugum):
    def __init__(self, kosul, govde, alternatif=None):
        self.kosul = kosul
        self.govde = govde
        self.alternatif = alternatif


class Dongu(Dugum):
    def __init__(self, kosul, govde):
        self.kosul = kosul
        self.govde = govde


class Islev(Dugum):
    def __init__(self, isim, parametreler, govde):
        self.isim = isim
        self.parametreler = parametreler
        self.govde = govde


class Dondur(Dugum):
    def __init__(self, ifade):
        self.ifade = ifade


class Liste(Dugum):
    def __init__(self, elemanlar):
        self.elemanlar = elemanlar


class Sozluk(Dugum):
    def __init__(self, elemanlar):
        self.elemanlar = elemanlar
