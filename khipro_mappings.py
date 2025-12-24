#!/usr/bin/env python3
"""
Khipro Bengali Keyboard Layout - Mappings File

This file contains all the character mappings for the Khipro input method.
Store your huge dictionaries here, separate from the main logic.

Instructions:
1. Fill in each dictionary with your complete mappings
2. Keep this file in the same directory as the main script
3. The main script will automatically load these mappings

Dictionary naming must match exactly:
- shor, fkar, byanjon, juktoborno, ng, reph, phola, kar,
  ongko, diacritic, biram, prithayok, ae
"""

# Vowels (স্বরবর্ণ)
shor = {
    "o": "অ",
    # Add more vowel mappings here
    # "a": "আ",
    # "i": "ই",
    # etc...
}

# Vowel diacritics/modifiers (ফলা)
fkar = {
    "uff": "‌ু",
    # Add more fkar mappings here
}

# Consonants (ব্যঞ্জনবর্ণ)
byanjon = {
    "k": "ক",
    # Add more consonant mappings here
    # "kh": "খ",
    # "g": "গ",
    # "gh": "ঘ",
    # etc...
}

# Conjunct consonants (যুক্তবর্ণ)
juktoborno = {
    "rz": "র্য",
    # Add more conjunct mappings here
    # "kk": "ক্ক",
    # "kt": "ক্ত",
    # etc...
}

# Anusvara/Chandrabindu/etc
ng = {
    # Add ng-related mappings here
}

# Reph (র-ফলা)
reph = {
    "rr": "র্",
    "r": "র",
    "rr/": "রর",
    # Add more reph mappings here
}

# Phola (য-ফলা, র-ফলা when attached to consonants)
phola = {
    "r": "র",
    "z": "য",
    # Add more phola mappings here
}

# Vowel signs/kar (কার)
kar = {
    "o": "",
    "of": "অ",
    # Add more kar mappings here
    # "a": "া",
    # "i": "ি",
    # etc...
}

# Numbers (সংখ্যা)
ongko = {
    ".1": ".১",
    # Add more number mappings here
    # ".2": ".২",
    # ".3": ".৩",
    # etc...
}

# Diacritical marks (হসন্ত, চন্দ্রবিন্দু, etc.)
diacritic = {
    "qq": "্",
    "xx": "্‌",
    # Add more diacritic mappings here
}

# Punctuation marks (বিরাম চিহ্ন)
biram = {
    ".": "।",
    "...": "...",
    "..": ".",
    "$": "৳",
    "$f": "₹",
    ",,,": ",,",
    ".f": "॥",
    ".ff": "॰",
    "+": "+",
    "-": "-",
    "+f": "×",
    "-f": "÷",
    "$$": "$",
    "=": "=",
    "=f": "≠",
    # Add more punctuation mappings here
}

# Separator/null mapping
prithayok = {
    ";": "",
    ";;": ";",
    # Add more separator mappings here
}

# Special cases (like AE combination)
ae = {
    "ae": "‍্যা",
    # Add more special case mappings here
}


# Optional: You can add comments to document your mappings
"""
Mapping Documentation:

State transitions:
- init → shor-state: when typing vowels, punctuation, numbers
- init → reph-state: when typing 'r' combinations
- init → byanjon-state: when typing consonants
- byanjon-state → shor-state: when adding vowel signs (kar)
- any-state → any-state: based on the mapping matched

Special behaviors:
- phola: automatically inserts hasant (্) before the character
- reph: can be chained with other characters
- kar: modifies the previous consonant
"""
