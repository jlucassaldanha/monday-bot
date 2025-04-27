import secrets

k = secrets.token_urlsafe(32)

print(k)
print(type(k))