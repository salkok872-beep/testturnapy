
import sys
from pathlib import Path

ANA_KLASOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ANA_KLASOR))

from cekirdek.hatalar import ParserHatasi

hata = ParserHatasi(
    kod="TR002",
    baslik="Beklenmeyen ifade",
    mesaj="Koşulun sonunda iki nokta bekleniyordu.",
    satir=2,
    sutun=17,
    dosya="program.trn",
    oneriler=[
        "Koşulun sonuna iki nokta (:) ekleyin.",
        "Sözdizimi kurallarını kontrol edin."
    ]
)

hata.raporla()
