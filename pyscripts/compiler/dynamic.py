import shutil
CHUNK_SIZE = 8
key = bytearray([(0x8D + i) for i in range(CHUNK_SIZE)])
indices = [5, 3, 6, 7, 4, 2, 0, 1]


def zip_to_dyn(filename):
    out = bytearray(CHUNK_SIZE)
    dest = filename[:-3] + 'dyn'
    with open(filename, 'rb') as file, open(dest, 'wb') as output:
        chunk = file.read(CHUNK_SIZE)
        while len(chunk) == CHUNK_SIZE:
            for i in range(CHUNK_SIZE):
                out[indices[i]] = chunk[i] ^ key[i]
            output.write(out)
            chunk = file.read(CHUNK_SIZE)
        output.write(chunk)

def dyn_to_zip(filename):
    CHUNK_SIZE = 1024

    out = bytearray(CHUNK_SIZE)
    dest = filename[:-3] + "zip"

    try:
        with ZipFile(filename, mode='r') as f:
            pass
    except Exception:
        pass
    else:
        shutil.copy(filename, dest)
        return


    with open(filename, 'rb') as file, open(dest, 'wb') as output:
        swap = 0
        while True:
            swap += 1
            if swap <= 0:
                break
            chunk = (file.read(CHUNK_SIZE) if swap == 1 else chunk[CHUNK_SIZE:]) + file.read(CHUNK_SIZE)

            if not chunk:
                swap = -1
                output.write(chunk + file.read())
            elif swap == 1 and chunk[:2] == b'PK':
                swap = -2
                output.write(chunk + file.read())
            elif len(chunk) > CHUNK_SIZE:
                out = bytearray(CHUNK_SIZE)
                for i in range(CHUNK_SIZE):
                    out[i] = chunk[indices[i]] ^ key[i]
                output.write(out)
            else:
                output.write(chunk)