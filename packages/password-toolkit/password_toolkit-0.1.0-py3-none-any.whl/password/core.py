import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# 多语言配置
current_lang = "en"

translations = {
    "en": {
        "errors": {
            "invalid_format": "Invalid encrypted string format",
            "key_required": "Key is required for decryption",
            "key_type_error": "Key must be a string",
            "incorrect_key": "Incorrect key",
            "lang_error": "Unsupported language. Available options: cn/en"
        },
        "help_text": """
        Password Encryption Module Usage
        ================================
        
        Functions:
        1. format(text, [key]) -> encrypted_str
        2. un(encrypted_str, [key]) -> original_text
        3. help() -> Display this message
        4. lang(cn/en) -> Switch language
        
        Parameters:
        - text: String to encrypt/decrypt
        - key:  Optional encryption key (string)
        
        Examples:
        # Encryption
        encrypted = password.format("secret")
        encrypted_with_key = password.format("secret", "mykey")
        
        # Decryption
        decrypted = password.un(encrypted)
        decrypted_with_key = password.un(encrypted_with_key, "mykey")
        
        Security Features:
        - AES-256-CBC encryption
        - PBKDF2 key derivation
        - Random salt and IV generation
        - Automatic padding
        
        Error Handling:
        - Raises ValueError for:
          * Invalid encrypted format
          * Incorrect key
          * Corrupted data
        
        Note: Always use strong keys and keep them safe!
        """
    },
    "cn": {
        "errors": {
            "invalid_format": "加密字符串格式无效",
            "key_required": "解密需要提供密钥",
            "key_type_error": "密钥必须为字符串",
            "incorrect_key": "密钥不正确",
            "lang_error": "不支持的语言，可选值：cn/en"
        },
        "help_text": """
        密码加密模块使用说明
        =======================
        
        函数列表：
        1. format(文本, [密钥]) -> 加密字符串
        2. un(加密字符串, [密钥]) -> 原始文本
        3. help() -> 显示本帮助信息
        4. lang(cn/en) -> 切换语言
        
        参数说明：
        - 文本: 需要加密/解密的字符串
        - 密钥: 可选加密密钥（字符串）
        
        使用示例：
        # 加密
        encrypted = password.format("秘密信息")
        encrypted_with_key = password.format("秘密信息", "我的密钥")
        
        # 解密
        decrypted = password.un(encrypted)
        decrypted_with_key = password.un(encrypted_with_key, "我的密钥")
        
        安全特性：
        - 使用AES-256-CBC加密算法
        - PBKDF2密钥派生
        - 随机生成盐和初始向量(IV)
        - 自动填充
        
        错误处理：
        - 抛出ValueError异常的情况：
          * 加密字符串格式无效
          * 密钥不正确
          * 数据损坏
        
        注意：请务必使用强密钥并妥善保管！
        """
    }
}

DEFAULT_KEY = "default_password_key_please_change"

def lang(language):
    """切换模块语言（cn/en）"""
    global current_lang
    if language.lower() in ("cn", "en"):
        current_lang = language.lower()
    else:
        raise ValueError(translations[current_lang]["errors"]["lang_error"])

def format(plaintext, key=None):
    """加密文本"""
    use_default_key = key is None
    if use_default_key:
        key = DEFAULT_KEY
    elif not isinstance(key, str):
        raise TypeError(translations[current_lang]["errors"]["key_type_error"])

    salt = os.urandom(16)
    iv = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    secret_key = kdf.derive(key.encode("utf-8"))

    cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    flag = 0 if use_default_key else 1
    encoded_salt = base64.urlsafe_b64encode(salt).decode().strip("=")
    encoded_iv = base64.urlsafe_b64encode(iv).decode().strip("=")
    encoded_ciphertext = base64.urlsafe_b64encode(ciphertext).decode().strip("=")

    return f"{flag}${encoded_salt}${encoded_iv}${encoded_ciphertext}"

def un(encrypted_str, key=None):
    """解密文本"""
    parts = encrypted_str.split("$")
    if len(parts) != 4:
        raise ValueError(translations[current_lang]["errors"]["invalid_format"])

    flag_str, encoded_salt, encoded_iv, encoded_ciphertext = parts
    flag = int(flag_str)

    # Base64解码
    salt = base64.urlsafe_b64decode(encoded_salt + "=" * (-len(encoded_salt) % 4))
    iv = base64.urlsafe_b64decode(encoded_iv + "=" * (-len(encoded_iv) % 4))
    ciphertext = base64.urlsafe_b64decode(encoded_ciphertext + "=" * (-len(encoded_ciphertext) % 4))

    # 密钥处理
    if flag == 1:
        if key is None:
            raise ValueError(translations[current_lang]["errors"]["key_required"])
    else:
        key = DEFAULT_KEY

    if not isinstance(key, str):
        raise TypeError(translations[current_lang]["errors"]["key_type_error"])

    # 密钥派生
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    secret_key = kdf.derive(key.encode("utf-8"))

    # 解密处理
    cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # 去除填充
    unpadder = padding.PKCS7(128).unpadder()
    try:
        plaintext_data = unpadder.update(padded_data) + unpadder.finalize()
    except ValueError:
        raise ValueError(translations[current_lang]["errors"]["incorrect_key"])

    return plaintext_data.decode("utf-8")

def help():
    """显示帮助信息"""
    print(translations[current_lang]["help_text"].strip())

# 初始化帮助文档
help.__doc__ = help.__doc__.strip()
