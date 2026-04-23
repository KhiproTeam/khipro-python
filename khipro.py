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

def processable_slice (string:str, pointer:int):
    return string[:pointer]

def refundable_slice (string:str, pointer:int):
    return string[pointer:]

def tokenizer(string:str, pointer:int):
        decision = check_string_against_dicts(processable_slice(string,pointer), *list_of_dictionaries)

        if decision == -1:
            print("Impossibly -1 was returned.")

        while pointer > 0:
            decision = check_string_against_dicts(processable_slice(string, pointer), *list_of_dictionaries)
            if decision == 0:
                pointer -= 1  # যদি ম্যাচ না পাওয়া যায় তাহলে পয়েন্টার একঘর বামে সরাবে। তাহলে প্রসেসেবল স্ট্রিং ছোটো হবে।
            elif decision not in {0, -1}:
                break  # অর্থাৎ, ম্যাচ পাওয়া গেছে।
            elif pointer == 1:
                break # অর্থাৎ ম্যাচ পাওয়া যায় নি। কিন্তু স্লাইস এক ক্য‍ারেক্টারের হয়ে গেছে।

        return decision

def init_state(string):
    list_of_dictionaries = [shor, byanjon]
    pointer = longest_key_length(*list_of_dictionaries)

    decision = tokenizer(string, pointer)

    if decision == 0:  # যদি এখনও no-match অবস্থা থাকে তাহলে...
        
        output = processable_slice(string, pointer) # অর্থাৎ প্রথম ক্য‍ারেক্টার, যেটা ম্যাচ হয়নি, সেটাকেই ইংরেজি অবস্থাতেই পাঠিয়ে দেওয়া হচ্ছে।
        return (output, refundable_slice(string, pointer))

    elif decision not in {0, -1}: # যদি এক বা একাধিক ম্যাচ পাওয়া যায়...
        if 0 in decision: # shor
            output_stream.append(shor[processable_slice])
            shor_state(refundable_slice)
        elif 1 in decision: # byanjon
            output_stream.append(byanjon[processable_slice])
            byanjon_state(refundable_slice)

