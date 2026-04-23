from mappings import shor, kar, byanjon
import sys

output_stream = ""
input_stream = sys.argv[1]


def longest_key_length(*dicts):
    max_len = 0

    for d in dicts:
        for key in d.keys():
            if len(key) > max_len:
                max_len = len(key)

    return max_len


def check_string_against_dicts(input_str, *dicts):
    # Step 1: get longest key length
    max_key_len = longest_key_length(*dicts)

    # Rule 1: input string too long
    if len(input_str) > max_key_len:
        return -1

    matched_dict_indices = []

    # Step 2: check exact matches
    for i, d in enumerate(dicts):
        if input_str in d:   # exact key match
            matched_dict_indices.append(i)

    # Rule 2: no match found
    if not matched_dict_indices:
        return 0

    # Rule 3: return where it matched
    return matched_dict_indices


def init_state(string):
    list_of_dictionaries = [shor, kar, byanjon]
    pointer = longest_key_length(*list_of_dictionaries)

    processable_slice = string[:pointer]
    refundnable_slice = string[pointer:]

    decision = check_string_against_dicts(
        processable_slice, *list_of_dictionaries)

    if decision == -1:
        print("Impossibly -1 was returned.")

    while pointer > 0:
        decision = check_string_against_dicts(
            processable_slice, *list_of_dictionaries)
        if decision == 0:
            pointer -= 1  # যদি ম্যাচ না পাওয়া যায় তাহলে পয়েন্টার একঘর বামে সরাবে। তাহলে প্রসেসেবল স্ত্রিং ছোটো হবে।
        elif decision not in {0, -1}:
            break  # অর্থাৎ, ম্যাচ পাওয়া গেছে।

    if decision == 0:  # যদি এখনও no-match অবস্থা থাকে তাহলে...
        refundnable_slice = string[pointer:]
        output = processable_slice
        return (output, refundnable_slice)

    # if decision == -1:
    #     decision = string[:longest_key_length(list_of_dictionaries)]

    # if decision == 0:
    #     while True:
    #         i = 1
    #         decision = check_string_against_dicts(string[:-i])
    #         i += 1
    #         if string[:-i] == '':
    #             break
