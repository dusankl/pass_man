# imports
from customprompt import OwnPrompt
from cryptomodul import *
import json


def select_language():
    with open(".lang.json", "r") as jsonf:
        all_lang_dict = json.load(jsonf)

    print(" / ".join([all_lang_dict[k]["lang_select"] for k in all_lang_dict.keys()]))

    zipped = set(zip(all_lang_dict.keys(), [all_lang_dict[k]["lang_name"] for k in all_lang_dict.keys()]))
    lang_possibilities = [" - ".join(tup) for tup in zipped]

    error_text = " / ".join([all_lang_dict[k]["lang_invalid"] for k in all_lang_dict.keys()])

    while True:
        lang_chosen = input("{}\n".format(lang_possibilities))

        if lang_chosen.lower() in all_lang_dict.keys():
            return all_lang_dict[lang_chosen]
        else:
            print(error_text)


def main():
    pws_db_file = ".passwords.txt"
    ultimate_pw_file = ".ult_passw.txt"

    lang_dict = select_language()

    master_pw_handler = MasterPw(ultimate_pw_file, lang_dict)

    print(lang_dict["welc"])

    # Authenticate user
    if osp.exists(pws_db_file):
        user_pw, salt = master_pw_handler.check_password()
        if user_pw is not None:
            print(lang_dict["login_ok"])
        else:
            print(lang_dict["login_ko"])
            return

    else:
        print(lang_dict["no_pw"])
        user_pw, salt = master_pw_handler.save_password()

    # main program loop

    OwnPrompt(user_pw, salt, pws_db_file, lang_dict).cmdloop()

    print("Program ukoncen\nUzivatel odhlasen")


if __name__ == "__main__":
    main()
