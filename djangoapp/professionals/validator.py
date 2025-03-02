import re
from rest_framework.status import *

def isTaxNumberValid(taxNumber):
    """ If cnpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """

    # Check if type is str
    if not isinstance(taxNumber,str):
        return {
                    "success": False, 
                    "status_code": HTTP_400_BAD_REQUEST, 
                    "message": f"CPF informado precisa ser uma string: {taxNumber}", 
                    "error": "CPF informado precisa ser uma string"
                    }

    # Remove some unwanted characters
    taxNumber = re.sub("[^0-9]",'',taxNumber)

    # Checks if string has 11 characters
    if len(taxNumber) != 11:
        return {
                    "success": False, 
                    "status_code": HTTP_400_BAD_REQUEST, 
                    "message": f"CPF informado precisa ter 11 caracteres: {taxNumber}", 
                    "error": "CPF informado precisa ter 11 caracteres"
                    }

    # Check if all digits are equal
    if (taxNumber == taxNumber[0] * 11):
        return {
                    "success": False, 
                    "status_code": HTTP_400_BAD_REQUEST, 
                    "message": f"CPF informado não é válido: {taxNumber}", 
                    "error": "CPF informado não é válido"
                    }
    
    sum = 0
    weight = 10

    """ Calculating the first taxNumber check digit. """
    for n in range(9):
        sum = sum + int(taxNumber[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    """ Calculating the second check digit of taxNumber. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(taxNumber[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if taxNumber[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return {
                    "success": False, 
                    "status_code": HTTP_400_BAD_REQUEST, 
                    "message": f"CPF informado não é válido: {taxNumber}", 
                    "error": "CPF informado não é válido"
                    }