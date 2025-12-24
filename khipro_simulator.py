#!/usr/bin/env python3
"""
bn-khipro Input Method Simulator
A Python implementation of the Khipro Bengali keyboard layout logic.

This module replicates the state machine behavior of the m17n input method
to process key sequences and generate Bengali text output.
"""

from datetime import datetime
from typing import List, Tuple, Optional
import importlib.util
import sys
import os


class KhiproInputMethod:
    def __init__(self, mappings_module=None):
        """
        Initialize the input method.

        Args:
            mappings_module: A module object containing mapping dictionaries,
                           or None to use default mappings
        """
        if mappings_module:
            self.load_mappings_from_module(mappings_module)
        else:
            self.load_default_mappings()

        # State definitions
        self.current_state = "init"
        self.buffer = ""
        self.output = ""

    def load_default_mappings(self):
        """Load default (minimal) mappings"""
        self.shor = {"o": "অ"}
        self.fkar = {"uff": "‌ু"}
        self.byanjon = {"k": "ক"}
        self.juktoborno = {"rz": "র্য"}
        self.ng = {}
        self.reph = {"rr": "র্", "r": "র", "rr/": "রর"}
        self.phola = {"r": "র", "z": "য"}
        self.kar = {"o": "", "of": "অ"}
        self.ongko = {".1": ".১"}
        self.diacritic = {"qq": "্", "xx": "্‌"}
        self.biram = {
            ".": "।", "...": "...", "..": ".", "$": "৳", "$f": "₹",
            ",,,": ",,", ".f": "॥", ".ff": "॰", "+": "+", "-": "-",
            "+f": "×", "-f": "÷", "$$": "$", "=": "=", "=f": "≠"
        }
        self.prithayok = {";": "", ";;": ";"}
        self.ae = {"ae": "‍্যা"}

    def load_mappings_from_module(self, module):
        """
        Load mappings from an external module.

        The module should define dictionaries named:
        shor, fkar, byanjon, juktoborno, ng, reph, phola, kar,
        ongko, diacritic, biram, prithayok, ae
        """
        self.shor = getattr(module, 'shor', {})
        self.fkar = getattr(module, 'fkar', {})
        self.byanjon = getattr(module, 'byanjon', {})
        self.juktoborno = getattr(module, 'juktoborno', {})
        self.ng = getattr(module, 'ng', {})
        self.reph = getattr(module, 'reph', {})
        self.phola = getattr(module, 'phola', {})
        self.kar = getattr(module, 'kar', {})
        self.ongko = getattr(module, 'ongko', {})
        self.diacritic = getattr(module, 'diacritic', {})
        self.biram = getattr(module, 'biram', {})
        self.prithayok = getattr(module, 'prithayok', {})
        self.ae = getattr(module, 'ae', {})

    def reset(self):
        """Reset the input method state"""
        self.current_state = "init"
        self.buffer = ""
        self.output = ""

    def match_in_map(self, text: str, map_dict: dict) -> Optional[Tuple[str, str]]:
        """
        Try to match text against a mapping dictionary.
        Returns (matched_key, output) if found, None otherwise.
        Tries longest matches first.
        """
        # Sort keys by length (descending) to match longest first
        sorted_keys = sorted(map_dict.keys(), key=len, reverse=True)

        for key in sorted_keys:
            if text.endswith(key):
                return (key, map_dict[key])
        return None

    def process_in_state(self, current_input: str, state: str) -> Tuple[str, str]:
        """
        Process input according to current state.
        Returns (output, new_state)
        """
        output = ""
        new_state = state
        matched = False

        if state == "init":
            # Try matching in order of priority
            if (match := self.match_in_map(current_input, self.diacritic)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ng)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.shor)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.fkar)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.prithayok)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ongko)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.biram)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.reph)):
                output = match[1]
                new_state = "reph-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.juktoborno)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.byanjon)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True

        elif state == "shor-state":
            if (match := self.match_in_map(current_input, self.diacritic)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ng)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.shor)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.fkar)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.biram)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.prithayok)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ongko)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.reph)):
                output = match[1]
                new_state = "reph-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.juktoborno)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.byanjon)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True

        elif state == "reph-state":
            if (match := self.match_in_map(current_input, self.prithayok)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.diacritic)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ng)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ae)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.juktoborno)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.byanjon)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.reph)):
                output = match[1]
                new_state = "reph-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.kar)):
                output = match[1]
                new_state = "shor-state"
                matched = True

        elif state == "byanjon-state":
            if (match := self.match_in_map(current_input, self.diacritic)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ng)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.prithayok)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.ongko)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.biram)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.kar)):
                output = match[1]
                new_state = "shor-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.juktoborno)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.phola)):
                # Special handling for phola: insert hasant before
                output = "্" + match[1]
                new_state = "byanjon-state"
                matched = True
            elif (match := self.match_in_map(current_input, self.byanjon)):
                output = match[1]
                new_state = "byanjon-state"
                matched = True

        return (output, new_state)

    def process_sequence(self, key_sequence: str) -> List[Tuple[str, str]]:
        """
        Process a complete key sequence and return all intermediate outputs.
        Returns a list of (input_prefix, output) tuples.
        """
        results = []
        self.reset()

        accumulated_input = ""
        accumulated_output = ""

        for char in key_sequence:
            accumulated_input += char

            # Try to process with current state
            output, new_state = self.process_in_state(
                accumulated_input, self.current_state)

            if output or new_state != self.current_state:
                accumulated_output += output
                self.current_state = new_state
            else:
                # If no match, just append the character as-is
                accumulated_output += char

            results.append((accumulated_input, accumulated_output))

        return results


def load_mappings_file(filepath: str):
    """
    Load a Python file containing mapping dictionaries.

    Args:
        filepath: Path to the mappings file

    Returns:
        Module object with the mappings loaded
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Mappings file not found: {filepath}")

    spec = importlib.util.spec_from_file_location("khipro_mappings", filepath)

    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load module spec from {filepath}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["khipro_mappings"] = module
    spec.loader.exec_module(module)

    return module


def main():
    """Main function to run the input method simulator"""
    print("=" * 60)
    print("Bengali Khipro Input Method Simulator")
    print("=" * 60)
    print()

    # Check for mappings file
    mappings_module = None
    mappings_file = "khipro_mappings.py"

    if os.path.exists(mappings_file):
        print(f"✓ Found mappings file: {mappings_file}")
        try:
            mappings_module = load_mappings_file(mappings_file)
            print("✓ Mappings loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading mappings file: {e}")
            print("  Using default mappings instead")
    else:
        print(f"ℹ Mappings file '{mappings_file}' not found")
        print("  Using default (minimal) mappings")
        print(f"  Create '{mappings_file}' to use custom mappings")

    print()

    # Create input method instance
    im = KhiproInputMethod(mappings_module)

    # Get user input
    key_sequence = input("Enter your key sequence: ").strip()

    if not key_sequence:
        print("No input provided. Exiting.")
        return

    # Process the sequence
    results = im.process_sequence(key_sequence)

    # Generate output content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("Bengali Khipro Input Method - Output")
    output_lines.append(f"Generated: {timestamp}")
    output_lines.append("=" * 60)
    output_lines.append("")
    output_lines.append(f"Input Sequence: {key_sequence}")
    output_lines.append("")
    output_lines.append("Progressive Output:")
    output_lines.append("-" * 60)

    for input_prefix, output in results:
        output_lines.append(f"{input_prefix} = \"{output}\"")

    output_lines.append("")
    output_lines.append("=" * 60)

    # Write to file
    output_filename = f"khipro_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print()
    print(f"✓ Output successfully generated and saved to: {output_filename}")
    print()
    print("Preview of output:")
    print("-" * 60)
    for line in output_lines[-10:]:  # Show last 10 lines as preview
        print(line)


if __name__ == "__main__":
    main()
