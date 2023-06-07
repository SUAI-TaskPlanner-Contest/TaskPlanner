import cryptocode


def encrypt(raw_data: str, pincode: str) -> str:
    """
                Encrypts data with a pincode

                parameters:
                    raw_data: data to encrypt, pincode: key to encrypt
                returns:
                    encrypt data

     """
    en_data = cryptocode.encrypt(raw_data, pincode)
    assert en_data != False
    return en_data


def decrypt(en_data: str, pincode: str) -> str:
    """
                    decrypts data with a pincode

                    parameters:
                        raw_data: data to decrypt, pincode: key to decrypt
                    returns:
                        decrypt data

    """
    dec_data = cryptocode.decrypt(en_data, pincode)
    assert dec_data != False
    return dec_data
