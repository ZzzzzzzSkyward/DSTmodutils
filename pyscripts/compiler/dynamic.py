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
    from zipfile import ZipFile
    out = bytearray(CHUNK_SIZE)
    dest = filename[:-3] + "zip"
    try:
        f = ZipFile(filename,mode='r')
        f.close()
        shutil.copy(filename, dest)
        return
    except Exception:
        pass
    swap = 0
    with open(filename, 'rb') as file, open(dest, 'wb') as output:
        while True and (swap := swap + 1) > 0:
            chunk = (file.read(CHUNK_SIZE) if swap ==
                     1 else chunk[CHUNK_SIZE:]) + file.read(CHUNK_SIZE)
            if not chunk or (swap == 1 and chunk[:2] == b'PK'):
                output.write(chunk +
                             file.read() +
                             b''[:(swap := -
                                   2)] if swap == 1 and chunk[:2] == b'PK' else b''[:(swap := -
                                                                                      1)])
            else:
                if len(chunk) > CHUNK_SIZE:
                    out = bytearray(CHUNK_SIZE)
                    for i in range(CHUNK_SIZE):
                    out[i] = chunk[indices[i]] ^ key[i]
                else:
                    out = chunk
            output.write(out)
