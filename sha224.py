#!/usr/bin/python
# This is an implementation of sha224.
import sys


def mask(n):
    """Return a bitmask of length n (suitable for masking against an
      int to coerce the size to a given length)
   """
    if n >= 0:
        return 2 ** n - 1
    else:
        return 0


def rol(n, rotations=1, width=32):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width)  # # Should it be an error to truncate here?
    return ((n << rotations) & mask(width)) | (n >> (width - rotations))


def ror(n, rotations=1, width=32):
    """Return a given number of bitwise right rotations of an integer n,
       for a given bit field width.
    """
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width)
    return (n >> rotations) | ((n << (width - rotations)) & mask(width))


def clean(s):
    # Clean a 4 byte integer, converting it to hex for display
    return hex(domask(s))[2:].strip('L').zfill(8)

def domask(s):
    return s & 0xffffffff


def do_hash(m):
    # Initializing hash sectors from the fractional parts of the square roots of the 9th through 16th primes
    h0 = 0xc1059ed8
    h1 = 0x367cd507
    h2 = 0x3070dd17
    h3 = 0xf70e5939
    h4 = 0xffc00b31
    h5 = 0x68581511
    h6 = 0x64f98fa7
    h7 = 0xbefa4fa4

    # Initialize array of round constants
    k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    m = [bin(ord(x))[2:].zfill(8) for x in m]  # Convert to binary string
    initial_len = len(''.join(m))
    m.append('10000000')  # Add initial 10 padding
    mlen = len(''.join(m))
    modlen = mlen % 512
    while modlen != 448:
        m.append('0' * 8)
        modlen = len(''.join(m)) % 512

    # Append length as 64-bit integer
    binary_length = bin(initial_len)[2:].strip('L').zfill(64)
    block_length = [binary_length[i:i + 8] for i in range(0, len(binary_length), 8)]
    m.extend(block_length)

    # Convert m to 32 bit words
    n = []
    for i in range(0, len(m), 4):
        n.append(''.join(m[i:i + 4]))
    m = n


    # At this point everything is words, so convert back to integers for easier manipulation
    m = [int(x, 2) for x in m]

    chunks = []
    for chunk in range(0, len(m), 16):
        chunks.append(m[chunk:chunk + 16])

    for chunk in chunks:
        w = [0] * 64
        for i in range(16):
            w[i] = chunk[i]

        for i in range(16, 64):
            s0 = ror(w[i - 15], 7) ^ ror(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = ror(w[i - 2], 17) ^ ror(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = domask(w[i - 16] + s0 + w[i - 7] + s1)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            # print('t=%s' % (i - 1), hex(a), hex(b), hex(c), hex(d), hex(e), hex(f), hex(g), hex(h))
            S1 = ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = h + S1 + ch + k[i] + w[i]
            S0 = ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = S0 + maj

            h = g
            g = f
            f = e
            e = domask(d + temp1)
            d = c
            c = b
            b = a
            a = domask(temp1 + temp2)

        h0, h1, h2, h3, h4, h5, h6, h7 = domask(h0 + a), domask(h1 + b), domask(h2 + c), domask(h3 + d), domask(h4 + e), domask(h5 + f), domask(h6 + g), domask(h7 + h)

    result = clean(h0) + clean(h1) + clean(h2) + clean(h3) + clean(h4) + clean(h5) + clean(h6)

    return result


def main():
    if len(sys.argv) < 2:
        inp = sys.stdin.read()
        print('%s  -' % do_hash(inp))
    else:
        f = open(sys.argv[1], 'r')
        print('%s  %s' % (do_hash(f.read()), sys.argv[1]))
        f.close()


if __name__ == '__main__':  main()
