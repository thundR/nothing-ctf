# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.4 (default, Jul  9 2019, 16:32:37) 
# [GCC 9.1.1 20190503 (Red Hat 9.1.1-1)]
# Embedded file name: ./encoder.py
# Compiled at: 2019-10-09 22:14:05
import base64, string, sys
from random import shuffle

def encode(file, base64):
    s = string.printable # len(s) = 100
    init = lambda : (list(s), [])
    bag, buf = init()
    for x in base64:
        if x not in s:
            continue
        while True:
            r = bag[0] # get first printable from list
            bag.remove(r) # remove first character from bag
            diff = (ord(x) - ord(r) + 100) % 100 # create 'hash' from bag, index within [0-100)
            if diff == 0 or len(bag) == 0: #if same character or bag is empty:
                shuffle(buf)
                file.write(('').join(buf)) #write out shuffled buffer :))))))))))))
                file.write('\x00') # null char
                bag, buf = init() # re-init bag, kill buffer
                shuffle(bag) # shuffle bag
            else:
                break
            #end while
        buf.extend(r * (diff - 1)) # add current character diff -1 times to the buffer
        file.write(r) # write current character popped from the from of bag

        # buf = [a, a, a, a, a, b, b, b, c, c] 5 a's diff = 6 r='a'
        #end for
    shuffle(buf)
    file.write(('').join(buf))

    #buf = [a, c, b, a, a, b, c, ]


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as (r):
        w = open(sys.argv[1] + '.enc', 'wb')
        b64 = base64.b64encode(r.read())
        encode(w, b64)
# okay decompiling encoder.pyc




             
