import base64

name = "farai"
user = name.encode('ascii')
base64 = base64.b64encode(user)

print(base64)

print(base64.b64decode(base64))