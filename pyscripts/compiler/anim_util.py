import os

FRAME_RATE = 30

FACING_RIGHT = 1<<0
FACING_UP = 1<<1
FACING_LEFT = 1<<2
FACING_DOWN = 1<<3
FACING_UPRIGHT = 1<<4
FACING_UPLEFT = 1<<5
FACING_DOWNRIGHT = 1<<6
FACING_DOWNLEFT = 1<<7

SCALE_FACTOR = 1.0
EXPORT_DEPTH = 10

faceing_dir = {
    FACING_UP: "_up",
    FACING_DOWN: "_down",
    FACING_LEFT | FACING_RIGHT: "_side",
    FACING_LEFT: "_left",
    FACING_RIGHT: "_right",
    FACING_UPLEFT | FACING_UPRIGHT: "_upside",
    FACING_DOWNLEFT | FACING_DOWNRIGHT: "_downside",
    FACING_UPLEFT: "_upleft",
    FACING_UPRIGHT: "_upright",
    FACING_DOWNLEFT: "_downleft",
    FACING_DOWNRIGHT: "_downright",
    FACING_UPLEFT | FACING_UPRIGHT | FACING_DOWNLEFT | FACING_DOWNRIGHT: "_45s",
    FACING_UP | FACING_DOWN | FACING_LEFT | FACING_RIGHT: "_90s"
}

def try_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def strhash(str, hash_dict):
    hash = 0
    for c in str:
        v = ord(c.lower())
        hash = (v + (hash << 6) + (hash << 16) - hash) & 0xFFFFFFFF
    hash_dict[hash] = str
    return hash

def round_up(a, b=0):
    assert b <= 0

    if b == 0:
        add = 0.5 if a >= 0 else -0.5
        return int(a + add)
    elif b < 0:
        mul = 10 ** -b
        add = 0.5 * 10 ** b
        add = add if a >= 0 else -add
        return int((a + add) * mul) / mul
    return a