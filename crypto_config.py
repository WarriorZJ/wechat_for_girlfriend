"""
config.conf 加密 / 解密工具（Fernet 对称加密）
------------------------------------------------
- 加密：将明文 config.conf 加密为 config.conf.enc（可安全提交到仓库）
- 解密：运行时用环境变量 WECHAT_CONF_KEY 解密，还原出 config.conf

依赖：cryptography（已在 requirements.txt）

用法：
    python crypto_config.py encrypt   # 生成 config.conf.enc，并打印密钥（请妥善保管）
    python crypto_config.py decrypt   # 用 WECHAT_CONF_KEY 还原 config.conf
"""
import os
import sys

from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENC_FILE = os.path.join(BASE_DIR, "config.conf.enc")
PLAIN_NAME = "config.conf"  # 解密后写到「当前工作目录」，与 main.py 的读取位置一致


def _key():
    k = os.environ.get("WECHAT_CONF_KEY")
    if not k:
        raise RuntimeError("请在环境变量 WECHAT_CONF_KEY 中设置解密密钥（Fernet key）")
    return k.encode() if isinstance(k, str) else k


def decrypt_config():
    """解密 config.conf.enc → 当前目录的 config.conf，返回路径。"""
    if not os.path.exists(ENC_FILE):
        raise FileNotFoundError("未找到 config.conf.enc，无法解密")
    with open(ENC_FILE, "rb") as f:
        token = f.read()
    plain = Fernet(_key()).decrypt(token)
    out = os.path.join(os.getcwd(), PLAIN_NAME)
    with open(out, "wb") as f:
        f.write(plain)
    return out


def encrypt_config(plain_path=None):
    """加密 config.conf → config.conf.enc，返回 (密钥, 密文路径)。

    密钥策略：
    - 若环境变量 WECHAT_CONF_KEY 已设置 → 复用该密钥（只更新密文，GitHub Secret 无需改动）
    - 否则 → 现生成新密钥（此时需同步更新 GitHub Secret WECHAT_CONF_KEY）

    密钥务必自行保管，不要提交。
    """
    plain_path = plain_path or os.path.join(os.getcwd(), PLAIN_NAME)
    if not os.path.exists(plain_path):
        raise FileNotFoundError(f"未找到明文配置：{plain_path}")
    with open(plain_path, "rb") as f:
        data = f.read()

    env_key = os.environ.get("WECHAT_CONF_KEY")
    if env_key:                       # 复用现有密钥：更新密文，但 Secret 不变
        key = env_key.encode() if isinstance(env_key, str) else env_key
        reused = True
    else:                            # 未设密钥：生成新密钥（需同步更新 Secret）
        key = Fernet.generate_key()
        reused = False

    token = Fernet(key).encrypt(data)
    with open(ENC_FILE, "wb") as f:
        f.write(token)
    return key, ENC_FILE, reused


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "encrypt":
        key, path, reused = encrypt_config()
        if reused:
            print("已复用环境变量 WECHAT_CONF_KEY 更新密文，GitHub Secret 无需改动。")
        else:
            print("密钥（新生成，请妥善保管，并同步更新 GitHub Secret WECHAT_CONF_KEY）：")
            print(key.decode())
        print("已生成密文：", path)
    elif len(sys.argv) > 1 and sys.argv[1] == "decrypt":
        print("已解密：", decrypt_config())
    else:
        print("用法: python crypto_config.py encrypt | decrypt")
