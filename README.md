Pass_man is CLI app for storing passwords (password manager). Passwords are saved in txt file and for encryption 256-bit AES cipher is used. Passwords are randomly generated. You can choose from two different languages-Czech or English.
When you need password pass_man will insert it into your clipboard. It is recomended to clear your clipboard when password is not needed, however pass_man wil do this during logout.

I faced some new challenges in this project. Implementing and understanding AES cipher was new to me and it was the main motivation for me to start this project. Also managing user acces to be save was interesting challenge, I hope it is done well, however I am still making some research about this topic and maybe some changes will appear.

In future I would like to implement: 
    - Two factor authorization, using SMS gateway or some API like Authy or Red Hat OTP
    - Possibility to store user`s own passwords (not only generated)
    - Password expiration
    - Possibility to change master password (password, that is used for opening the app)
