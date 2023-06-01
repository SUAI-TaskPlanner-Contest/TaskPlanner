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
    return dec_data
