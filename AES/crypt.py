# -*- coding: utf-8 -*-
import base64
import hashlib
import random
import string
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding

class AESCipher(object):
    def __init__(self, key):
        self.key = (hashlib.md5(key.encode('utf-8')).hexdigest()).encode('utf-8')
        # self.key = key.encode('utf-8')

    def encrypt(self, raw):
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
        return base64.b64encode(iv + cipher.encrypt(data))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size, 'pkcs7')
        return data.decode('utf-8')

if __name__ == '__main__':
    key = input('Input key:\t')
    text = input('Input text:\t')
    # key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(32)])  # -> '4yKxQ5hMcUJixcG4Z8Lc5ZPBr5McS65X'

    cipher = AESCipher(key)

    encrypted = cipher.encrypt(text)
    print(encrypted)  # -> b'MLXpzLheE1383lHyVkGzoppMmO78otn3d0BOgh7WGdw='

    angou = input('Input text to decode:\t').encode('utf-8')
    print(cipher.key)
    decrypted = cipher.decrypt(angou)
    print(decrypted)  # -> 'plain text'

# TODO
### コマンドラインから改行含んだファイルを読み込む
#### 改行を含む入力を取得し続ける続ける方法
#### 改行 -> \n で変換
