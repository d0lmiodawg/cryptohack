from os import urandom

"""
Implementation lacks addition step after the 8 quarter rounds,
making the _inner_block invertible, which in turn lets us recover
the initial state matrix containing the key.
"""

def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def r_rotate(x, n):
    return ((x >> n) & 0xffffffff) | ((x << (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])

class RChaCha20:
    def __init__(self):
        self._state = []

    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    def r_inner_block(self, state):
        self.r_quarter_round(state, 3, 4, 9, 14)
        self.r_quarter_round(state, 2, 7, 8, 13)
        self.r_quarter_round(state, 1, 6, 11, 12)
        self.r_quarter_round(state, 0, 5, 10, 15)
        self.r_quarter_round(state, 3, 7, 11, 15)
        self.r_quarter_round(state, 2, 6, 10, 14)
        self.r_quarter_round(state, 1, 5, 9, 13)
        self.r_quarter_round(state, 0, 4, 8, 12)

    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    
    def r_quarter_round(self, x, a, b, c, d):
        x[b] = r_rotate(x[b], 7); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
        x[d] = r_rotate(x[d], 8); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
        x[b] = r_rotate(x[b], 12); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
        x[d] = r_rotate(x[d], 16); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
    
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))

    def r_encrypt(self, m, enc):
        c = b''
        self._counter = 1

        # for i in range(0, len(enc), 64):
        for i in range(0, 64, 64):
            self._state = bytes_to_words(xor(enc[i:i+64], m[i:i+64])) # xor with state
            print(len(self._state))
            # self._setup_state(key, iv) # Make key matrix (state)
            for j in range(10):
                self.r_inner_block(self._state) # 8 quarter rounds, modifies state
            key = words_to_bytes(self._state[4:12])

            self._counter += 1
        
        return key
    
class ChaCha20:
    def __init__(self):
        self._state = []

    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    def _quarter_round(self, x, a, b, c, d):
        """
        
        """
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))

    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)

    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1

        for i in range(0, len(m), 64):
            self._setup_state(key, iv) # Make key matrix (state)
            for j in range(10):
                self._inner_block(self._state) # 8 quarter rounds, modifies state
            c += xor(m[i:i+64], words_to_bytes(self._state)) # xor with state

            self._counter += 1
        
        return c

with open("output_chacha.txt", "r") as f:
    lines = f.readlines()

msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
iv1 = bytes.fromhex(lines[0].split("=")[-1].strip()[1:-1])
iv2 = bytes.fromhex(lines[1].split("=")[-1].strip()[1:-1])
msg_enc = bytes.fromhex(lines[2].split("=")[-1].strip()[1:-1])
flag_enc = bytes.fromhex(lines[3].split("=")[-1].strip()[1:-1])

r = RChaCha20()
k = r.r_encrypt(msg, msg_enc)
c = ChaCha20()
print(c.decrypt(flag_enc, k, iv2))

