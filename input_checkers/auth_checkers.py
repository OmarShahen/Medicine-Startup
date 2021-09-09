
import re


class Verification:

    def __init__(self):
        pass


    def is_name_valid(self,input_name):

        invalid_chars = '01234567890~`!@#$%^&*()_-=+\|]}[{:;?/><,.'
        for i in input_name:
            for j in invalid_chars:
                if i == j:
                    return False
        return True

    def is_password_valid(self, input_password):

        if len(input_password) < 8:
            return False
        return True
        

    def is_email_valid(self, input_email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, input_email):
            return True
        return False


    def is_phone_number_valid(self, input_phone):

        digits = '0123456789'

        if len(input_phone) != 11:
            return False
        
        for i in input_phone:
            valid = False
            for j in digits:
                if i == j:
                    valid = True

            if not valid:
                return False
        return True



