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
            if len(bag) == 0: #if same character or bag is empty:
                shuffle(buf)
                file.write(('').join(buf)) #write out shuffled buffer :))))))))))))
                file.write('\x00') # null char
                bag, buf = init() # re-init bag, kill buffer
                shuffle(bag) # shuffle bag
            else:
                break
            #end while
        buf.extend(r * (diff - 1)) # add current character diff -1 times to the buffer
        file.write(r) # write current character popped from teh front of bag
        #end for
    shuffle(buf)
    file.write(('').join(buf))


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as (r):
        w = open(sys.argv[1] + '.enc', 'wb')
        b64 = base64.b64encode(r.read())
        encode(w, b64)
# okay decompiling encoder.pyc
