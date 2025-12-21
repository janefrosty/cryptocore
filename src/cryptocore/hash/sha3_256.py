import struct

class SHA3_256:
    """
    Sprint 4: SHA3-256 implementation from scratch
    Follows NIST FIPS 202 specification
    Keccak sponge construction with 1088-bit rate
    """
    
    def __init__(self):
        self.rate = 1088
        self.capacity = 512
        self.output_length = 256
        
        self.state = [[0] * 5 for _ in range(5)]
        self.buffer = bytearray()
        self.total_length = 0

    @staticmethod
    def _rot64(a, n):
        return ((a >> (64 - n)) | (a << n)) & ((1 << 64) - 1)

    def _keccak_f(self):
        RC = [
            0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
            0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
            0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
            0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
            0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
            0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
            0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
            0x8000000000008080, 0x0000000080000001, 0x8000000080008008
        ]
        
        C = [0] * 5
        D = [0] * 5
        
        for x in range(5):
            C[x] = self.state[x][0] ^ self.state[x][1] ^ self.state[x][2] ^ self.state[x][3] ^ self.state[x][4]
        
        for x in range(5):
            D[x] = C[(x - 1) % 5] ^ self._rot64(C[(x + 1) % 5], 1)
        
        for x in range(5):
            for y in range(5):
                self.state[x][y] ^= D[x]
        
        x, y = 1, 0
        current = self.state[x][y]
        
        for t in range(24):
            X, Y = y, (2 * x + 3 * y) % 5
            self.state[x][y], current = current, self.state[X][Y]
            x, y = X, Y
        
        for y in range(5):
            T = [self.state[x][y] for x in range(5)]
            for x in range(5):
                self.state[x][y] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5])
        
        for round in range(24):
            self.state[0][0] ^= RC[round]

    def _absorb(self):
        while len(self.buffer) >= self.rate // 8:
            block = self.buffer[:self.rate // 8]
            
            for i in range(len(block) // 8):
                word = struct.unpack('<Q', block[i*8:(i+1)*8])[0]
                x, y = i % 5, i // 5
                self.state[x][y] ^= word
            
            self._keccak_f()
            self.buffer = self.buffer[self.rate // 8:]

    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.total_length += len(data)
        self.buffer.extend(data)
        self._absorb()

    def digest(self):
        padding = bytearray([0x06])
        while (len(self.buffer) + len(padding)) % (self.rate // 8) != 0:
            padding.append(0x00)
        padding[-1] |= 0x80
        
        self.buffer.extend(padding)
        self._absorb()
        
        output = bytearray()
        while len(output) < self.output_length // 8:
            block = bytearray()
            for i in range(self.rate // 64):
                x, y = i % 5, i // 5
                block.extend(struct.pack('<Q', self.state[x][y]))
            
            output.extend(block[:min(len(block), self.output_length // 8 - len(output))])
            
            if len(output) < self.output_length // 8:
                self._keccak_f()
        
        return output[:self.output_length // 8]

    def hexdigest(self):
        return self.digest().hex()

def sha3_256_hash(data):
    sha3 = SHA3_256()
    sha3.update(data)
    return sha3.hexdigest()

def sha3_256_file(filename, chunk_size=8192):
    sha3 = SHA3_256()
    
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha3.update(chunk)
    
    return sha3.hexdigest()