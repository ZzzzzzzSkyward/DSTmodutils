SymbolMap: dict[str: list[str]] = {
    "swap_frozen": ["frozen"],
    "swap_object": ["swap_spear", "swap_axe", "swap_spear", "swap_lantern"],
    "swap_hat": ["hat_ice"],
    "SWAP_BODY": ["swap_body"],
    "SWAP_BODY_TALL": ["swap_body_tall"],
    "BEARD": ["beardsilk_long", "beard_long"],
    "LANTERN_OVERLAY": ["lantern_overlay"],

}

def GetSwapSymbol(symbol: str):
    for swap_symbol, mapping in SymbolMap.items():
        if symbol in mapping or symbol.lower() in mapping:
            return swap_symbol.lower()

    return symbol.lower()