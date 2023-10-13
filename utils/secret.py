"""
@Project: BackendForPain
@File: login.py
@Auth: Bosscal
@Date: 2023/10/7
@Description: 
"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from const import AppSecretKey


# 加密函数
def encrypt(plaintext):
    cipher = AES.new(AppSecretKey, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv + ciphertext


# 解密函数
def decrypt(ciphertext):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(AppSecretKey, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()


# 将二进制数据转换为Base64字符串
def binary_to_base64(binary_data):
    return base64.b64encode(binary_data).decode()


# 将Base64字符串转换为二进制数据
def base64_to_binary(base64_string):
    return base64.b64decode(base64_string)


def get_token(code):
    # 去请求微信，同时获取到
    pass


def verif_token(token):
    pass
