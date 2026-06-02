# -*- coding: utf-8 -*-
"""
Khipro Bengali Input Method - Python Implementation
Comprehensive state machine implementation of the khipro-m17n input method.
Follows the logic from bn-khipro.mim verbatim with context-aware conjunct handling.

MIT License - Copyright (c) 2024 rank_coder
"""
from typing import Dict, List, Tuple, Generator, Optional
from dataclasses import dataclass

# --------------------------
# Mapping groups (exactly as in bn-khipro.mim)
# --------------------------

SHOR: Dict[str, str] = {
    "o": "অ", "a": "আ", "i": "ই", "ii": "ঈ", "u": "উ", "uu": "ঊ", "q": "ঋ", "e": "এ", "wi": "ঐ", 
    "w": "ও", "wu": "ঔ", "ae": "অ্যা", "wa": "ওয়া", "wae": "ওয়্যা", "we": "ওয়ে", 
    "ooo": "অঃ", "off": "ঽ",
}

FKAR: Dict[str, str] = {
    "uff": "‌ু", "uuff": "‌ূ", "qff": "‌ৃ", "of": "ঽ", "af": "া", "if": "ি", "iif": "ী", 
    "uf": "ু", "uuf": "ূ", "qf": "ৃ", "ef": "ে", "wif": "ৈ", "wf": "ো", "wuf": "ৌ", 
    "aef": "্যা", "waf": "োয়া", "wef": "োয়ে", "oo": "ঃ",
}

# BYANJON with CID (Consonant ID) for context tracking
BYANJON: Dict[str, Tuple[str, int]] = {
    "k": ("ক", 1), "kh": ("খ", 2), "g": ("গ", 3), "gh": ("ঘ", 4), "ng": ("ঙ", 5),
    "c": ("চ", 6), "ch": ("ছ", 7), "j": ("জ", 8), "jh": ("ঝ", 9), "nff": ("ঞ", 10), 
    "tf": ("ট", 11), "tff": ("ঠ", 12), "df": ("ড", 13), "dff": ("ঢ", 14), "nf": ("ণ", 15), 
    "t": ("ত", 16), "th": ("থ", 17), "d": ("দ", 18), "dh": ("ধ", 19), "n": ("ন", 20), 
    "p": ("প", 21), "ph": ("ফ", 22), "b": ("ব", 23), "v": ("ভ", 24), "m": ("ম", 25), 
    "z": ("য", 26), "r": ("র", 27), "l": ("ল", 28), "sh": ("শ", 29), "sf": ("ষ", 30), 
    "s": ("স", 31), "h": ("হ", 32), "y": ("য়", 33), "rf": ("ড়", 34), "rff": ("ঢ়", 35), 
    ",,": ("়", 36), "kf": ("ক্ষ", 39), "f": ("⁌", 189), "zf": ("্য", 190),
}

# Conjunct consonant mappings (juktoborno) - complete mapping from mim file
JUKTOBORNO_MAP: Dict[Tuple[int, int], Tuple[str, int]] = {
    # Format: (PCID, CID) -> (character, new_CID)
    (1, 1): ("ক্ক", 38), (1, 2): ("ক্ষ", 39), (1, 11): ("ক্ট", 40), (1, 16): ("ক্ত", 41),
    (1, 23): ("ক্ব", 42), (1, 25): ("ক্ম", 43), (1, 30): ("ক্ষ", 39), (1, 28): ("ক্ল", 44), (1, 31): ("ক্স", 45),
    
    (3, 3): ("জ্ঞ", 65), (3, 15): ("গ্‌ণ", 46), (3, 19): ("গ্ধ", 47), (3, 20): ("গ্ন", 48),
    (3, 23): ("গ্‌ব", 49), (3, 25): ("গ্ম", 50), (3, 28): ("গ্ল", 51),
    
    (4, 20): ("ঘ্ন", 52),
    
    (5, 1): ("ঙ্ক", 53), (5, 2): ("ঙ্খ", 54), (5, 3): ("ঙ্গ", 55), (5, 4): ("ঙ্ঘ", 56),
    (5, 25): ("ঙ্ম", 57), (5, 39): ("ঙ্ক্ষ", 58),
    
    (6, 6): ("চ্চ", 59), (6, 7): ("চ্ছ", 60), (6, 10): ("চ্ঞ", 61), (6, 23): ("চ্ব", 62),
    
    (8, 8): ("জ্জ", 63), (8, 9): ("জ্ঝ", 64), (8, 10): ("জ্ঞ", 65), (8, 23): ("জ্ব", 66),
    
    (10, 6): ("ঞ্চ", 67), (10, 7): ("ঞ্ছ", 68), (10, 8): ("ঞ্জ", 69), (10, 9): ("ঞ্ঝ", 70),
    
    (11, 11): ("ট্ট", 71), (11, 23): ("ট্ব", 72), (11, 25): ("ট্ম", 73),
    
    (13, 13): ("ড্ড", 74), (13, 23): ("ড্ব", 75),
    
    (15, 11): ("ণ্ট", 77), (15, 12): ("ণ্ঠ", 78), (15, 15): ("ণ্ণ", 81),
    (15, 13): ("ণ্ড", 79), (15, 14): ("ণ্ঢ", 80), (15, 20): ("ণ্ণ", 81), (15, 23): ("ণ্ব", 82), (15, 25): ("ণ্ম", 83),
    
    (16, 11): ("ট্ট", 71), (16, 16): ("ত্ত", 84), (16, 17): ("ত্থ", 85), (16, 20): ("ত্ন", 86),
    (16, 23): ("ত্ব", 87), (16, 25): ("ত্ম", 88),
    
    (17, 23): ("থ্ব", 89),
    
    (18, 3): ("দ্‌গ", 90), (18, 4): ("দ্‌ঘ", 91), (18, 13): ("ড্ড", 74), (18, 18): ("দ্দ", 92),
    (18, 19): ("দ্ধ", 93), (18, 23): ("দ্ব", 94), (18, 24): ("দ্ভ", 95), (18, 25): ("দ্ম", 96),
    
    (19, 20): ("ধ্ন", 97), (19, 23): ("ধ্ব", 98), (19, 25): ("ধ্ম", 99),
    
    (20, 6): ("ঞ্চ", 67), (20, 7): ("ঞ্ছ", 68), (20, 8): ("ঞ্জ", 69), (20, 9): ("ঞ্ঝ", 70),
    (20, 11): ("ন্ট", 100), (20, 12): ("ন্ঠ", 101), (20, 13): ("ন্ড", 102),
    (20, 15): ("ণ্ণ", 81), (20, 16): ("ন্ত", 103), (20, 17): ("ন্থ", 104), (20, 18): ("ন্দ", 105),
    (20, 19): ("ন্ধ", 106), (20, 20): ("ন্ন", 107), (20, 23): ("ন্ব", 108), (20, 25): ("ন্ম", 109), (20, 31): ("ন্স", 110),
    
    (21, 11): ("প্ট", 111), (21, 16): ("প্ত", 112), (21, 20): ("প্ন", 113), (21, 21): ("প্প", 114),
    (21, 28): ("প্ল", 115), (21, 31): ("প্স", 116),
    
    (22, 28): ("ফ্ল", 117),
    
    (23, 8): ("ব্জ", 118), (23, 18): ("ব্দ", 119), (23, 19): ("ব্ধ", 120), (23, 23): ("ব্ব", 121), (23, 28): ("ব্ল", 122),
    
    (24, 23): ("ভ্ব", 123), (24, 28): ("ভ্ল", 124),
    
    (25, 20): ("ম্ন", 125), (25, 21): ("ম্প", 126), (25, 22): ("ম্ফ", 127), (25, 23): ("ম্ব", 128),
    (25, 24): ("ম্ভ", 129), (25, 25): ("ম্ম", 130), (25, 28): ("ম্ল", 131),
    
    (28, 1): ("ল্ক", 132), (28, 3): ("ল্গ", 133), (28, 11): ("ল্ট", 134), (28, 13): ("ল্ড", 135),
    (28, 21): ("ল্প", 136), (28, 22): ("ল্ফ", 137), (28, 23): ("ল্ব", 138), (28, 24): ("ল্‌ভ", 139),
    (28, 25): ("ল্ম", 140), (28, 28): ("ল্ল", 141),
    
    (29, 6): ("শ্চ", 142), (29, 7): ("শ্ছ", 143), (29, 20): ("শ্ন", 144), (29, 23): ("শ্ব", 145),
    (29, 25): ("শ্ম", 146), (29, 28): ("শ্ল", 147),
    
    (30, 1): ("ষ্ক", 148), (30, 11): ("ষ্ট", 149), (30, 12): ("ষ্ঠ", 150), (30, 15): ("ষ্ণ", 151),
    (30, 20): ("ষ্ণ", 151), (30, 21): ("ষ্প", 152), (30, 22): ("ষ্ফ", 153), (30, 23): ("ষ্ব", 154), (30, 25): ("ষ্ম", 155),
    
    (31, 1): ("স্ক", 156), (31, 2): ("স্খ", 157), (31, 11): ("স্ট", 158), (31, 16): ("স্ত", 159),
    (31, 17): ("স্থ", 160), (31, 20): ("স্ন", 161), (31, 21): ("স্প", 162), (31, 22): ("স্ফ", 163),
    (31, 23): ("স্ব", 164), (31, 25): ("স্ম", 165), (31, 28): ("স্ল", 166),
    
    (32, 15): ("হ্ণ", 168), (32, 20): ("হ্ন", 167), (32, 23): ("হ্ব", 169), (32, 25): ("হ্ম", 170), (32, 28): ("হ্ল", 171),
    
    (34, 3): ("ড়্‌গ", 76),
    
    (39, 15): ("ক্ষ্ণ", 172), (39, 20): ("ক্ষ্ণ", 172), (39, 23): ("ক্ষ্ব", 173), (39, 25): ("ক্ষ্ম", 174),
    
    (27, 26): ("র‍্য", 37),  # র + য = র‍্য
}

PHOLA: Dict[str, int] = {
    "r": 27,  # র-ফলা
    "z": 26,  # য-ফলা
}

KAR: Dict[str, str] = {
    "o": "", "of": "অ", "oof": "ঽ", "a": "া", "af": "আ", "i": "ি", "if": "ই",
    "ii": "ী", "iif": "ঈ", "u": "ু", "uf": "উ", "uu": "ূ", "uuf": "ঊ",
    "q": "ৃ", "qf": "ঋ", "e": "ে", "ef": "এ", "wi": "ৈ", "wif": "োই",
    "w": "ো", "wf": "ও", "wu": "ৌ", "wuf": "োউ", "ae": "্যা", "aef": "অ্যা",
    "uff": "‌ু", "uuff": "‌ূ", "qff": "‌ৃ", "we": "োয়ে", "wef": "ওয়ে",
    "waf": "ওয়া", "wa": "োয়া", "wae": "ওয়্যা", "oo": "ঃ",
}

ONGKO: Dict[str, str] = {
    ".1": ".१", ".2": ".२", ".3": ".३", ".4": ".४", ".5": ".५", ".6": ".६", 
    ".7": ".७", ".8": ".८", ".9": ".९", ".0": ".०",
    "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", "0": "०",
    "1.": "१.", "2.": "२.", "3.": "३.", "4.": "४.", "5.": "५.", "6.": "६.",
    "7.": "७.", "8.": "८.", "9.": "९.", "0.": "०.",
    "1..": "१।", "2..": "२।", "3..": "३।", "4..": "४।", "5..": "५।", "6..": "६।",
    "7..": "७।", "8..": "८।", "9..": "९।", "0..": "०।",
}

DIACRITIC: Dict[str, str] = {
    "qq": "্", "xx": "্‌", "x": "ং", "`": "`", "``": "‌", "```": "``", "``f": "‍",
}

BIRAM: Dict[str, str] = {
    ".": "।", "...": "...", "..": ".", "$": "৳", "$f": "₹", ",,,": ",,", 
    ".f": "॥", ".ff": "৺", "+": "+", "-": "-", "+f": "×", "-f": "÷", "$$": "$", "=": "=", "=f": "≠",
}

PRITHAYOK: Dict[str, str] = {
    ";": "",
}

AE: Dict[str, str] = {
    "ae": "‍్్యా",
}

SLICER: Dict[str, str] = {
    "/": "/",
}

SLICER2: Dict[str, str] = {
    "//": "/",
}

SLICER3: Dict[str, str] = {
    "///": "//",
}

# All groups combined
GROUP_MAPS: Dict[str, Dict] = {
    "shor": SHOR,
    "fkar": FKAR,
    "diacritic": DIACRITIC,
    "slicer": SLICER,
    "slicer2": SLICER2,
    "slicer3": SLICER3,
    "prithayok": PRITHAYOK,
    "ongko": ONGKO,
    "biram": BIRAM,
    "byanjon": {k: v[0] for k, v in BYANJON.items()},  # Extract just characters for basic matching
    "phola": {str(k): str(v) for k, v in PHOLA.items()},  # Simple string map
    "kar": KAR,
}

# State names
INIT = "init"
SHOR_STATE = "shor-state"
REPH_STATE = "reph-state"
BYANJON_STATE = "byanjon-state"
JUKTOBORNO_STATE = "juktoborno-state"
RR_STATE = "rr-state"

# Precompute max key length per group
MAXLEN_PER_GROUP: Dict[str, int] = {
    g: max((len(k) for k in m.keys()), default=0) 
    for g, m in GROUP_MAPS.items()
}


@dataclass
class InputState:
    """Context state for the input method"""
    state: str = INIT
    output: str = ""
    
    # Context variables from MIM
    CID: int = 0          # Current Consonant ID
    PCID: int = 0         # Previous Consonant ID
    P2CID: int = 0        # Previous-Previous Consonant ID
    ALTERNATE: int = 0    # For disambiguating similar conjuncts
    SLICER: int = 0       # For slicing conjuncts
    KAR: int = 0          # For marking special kar


def _find_group_and_key(state: str, text: str, i: int) -> Tuple[str, str, str]:
    """Find longest matching key in allowed groups for current state"""
    # Define allowed groups per state (matching MIM state definitions)
    state_groups = {
        INIT: ["diacritic", "slicer", "slicer3", "slicer2", "shor", "fkar", "prithayok", "ongko", "biram", "byanjon"],
        SHOR_STATE: ["diacritic", "slicer", "slicer2", "slicer3", "shor", "fkar", "biram", "prithayok", "ongko", "byanjon"],
        REPH_STATE: ["prithayok", "diacritic", "slicer", "slicer2", "slicer3", "phola", "kar"],
        BYANJON_STATE: ["prithayok", "ongko", "biram", "diacritic", "slicer", "slicer2", "slicer3", "kar", "phola", "byanjon"],
        JUKTOBORNO_STATE: ["slicer", "diacritic", "slicer2", "slicer3", "prithayok", "ongko", "biram", "kar", "phola", "byanjon"],
        RR_STATE: [],
    }
    
    allowed = state_groups.get(state, [])
    if not allowed:
        return ("", "", "")
    
    # Try greedy matching from longest to shortest
    maxlen = max((MAXLEN_PER_GROUP.get(g, 0) for g in allowed), default=0)
    end = min(len(text), i + maxlen)
    
    for L in range(end - i, 0, -1):
        chunk = text[i:i + L]
        for g in allowed:
            m = GROUP_MAPS[g]
            if chunk in m:
                return (g, chunk, m[chunk])
    
    return ("", "", "")


def _apply_transition(state: str, group: str) -> str:
    """Apply state transition based on group matched"""
    if state == INIT:
        if group in ("diacritic", "slicer", "slicer3", "slicer2", "shor", "fkar", "prithayok", "ongko", "biram"):
            return SHOR_STATE
        if group == "byanjon":
            return BYANJON_STATE
        return INIT
    
    if state == SHOR_STATE:
        if group in ("diacritic", "slicer", "slicer2", "slicer3", "shor", "fkar", "biram", "prithayok", "ongko"):
            return SHOR_STATE
        if group == "byanjon":
            return BYANJON_STATE
        return SHOR_STATE
    
    if state == REPH_STATE:
        if group in ("prithayok", "diacritic", "slicer", "slicer2", "slicer3"):
            return SHOR_STATE
        if group == "kar":
            return SHOR_STATE
        if group == "phola":
            return BYANJON_STATE
        return REPH_STATE
    
    if state == BYANJON_STATE:
        if group in ("prithayok", "ongko", "biram", "diacritic", "slicer", "slicer2", "slicer3"):
            return SHOR_STATE
        if group == "kar":
            return SHOR_STATE
        if group in ("phola", "byanjon"):
            return JUKTOBORNO_STATE
        return BYANJON_STATE
    
    if state == JUKTOBORNO_STATE:
        if group == "slicer":
            return JUKTOBORNO_STATE
        if group in ("diacritic", "slicer2", "slicer3", "prithayok", "ongko", "biram", "kar"):
            return SHOR_STATE
        if group in ("phola", "byanjon"):
            return JUKTOBORNO_STATE
        return JUKTOBORNO_STATE
    
    if state == RR_STATE:
        return BYANJON_STATE
    
    return INIT


def convert(text: str) -> str:
    """Convert ASCII input to Bengali using khipro state machine"""
    i = 0
    n = len(text)
    state_ctx = InputState()
    
    while i < n:
        group, key, val = _find_group_and_key(state_ctx.state, text, i)
        
        if not group:
            # No match: pass through and reset
            state_ctx.output += text[i]
            i += 1
            state_ctx.state = INIT
            state_ctx.CID = 0
            state_ctx.PCID = 0
            continue
        
        # ===== Handle SLICER (/) - converts to anusvara in SHOR_STATE =====
        if group == "slicer" and state_ctx.state == SHOR_STATE:
            # In SHOR_STATE: delete last char and insert anusvara ঁ
            if state_ctx.output:
                state_ctx.output = state_ctx.output[:-1] + "ঁ"
            else:
                state_ctx.output += val
            i += len(key)
            state_ctx.state = _apply_transition(state_ctx.state, group)
            continue
        
        # ===== Handle PHOLA (র-ফলা, য-ফলা) =====
        if group == "phola" and state_ctx.state == BYANJON_STATE:
            phola_cid = PHOLA.get(key)
            if phola_cid and state_ctx.PCID:
                # Check if (PCID, phola_cid) exists in JUKTOBORNO_MAP
                if (state_ctx.PCID, phola_cid) in JUKTOBORNO_MAP:
                    conjunct, new_cid = JUKTOBORNO_MAP[(state_ctx.PCID, phola_cid)]
                    # Delete previous consonant and insert conjunct with halant
                    state_ctx.output = state_ctx.output[:-1]  # Remove last consonant
                    state_ctx.output += conjunct
                    state_ctx.P2CID = state_ctx.PCID
                    state_ctx.PCID = new_cid
                    state_ctx.CID = new_cid
                else:
                    # No conjunct form, just insert halant + new consonant
                    state_ctx.output = state_ctx.output[:-1]  # Remove last consonant
                    char, cid = BYANJON.get(key, ("", phola_cid))
                    if char:
                        state_ctx.output += "्" + char  # halant + consonant
                    state_ctx.P2CID = state_ctx.PCID
                    state_ctx.PCID = cid if char else phola_cid
                    state_ctx.CID = cid if char else phola_cid
            else:
                # Fallback: just insert the character (shouldn't happen)
                state_ctx.output += val
            i += len(key)
            state_ctx.state = _apply_transition(state_ctx.state, group)
            continue
        
        # ===== Handle BYANJON (consonants) - check for conjunct formation =====
        if group == "byanjon" and key in BYANJON:
            char, cid = BYANJON[key]
            
            # If in BYANJON_STATE and we have a PCID, check for conjunct
            if state_ctx.state == BYANJON_STATE and state_ctx.PCID and (state_ctx.PCID, cid) in JUKTOBORNO_MAP:
                # Conjunct consonant formation!
                conjunct, new_cid = JUKTOBORNO_MAP[(state_ctx.PCID, cid)]
                # Replace last consonant with conjunct form
                state_ctx.output = state_ctx.output[:-1]  # Remove last consonant
                state_ctx.output += conjunct
                state_ctx.P2CID = state_ctx.PCID
                state_ctx.PCID = new_cid
                state_ctx.CID = new_cid
            else:
                # Simple consonant - just add it
                state_ctx.output += char
                state_ctx.P2CID = state_ctx.PCID
                state_ctx.PCID = cid
                state_ctx.CID = cid
            
            i += len(key)
            state_ctx.state = _apply_transition(state_ctx.state, group)
            continue
        
        # ===== Handle other groups (kar, diacritic, biram, etc.) =====
        state_ctx.output += val
        i += len(key)
        state_ctx.state = _apply_transition(state_ctx.state, group)
    
    return state_ctx.output


def type_stream(text: str) -> Generator[str, None, None]:
    """Yield converted text after each keystroke"""
    for k in range(1, len(text) + 1):
        yield convert(text[:k])


# --------------------------
# Demo
# --------------------------
if __name__ == "__main__":
    print("🔡 Khipro Typing Preview (Press Enter to quit)\n")

    while True:
        user_input = input("Type in khipro syntax: ").strip()
        if not user_input:
            break

        print("\nLive Typing:")
        for step, out in enumerate(type_stream(user_input), 1):
            print(f"{user_input[:step]!r} → {out}")
        print("-" * 40)
