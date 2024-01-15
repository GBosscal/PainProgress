"""
@Project: BackendForPain
@File: login.py
@Auth: Bosscal
@Date: 2023/10/7
@Description: 
"""
import bcrypt
import base64
import hashlib
import time
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


def verif_token(token):
    pass


def create_token(user_id):
    pass


# 存储密码
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


# 验证密码
def check_password(plain_password, hashed_password_str):
    hashed_password = hashed_password_str.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


def hash_string_with_timestamp(input_string):
    # 获取当前时间戳
    timestamp = str(time.time())

    # 将字符串和时间戳组合
    combined_string = input_string + timestamp

    # 使用 SHA-256 哈希算法进行哈希
    hashed_value = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()

    return hashed_value
