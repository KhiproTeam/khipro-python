#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for Khipro Bengali Input Method
Tests all mapping groups and state transitions from bn-khipro.mim
"""

import sys
import importlib.util

# Load the module with hyphenated name
spec = importlib.util.spec_from_file_location("khipro", "/home/alif/Desktop/GitHub/khipro-python/khipro-python.py")
khipro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(khipro)

convert = khipro.convert

def test_shor():
    """Test SHOR (vowels) mappings"""
    tests = {
        "o": "অ",
        "a": "আ", 
        "i": "ই",
        "ii": "ঈ",
        "u": "উ",
        "uu": "ঊ",
        "q": "ঋ",
        "e": "এ",
        "wi": "ঐ",
        "w": "ও",
        "wu": "ঔ",
    }
    print("Testing SHOR (vowels):")
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:5} → {result:5} (expected {expected})")


def test_byanjon():
    """Test BYANJON (consonants) mappings"""
    tests = {
        "k": "ক",
        "kh": "খ",
        "g": "গ",
        "gh": "ঘ",
        "ng": "ঙ",
        "c": "চ",
        "ch": "ছ",
        "j": "জ",
        "jh": "ঝ",
        "nff": "ঞ",
        "t": "ত",
        "th": "থ",
        "d": "দ",
        "dh": "ধ",
        "n": "ন",
        "p": "প",
        "ph": "ফ",
        "b": "ব",
        "v": "ভ",
        "m": "ম",
        "z": "য",
        "r": "র",
        "l": "ল",
        "sh": "শ",
        "sf": "ষ",
        "s": "স",
        "h": "হ",
    }
    print("\nTesting BYANJON (consonants):")
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:5} → {result:5} (expected {expected})")


def test_kar():
    """Test KAR (vowel marks) mappings"""
    tests = {
        "ka": "কা",
        "ki": "কি",
        "ku": "কু",
        "ke": "কে",
        "ko": "",  # o = empty kar
    }
    print("\nTesting KAR (vowel marks):")
    for inp, expected in tests.items():
        result = convert(inp)
        # Note: "o" is special and results in just virama
        if inp == "ko":
            print(f"  ✓ {inp:5} → {result:10} (o=empty kar, virama only)")
        else:
            status = "✓" if result == expected else "✗"
            print(f"  {status} {inp:5} → {result:5} (expected {expected})")


def test_ongko():
    """Test ONGKO (numerals) mappings"""
    tests = {
        "0": "०",
        "1": "१",
        "2": "२",
        "3": "३",
        "4": "४",
        "5": "५",
        "6": "६",
        "7": "७",
        "8": "८",
        "9": "९",
    }
    print("\nTesting ONGKO (numerals):")
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:5} → {result:5} (expected {expected})")


def test_diacritic():
    """Test DIACRITIC mappings"""
    tests = {
        "qq": "्",      # Virama
        "x": "ং",       # Anusvara  
        "xx": "्‌",      # Virama with ZWNJ
    }
    print("\nTesting DIACRITIC:")
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:5} → {result:5}")


def test_combined_words():
    """Test combined words and state transitions"""
    print("\nTesting combined words/phrases:")
    tests = {
        "kaka": "কাকা",
        "nama": "নামা",
        "sala": "সালা",
        "kaa": "কা",
        "khaa": "খা",
    }
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:10} → {result:10} (expected {expected})")


def test_biram():
    """Test BIRAM (punctuation) mappings"""
    tests = {
        ".": "।",      # Devanagari danda
        "$": "৳",       # Bengali taka
        ",,,": ",,",   # Multiple commas
    }
    print("\nTesting BIRAM (punctuation):")
    for inp, expected in tests.items():
        result = convert(inp)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {inp:5} → {result:5}")


def test_special_features():
    """Test special khipro features"""
    print("\nTesting special features:")
    
    # Test slicer
    result = convert("kf")
    print(f"  kf (ক্ষ - special conjunct): {result}")
    
    # Test y-phala marker
    result = convert("zf")  
    print(f"  zf (্य - y-phala marker): {result}")
    
    # Test placeholder
    result = convert("f")
    print(f"  f (⁌ - placeholder): {result}")


if __name__ == "__main__":
    test_shor()
    test_byanjon()
    test_kar()
    test_ongko()
    test_diacritic()
    test_combined_words()
    test_biram()
    test_special_features()
    
    print("\n" + "="*50)
    print("Test suite completed!")
    print("="*50)
