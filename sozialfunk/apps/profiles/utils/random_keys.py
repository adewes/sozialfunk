import random
import os.path
import string
import uuid
import binascii

def generate_unique_key():
    return str(uuid.uuid4()).replace('-','')

def generate_random_key(length = 16):
    def generate_random_key_16():
        allowed_chars = string.letters+string.digits
        return ''.join(map(lambda x:allowed_chars[x%len(allowed_chars)],map(lambda x:ord(x),binascii.unhexlify(str(uuid.uuid4()).replace('-','')))))
    if length <= 16:
        return generate_random_key_16()[:length]
    else:
        turns = int(length/16)
        if length % 16 != 0:
            turns+=1
        key = ''
        for i in range(0,turns):
            key+= generate_random_key_16()
        return key[:length]

def generate_random_filename(directory,extension,length = 16,prefix = ''):
    filename = ''
    while filename == '' or os.path.exists(filename):
        filename = directory+"/"+prefix+generate_random_key(length)+"."+extension
    return filename

def generate_random_directory_name(parent_directory,length = 16,prefix = ''):
    candidate_directory = ''
    full_directory = ''
    while candidate_directory == '' or os.path.exists(full_directory):
        candidate_directory = prefix+generate_random_key(length)
        full_directory = parent_directory+"/"+candidate_directory
    return candidate_directory

def generate_random_filename_key(directory,extension,length = 16,prefix = ''):
    filename = ''
    while filename == '' or os.path.exists(filename):
        key = generate_random_key(length)
        filename = directory+"/"+prefix+key+"."+extension
    return key
