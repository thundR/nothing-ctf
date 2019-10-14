import base64, string, sys
import re
from __future__ import print_function

valid_b64_char = re.compile(r"[A-Za-z0-9+/=]")


def decode(encoded_file):
    b64_string = ''
    raw_data = encoded_file.read()
    data_len = len(raw_data)
    done = False
    segment_start = 0
    segment_end = 0
    data_end = 0
    # 
    while not done:
        seen_chars = dict()
        i = segment_start
        current_char = raw_data[i]
        is_in_buffer = False
        data_string = ''
        decoded_string = ''
        while (current_char != '\0') or (i == data_len):
            if current_char in seen_chars:
                seen_chars[current_char] += 1
                if not is_in_buffer:
                    data_end = i
                    is_in_buffer = True
            else:
                if is_in_buffer:
                    print("bork: char " + str(current_char) + " in buffer but not in data")
                    for key in seen_chars:
                        print(str(key) + ": " + str(seen_chars[key])) 
                data_string += str(current_char)
                seen_chars[current_char] = 1
            i += 1
            current_char = raw_data[i]
        for r in seen_chars:
            diff = seen_chars[r] # r is key in dict and our random printable
            # x = (ord(x) - ord(r) + 100) % 100
            candidate_char = None
            for i in range(-1, 2):
                candidate_val = ord(r) + diff + i*100
                
                if 0 <= candidate_val <= 127:
                    candidate_char = chr(candidate_val)
            if candidate_char is None:
                print("BORK: no char found for r value " + str(r) + " and diff " + str(diff) + " at location " + str(i))
                exit(69)


        segment_start = i + 1
        b64_string += decoded_string
    # 


    return b64_string 

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as (encoded_file):
        file_to_write = open(sys.argv[1].split('.')[:-1].join(''), 'wb')
        b64 = decode(encoded_file)
        byte_array = base64.b64decode(b64, True) # raise error if non-base64 characters are present
        file_to_write.write(byte_array)
        