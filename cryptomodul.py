import getpass
import bcrypt
import os.path as osp
import string
import random
from Cryptodome import Random as cRand
from Cryptodome.Cipher import AES
import base64


class MasterPw:
    def __init__(self, pw_file, ldict):
        self.pw_file = pw_file
        self.lang_dict = ldict

    # This function takes password from user and saves it in hash format to specified file
    def save_password(self):
        while True:
            user_pw = getpass.getpass(self.lang_dict["input_pw"])
            check_pw = getpass.getpass(self.lang_dict["input_pw_rep"])

            if check_pw == user_pw:
                break
            else:
                print(self.lang_dict["diff_pw"])

        salt = bcrypt.gensalt()
        hash_val = bcrypt.hashpw(user_pw.encode("utf8"), salt)

        with open(self.pw_file, "wb") as f:
            f.write(hash_val)

        print(self.lang_dict["pw_saved"])

        return user_pw, salt

    #This function checks password from input with saved hash
    def check_password(self):
        if osp.exists(self.pw_file):
            with open(self.pw_file, "rb") as f:
                hash_val = f.readline()
        else:
            return False

        print(self.lang_dict["acc_exist"])
        input_passw = getpass.getpass(self.lang_dict["input_pw"])

        if bcrypt.checkpw(input_passw.encode("utf8"), hash_val):
            return input_passw, hash_val[:29]
        else:
            return None, None


class StoredPw:
    def __init__(self, fpath, ldict, aes_obj):
        self.pw_file = fpath
        self.lang_dict = ldict
        self.aes_obj = aes_obj

    def read_pw_file(self):
        with open(self.pw_file, "rb") as f:
            f_cont = f.read()

        if f_cont == b"":
            return []

        f_decrypt = self.aes_obj.decrypt(f_cont)
        pw_list = []
        first_line = True
        keys = []

        for line in str(f_decrypt).split("\n"):
            if first_line:
                keys = line.split("\t")
                first_line = False
            else:
                pw_list.append(dict(zip(keys, line.split("\t"))))

        return pw_list

    def write_pw_file(self, pw_list):
        file_text = "\t".join(pw_list[0].keys()) + "\n"
        file_text += "\n".join(["\t".join(pw_list[i].values()) for i in range(len(pw_list))])
        with open(self.pw_file, "wb") as f:
            f.write(self.aes_obj.encrypt(file_text))

    def gen_rand_pw(self, pw_len=None):
        if pw_len is None:
            pw_len = 15
        elif not isinstance(pw_len, int):
            print(self.lang_dict["err_len_int"])
            return

        digits = [d for d in range(10)]
        l_case_chars = list(string.ascii_lowercase)
        u_case_chars = list(string.ascii_uppercase)
        symbols = list(string.punctuation)

        combined = digits + l_case_chars + u_case_chars + symbols

        pw_list = random.choices(population=combined, k=(pw_len - 4))

        #to be sure that from every list at least one value will be chosen
        pw_list.append(random.choice(digits))
        pw_list.append(random.choice(l_case_chars))
        pw_list.append(random.choice(u_case_chars))
        pw_list.append(random.choice(symbols))

        random.shuffle(pw_list)

        return "".join(map(str, pw_list))


class AesCipher:
    def __init__(self, pw, salt):
        self.key = bcrypt.kdf(pw.encode(), salt, 16, 32, True)
        self.bs = AES.block_size

    def encrypt(self, raw_text):
        raw_text = self._pad(raw_text)
        iv = cRand.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw_text.encode()))

    def decrypt(self, enc_text):
        enc_text = base64.b64decode(enc_text)
        iv = enc_text[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc_text[AES.block_size:])).decode()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]






