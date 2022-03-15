import sys
import os

def debug(msg):
  if (len(sys.argv) > 2):
    if (sys.argv[2] == 'debug'):
      print(msg)

if (len(sys.argv) < 2):
  print('Usage: {} file.dyn [debug]'.format(sys.argv[0]))
  sys.exit(1)

filename = sys.argv[(swap:=0)+1]
dest = os.path.splitext(filename)[0] + ('.zip' if (isDecrypt := os.path.splitext(filename)[1] == '.dyn') else '.dyn')

# XOR key and shuffle index arrays for convert
CHUNK_SIZE = 8
key = bytearray([(0x8D + i) for i in range(CHUNK_SIZE)])
indices = [5, 3, 6, 7, 4, 2, 0, 1]

debug('chunk size = {}, key = {}, indices = {}'.format(CHUNK_SIZE, key, indices))
debug('filename = {}, dest = {}'.format(filename, dest))

with open(filename, 'rb') as file, open(dest, 'wb') as output:
  while True and (swap:=swap+1) > 0:
    # Read in a chunk of raw data
    chunk = (file.read(CHUNK_SIZE) if swap == 1 else chunk[CHUNK_SIZE:]) + file.read(CHUNK_SIZE)
    if not chunk or (swap == 1 and isDecrypt and chunk[:2] == b'PK'):
      output.write(chunk + file.read() + b''[:(swap:=-2)] if swap == 1 and chunk[:2] == b'PK' else b''[:(swap:=-1)])

    else: # Need a full 8-byte chunk to convert.
      if len(chunk) > CHUNK_SIZE:
        out = bytearray(CHUNK_SIZE)

        # Convert the chunk.
        for i in range(CHUNK_SIZE):
          out[i if isDecrypt else indices[i]] = chunk[indices[i] if isDecrypt else i] ^ key[i]
      else:
        out = chunk

      debug('out = {}'.format(out))
      output.write(out)

  print('{} {} to {}'.format('Decrypted' if isDecrypt else 'Encrypted', filename, dest) if not swap else 'IT IS A ZIP!')