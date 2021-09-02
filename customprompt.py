from cmd import Cmd
import pyperclip
from cryptomodul import *


class OwnPrompt(Cmd):
    def __init__(self, pw, salt, file, ldict):
        Cmd.__init__(self)
        self.lang_dict = ldict
        self.user_pw = pw
        self.salt = salt
        self.pw_file = file
        self.aes_obj = AesCipher(self.user_pw, self.salt)
        self.storedPw_obj = StoredPw(self.pw_file, self.lang_dict, self.aes_obj)
        self.pw_list = self.storedPw_obj.read_pw_file()

    prompt = "passman> "

    def preloop(self) :
        print(self.lang_dict["prompt_intro"])

    #function to print all saved systems with usernames
    def do_show_sys(self, inp):
        text_to_print = self.lang_dict["acc_name"]
        text_to_print += "\n".join(
            ["{}\t{}".format(self.pw_list[i]["system"], self.pw_list[i]["username"]) for i in range(len(self.pw_list))])
        print(text_to_print)

    #function to generate new password
    def do_gen_new_pw(self, line):
        account_data = line.split()
        chosen_dict = next((dic for dic in self.pw_list if dic["system"] == account_data[0]), None)
        if chosen_dict is not None:
            while True:
                inp_choice = input(self.lang_dict["pw_exist"])
                if inp_choice.lower() == "y":
                    break
                elif inp_choice.lower() == "n":
                    return
                else:
                    print(self.lang_dict["unkn_choi"])
            chosen_dict["password"] = self.storedPw_obj.gen_rand_pw()
        else:
            account_data.append(self.storedPw_obj.gen_rand_pw())
            self.pw_list.append(dict(zip(["system", "username", "password"], account_data)))

        print(self.lang_dict["pw_saved"])

    #function to remove password
    def do_rem_pw(self, line):
        account_name = line.split()[0]
        rem_dict = next((dic for dic in self.pw_list if dic["system"] == account_name), None)

        if rem_dict is None:
            print(self.lang_dict["unk_acc"])
        else:
            self.pw_list.remove(rem_dict)
            print(self.lang_dict["pw_del"])

    #function to insert selected password into clipboard
    def do_get_pw(self, system):
        pw = next((dic["password"] for dic in self.pw_list if dic["system"] == system), None)

        if pw is None:
            print(self.lang_dict["unknown_pw"])
        else:
            pyperclip.copy(pw)
            print(self.lang_dict["pw_copied"])

    #function to clear clipboard
    def do_cb_clear(self, inp):
        pyperclip.copy("")

    #function to encrypt and save password. After this the prompt will be closed
    def do_exit(self, inp):
        self.storedPw_obj.write_pw_file(self.pw_list)
        pyperclip.copy("")
        return True

    #all help functions
    def help_show_sys(self):
        print(self.lang_dict["help_show_sys"])

    def help_gen_new_pw(self):
        print(self.lang_dict["help_gen_new_pw"])

    def help_get_pw(self):
        print(self.lang_dict["help_get_pw"])

    def help_rem_pw(self):
        print(self.lang_dict["help_rem_pw"])

    def help_cb_clear(self):
        print(self.lang_dict["help_cb_clear"])

    def help_exit(self):
        print(self.lang_dict["help_exit"])
