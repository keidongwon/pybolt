import base64
from Crypto.Cipher import AES

BS = 16

# PKCS_PADDING
pad_pkcs = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad_pkcs = lambda s: s[:-ord(s[len(s)-1:])]

# ZEROS_PADDING
pad_zeros = lambda s: s + (BS - len(s) % BS) * chr(0).encode() if len(s) % BS != 0 else s
# def pad_zeros(raw):
#     if len(raw) % BS == 0:
#         return raw
#     padding_required = BS - (len(raw) % BS)
#     pad_char = b'\x00'
#     data = raw.encode('utf-8') + padding_required * pad_char
#     return data

unpad_zeros = lambda s: s.rstrip(b'\x00')
# def unpad_zeros(s):
#     s = s.rstrip(b'\x00')
#     return s


def iv():
    """
    The initialization vector to use for encryption or decryption.
    It is ignored for MODE_ECB and MODE_CTR.
    """
    return chr(0) * 16


class AESCipher(object):
    def __init__(self, key):
        self.key = key
        # self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, origin_msg, mode='ECB', padding='ZEROS'):
        origin_msg = origin_msg.encode('utf-8')
        if padding == 'PKCS':
            raw = pad_pkcs(origin_msg)
        else:
            raw = pad_zeros(origin_msg)
        if mode == 'CBC':
            cipher = AES.new(self.key, AES.MODE_CBC, iv())
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        enc_msg = cipher.encrypt(raw)
        return base64.b64encode(enc_msg).decode('utf-8')

    def decrypt(self, enc_msg, mode='ECB', padding='ZEROS'):
        enc_msg = base64.b64decode(enc_msg)
        if mode == 'CBC':
            cipher = AES.new(self.key, AES.MODE_CBC, iv())
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        dec_msg = cipher.decrypt(enc_msg)
        if padding == 'PKCS':
            return unpad_pkcs(dec_msg).decode('utf-8')
        return unpad_zeros(dec_msg).decode('utf-8')
