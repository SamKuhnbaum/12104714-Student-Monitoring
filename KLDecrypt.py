import random, struct, os, os.path
from Crypto.Cipher import AES

# Decryption Settings
INFILE = "enkeylog.txt"
OUTFILE = "dekeylog.txt"
key = 'k3yl0gg3r3dI0I37'


def AESDecryption(k, in_file, out_file, chunksize=24*1024):
    with open(in_file, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

AESDecryption(key, INFILE, OUTFILE)
