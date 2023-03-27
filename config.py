from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt


# Generate the RSA private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

private_key = key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

print(private_key)


public_key = key.public_key()
publickey = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(publickey)

payload={"name": "harry"}

encode = jwt.encode(payload, private_key, algorithm='RS256')
print(encode)

decode = jwt.decode(encode, publickey, algorithms=['RS256'])
print(decode)