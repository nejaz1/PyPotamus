import hid
from struct import unpack
import pdb

# open hand device

h = hid.device()
h.open(0x16c0, 0x486)
h.set_nonblocking(1)

h.write([0]*64)

while True:
    d = bytearray(h.read(46))
    if d:
        x = unpack('>LhHHHHHHHHHHHHHHHHHHHH', d)
        print(x)

h.close()
