#!/usr/bin/python
# This is an implementation of sha512.
import sys


def mask(n):
    """Return a bitmask of length n (suitable for masking against an
      int to coerce the size to a given length)
   """
    if n >= 0:
        return 2 ** n - 1
    else:
        return 0


def rol(n, rotations=1, width=64):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width)  # # Should it be an error to truncate here?
    return ((n << rotations) & mask(width)) | (n >> (width - rotations))


def ror(n, rotations=1, width=64):
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
    return hex(domask(s))[2:].strip('L').zfill(16)


def domask(s):
    return s & 0xffffffffffffffff


def do_hash(m):
    # Initializing hash sectors from the fractional parts of the square roots of the first 8 primes
    h0 = 0x6a09e667f3bcc908
    h1 = 0xbb67ae8584caa73b
    h2 = 0x3c6ef372fe94f82b
    h3 = 0xa54ff53a5f1d36f1
    h4 = 0x510e527fade682d1
    h5 = 0x9b05688c2b3e6c1f
    h6 = 0x1f83d9abfb41bd6b
    h7 = 0x5be0cd19137e2179

    # Initialize array of round constants
    k = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538,
              0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe,
              0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
              0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
              0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab,
              0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
              0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed,
              0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
              0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
              0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
              0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373,
              0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
              0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c,
              0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
              0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
              0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

    m = [bin(ord(x))[2:].zfill(8) for x in m]  # Convert to binary string
    initial_len = len(''.join(m))
    m.append('10000000')  # Add initial 10 padding
    mlen = len(''.join(m))
    modlen = mlen % 1024
    while modlen != 896:
        m.append('0' * 8)
        modlen = len(''.join(m)) % 1024

    # Append length as 128-bit integer
    binary_length = bin(initial_len)[2:].strip('L').zfill(128)
    block_length = [binary_length[i:i + 8] for i in range(0, len(binary_length), 8)]
    m.extend(block_length)

    # Convert m to 64 bit words
    n = []
    for i in range(0, len(m), 8):
        n.append(''.join(m[i:i + 8]))
    m = n


    # At this point everything is words, so convert back to integers for easier manipulation
    m = [int(x, 2) for x in m]

    chunks = []
    for chunk in range(0, len(m), 16):
        chunks.append(m[chunk:chunk + 16])

    for chunk in chunks:
        w = [0] * 80
        for i in range(16):
            w[i] = chunk[i]

        for i in range(16, 80):
            s0 = ror(w[i - 15], 1) ^ ror(w[i - 15], 8) ^ (w[i - 15] >> 7)
            s1 = ror(w[i - 2], 19) ^ ror(w[i - 2], 61) ^ (w[i - 2] >> 6)
            w[i] = domask(w[i - 16] + s0 + w[i - 7] + s1)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(80):
            # print('t=%s' % (i - 1), hex(a), hex(b), hex(c), hex(d), hex(e), hex(f), hex(g), hex(h))
            S1 = ror(e, 14) ^ ror(e, 18) ^ ror(e, 41)
            ch = (e & f) ^ ((~e) & g)
            temp1 = h + S1 + ch + k[i] + w[i]
            S0 = ror(a, 28) ^ ror(a, 34) ^ ror(a, 39)
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

    result = clean(h0) + clean(h1) + clean(h2) + clean(h3) + clean(h4) + clean(h5) + clean(h6) + clean(h7)

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
