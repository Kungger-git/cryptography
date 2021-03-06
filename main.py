import argparse
import string
from base64 import b64decode, b64encode


class Cipher:

    def __init__(self, text, shift):
        for key in shift:
            self.text = text
            self.key = key

    def encode_message(self):
        result_text = ""

        for i in range(len(self.text)):
            char = self.text[i]
            if (char.isupper()):
                result_text += chr((ord(char) + int(self.key) - 65) % 26 + 65)
            elif char == ' ':
                result_text += ' '
            elif char in string.punctuation:
                result_text += char
            else:
                result_text += chr((ord(char) + int(self.key) - 97) % 26 + 97)

        encoded_message = result_text.encode('utf-8')
        for _ in range(int(self.key)):
            encoded_message = b64encode(encoded_message)

        print(encoded_message.decode('utf-8'))


class Decoder:

    def __init__(self, text):
        for message in text:
            self.message = message

    def decode_message(self):
        import binascii
        for key in range(len(string.ascii_letters)):
            try:
                decoded_message = self.message.encode('utf-8')
                for _ in range(key):
                    decoded_message = b64decode(decoded_message)

                translated = ''
                for symbol in decoded_message.decode('utf-8'):
                    if (symbol in string.ascii_letters):
                        num = string.ascii_letters.find(symbol)
                        num -= key
                        if (num < 0):
                            num += len(string.ascii_letters)
                        translated += string.ascii_letters[num]
                    else:
                        translated += symbol

                print('Key Test #%s: %s' % (key, translated))
            except (binascii.Error, UnicodeDecodeError):
                print('\nKey Found! #%s' % (key - 1))
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Encodes and Decodes.')

    parser.add_argument('-m', '--message',
                        nargs=1, type=int, action='store',
                        help='Encodes input text. Required Argument is key shift. (e.g. -m 3)')

    parser.add_argument('-d', '--decode',
                        nargs=1, metavar='DECODE',
                        action='store',
                        help="Brute Forces to decode a Caesar Cipher Text. (e.g. -d 'TnJza25zamM=')")

    args = parser.parse_args()

    if args.message:
        try:
            while True:
                message = input("Message: ")
                Cipher(message, [key for key in args.message]).encode_message()
        except KeyboardInterrupt as c:
            print('\n\nStopped!')

    if args.decode:
        Decoder([x for x in args.decode]).decode_message()
