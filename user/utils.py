import random
from string import ascii_letters, punctuation


EMAIL_MESSAGE = """
Hey {username}!
You're registrating on seller shop.
Just write this code - {code} - in 'code for email' field.
If it wasn't you just ignore this message.
Have a good day!
"""
AUTHENTICATION_MESSAGE = """
Hey {username}!
You're authenticating on seller shop
Just write this code - {code} - in 'code for email' field.
If it wasn't you just ignore this message.
Have a good day!
"""
DELETE_MESSAGE = """
Hey {username}!
You're deletining on seller shop
Just write this code - {code} - in 'code for email' field
If it wasn't you just know someone is on your account
Have a good day!"""

def create_token():
    '''
    Creates and returns 12-chars token
    '''
    token = list(ascii_letters + punctuation)
    random.shuffle(token)
        
    result = []
    for _ in range(12):
        result.append(token[random.randint(0, 30)])
        
    return ''.join(result)