from typing import Hashable


import jwt

token = jwt.encode({'id': 7}, 'SECRET_KEY')
print(token)
print(jwt.decode(token.decode(), 'SECRET_KEY'))
