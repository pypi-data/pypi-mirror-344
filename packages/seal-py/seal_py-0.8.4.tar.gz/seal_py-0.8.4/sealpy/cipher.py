import random

try:
    import config
    import utilitis
except:
    from . import config
    from . import utilitis



class Enigma:
    def __init__(self, key):
        self.key = key

    def cipher_text(self, text: str) -> str:
        key =self.key
        offset = key[:3]
        keyOf = key[3:]
        cipher_text = list(text)

        for char in range(len(cipher_text)):

            cipher_text[char] = chr(ord(cipher_text[char]) + int(offset))


        for char in range(len(cipher_text)):
            key_code = -1
            try: 
                key_code = int(char % len(keyOf)) * -1

            except: 
                key_code = ord(char % len(keyOf))

            cipher_text[char] = chr(ord(cipher_text[char]) + key_code)

        

        output_text = utilitis.get_text_from_array(cipher_text)
        
        return output_text
    
    def anti_cipher_text(self, text: str):
        key = self.key
        offset = key[:3]
        keyOf = key[3:]
        cipher_text = list(text)


        for char in range(len(cipher_text)):
            key_code = -1
            try: 
                key_code = int(char % len(keyOf)) * -1

            except: 
                key_code = ord(char % len(keyOf))

            cipher_text[char] = chr(ord(cipher_text[char]) - key_code)

        for char in range(len(cipher_text)):
            cipher_text[char] = chr(ord(cipher_text[char]) - int(offset))

        output_text = utilitis.get_text_from_array(cipher_text)
        
        return output_text
    
    @staticmethod
    def generate_key(key_length):
        key = ""
        key += str(random.randint(200, 300))
        for char in range(key_length):
            key += config.SYMBWOL[random.randint(0, len(config.SYMBWOL) - 1)]
            key += str(random.randint(0, 9))

        return key
    
    @staticmethod
    def generate_key_from_hash(hash_data):
        sum_of_elements = 0

        for el in hash_data:
            try:
                int_hash_el = int(el)
                sum_of_elements += int_hash_el
            except:
                sum_of_elements += config.SYMBWOL.index(el.upper())
        
        while sum_of_elements > 300:
            sum_of_elements *= 0.8
            sum_of_elements = int(sum_of_elements)

        while sum_of_elements < 200:
            sum_of_elements *= 1.5
            sum_of_elements = int(sum_of_elements)


        key = str(sum_of_elements)

        for i, el in enumerate(hash_data):
            if i < len(hash_data) - 1:
                try:
                    int_hash_el = int(hash_data[i])
                    key += config.SYMBWOL[int_hash_el]
                except:
                    key += hash_data[i].upper()
                try:
                    int_hash_el = int(hash_data[i + 1])
                    key += str(int_hash_el)
                except:
                    key += str(config.SYMBWOL.index(hash_data[i + 1].upper()))
        

        return key
    

                



    

