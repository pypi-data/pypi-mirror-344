# gabutcat/behavior.py

import random

def random_behavior():
    """
    Mengembalikan kebiasaan acak kucing saat gabut.
    """
    behaviors = [
        "rebahan sambil natap kosong",
        "nyakar-nyakar sofa",
        "ngejar bayangan sendiri",
        "masuk ke kardus sempit",
        "melototin cicak di dinding",
        "nendang-nendang barang di meja",
        "tidur di keyboard hooman",
        "liatin hooman makan dengan tatapan penuh harap"
    ]
    return random.choice(behaviors)

def meow():
    """
    Mengembalikan suara kucing lucu saat gabut.
    """
    sounds = ["meong...", "mew~", "nyaw~", "mrrr...", "meeoo~ng"]
    return random.choice(sounds)

