# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple, Generator

# --------------------------
# Mapping groups (exactly as provided)
# --------------------------
from khipro_mappings import *

# --------------------------
# State machine configuration
# --------------------------

INIT = "init"
SHOR_STATE = "shor-state"
REPH_STATE = "reph-state"
BYANJON_STATE = "byanjon-state"

GROUP_MAPS: Dict[str, Dict[str, str]] = {
    "shor": SHOR,
    "fkar": FKAR,
    "byanjon": BYANJON,
    "juktoborno": JUKTOBORNO,
    "ng": NG,
    "reph": REPH,
    "phola": PHOLA,
    "kar": KAR,
    "ongko": ONGKO,
    "diacritic": DIACRITIC,
    "biram": BIRAM,
    "prithayok": PRITHAYOK,
    "ae": AE,
}

# Group order per state (priority used when same-length matches)
STATE_GROUP_ORDER: Dict[str, List[str]] = {
    INIT: ["diacritic", "ng", "shor", "fkar", "prithayok", "ongko", "biram", "reph", "juktoborno", "byanjon"],
    SHOR_STATE: ["diacritic", "ng", "shor", "fkar", "biram", "prithayok", "ongko", "biram", "reph", "juktoborno", "byanjon"],
    REPH_STATE: ["prithayok", "diacritic", "ng", "ae", "juktoborno", "byanjon", "kar"],
    BYANJON_STATE: ["diacritic", "ng", "prithayok", "ongko", "biram", "kar", "juktoborno", "phola", "byanjon"],
}

# Precompute max key length per group for greedy matching
MAXLEN_PER_GROUP: Dict[str, int] = {
    g: (max((len(k) for k in m.keys()), default=0)) for g, m in GROUP_MAPS.items()}


def _find_longest(state: str, text: str, i: int) -> Tuple[str, str, str]:
    """Return (group, key, value) for the longest match allowed in current state. If none, return ("", "", "")."""
    allowed = STATE_GROUP_ORDER[state]
    # Determine the max lookahead we need
    maxlen = 0
    for g in allowed:
        maxlen = max(maxlen, MAXLEN_PER_GROUP[g])
    end = min(len(text), i + maxlen)
    best_group = ""
    best_key = ""
    best_val = ""
    best_len = 0

    # Try lengths from longest to shortest to implement greedy matching
    for L in range(end - i, 0, -1):
        chunk = text[i:i + L]
        # Check groups by priority
        for g in allowed:
            m = GROUP_MAPS[g]
            if chunk in m:
                # First match at this length wins due to priority order
                return (g, chunk, m[chunk])
    return ("", "", "")


def _apply_transition(state: str, group: str) -> str:
    # ---------------------------
    # INIT state
    # ---------------------------
    if state == INIT:
        if group in ("diacritic", "ng", "shor", "fkar"):
            return SHOR_STATE
        if group in ("prithayok", "ongko", "biram"):
            return SHOR_STATE
        if group == "reph":
            return REPH_STATE
        if group in ("juktoborno", "byanjon"):
            return BYANJON_STATE
        return INIT

    # ---------------------------
    # SHOR state
    # ---------------------------
    if state == SHOR_STATE:
        if group in ("diacritic", "ng", "fkar"):
            return SHOR_STATE
        if group == "shor":
            return SHOR_STATE
        if group in ("biram", "prithayok", "ongko"):
            return SHOR_STATE
        if group == "reph":
            return REPH_STATE
        if group in ("juktoborno", "byanjon"):
            return BYANJON_STATE
        return SHOR_STATE

    # ---------------------------
    # REPH state
    # ---------------------------
    if state == REPH_STATE:
        if group == "prithayok":
            return SHOR_STATE
        if group in ("diacritic", "ng"):
            return SHOR_STATE
        if group == "ae":
            return SHOR_STATE
        if group in ("juktoborno", "byanjon"):
            return BYANJON_STATE
        if group in ("kar", "nil"):
            return SHOR_STATE
        return REPH_STATE

    # ---------------------------
    # BYANJON state
    # ---------------------------
    if state == BYANJON_STATE:
        if group in ("diacritic", "ng", "prithayok", "ongko", "biram", "kar"):
            return SHOR_STATE
        if group in ("juktoborno", "phola", "byanjon"):
            return BYANJON_STATE
        return BYANJON_STATE

    return INIT


def convert(text: str) -> str:
    """Convert an ASCII input string to Bengali output using the bn-khipro state machine."""
    i = 0
    n = len(text)
    state = INIT
    out: List[str] = []

    while i < n:
        group, key, val = _find_longest(state, text, i)
        if not group:
            # No mapping: pass through this char and reset to INIT
            out.append(text[i])
            i += 1
            state = INIT
            continue

        # Special handling: PHOLA in BYANJON_STATE inserts virama before mapped char
        if state == BYANJON_STATE and group == "phola":
            out.append("্")
            out.append(val)
        else:
            out.append(val)

        i += len(key)
        state = _apply_transition(state, group)

    return "".join(out)


def type_stream(text: str) -> Generator[str, None, None]:
    """Generator: yields the converted text after each keystroke (1..len(text))."""
    for k in range(1, len(text) + 1):
        yield convert(text[:k])


# --------------------------
# Demo
# --------------------------
if __name__ == "__main__":
    import sys
    from datetime import datetime

    output_file = "khipro_typing_log.txt"

    print(f"🔡 Khipro Typing Preview (Press Enter to quit)")
    print(f"Output will be saved to: {output_file}\n")

    while True:
        user_input = input("Type in khipro syntax: ").strip()
        if not user_input:
            break

        with open(output_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{'='*60}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Input: {user_input}\n\n")
            f.write("Live Typing Progression:\n")

            for step, out in enumerate(type_stream(user_input), 1):
                f.write(f"{user_input[:step]} → {out}\n")

            f.write(f"{'='*60}\n")

        print(f"✓ Saved to {output_file}")
        print("-" * 40)
