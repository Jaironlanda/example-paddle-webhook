from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


def validateWebhook(input_data):
  # Your Paddle public key.
  print(input_data)
  public_key = os.getenv('PADDLE_PUBLIC_KEY')

  import collections
  import base64

  # Crypto can be found at https://pypi.org/project/pycryptodome/
  from Crypto.PublicKey import RSA
  try:
    from Crypto.Hash import SHA1
  except ImportError:
    # Maybe it's called SHA
    from Crypto.Hash import SHA as SHA1
  try:
    from Crypto.Signature import PKCS1_v1_5
  except ImportError:
    # Maybe it's called pkcs1_15
    from Crypto.Signature import pkcs1_15 as PKCS1_v1_5
  import hashlib

  # PHPSerialize can be found at https://pypi.python.org/pypi/phpserialize
  import phpserialize

  # Convert key from PEM to DER - Strip the first and last lines and newlines, and decode
  public_key_encoded = public_key[26:-25].replace('\n', '')
  public_key_der = base64.b64decode(public_key_encoded)

  # input_data represents all of the POST fields sent with the request
  # Get the p_signature parameter & base64 decode it.
  signature = input_data['p_signature']

  # Remove the p_signature parameter
  del input_data['p_signature']

  # Ensure all the data fields are strings
  for field in input_data:
    input_data[field] = str(input_data[field])

  # Sort the data
  sorted_data = collections.OrderedDict(sorted(input_data.items()))

  # and serialize the fields
  serialized_data = phpserialize.dumps(sorted_data)

  # verify the data
  key = RSA.importKey(public_key_der)
  digest = SHA1.new()
  digest.update(serialized_data)
  verifier = PKCS1_v1_5.new(key)
  signature = base64.b64decode(signature)

  if verifier.verify(digest, signature):
    return True
  else:
    return False

@app.post('/webhook')
async def webhook(req: Request):
  if req.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
    body = await req.form()

    return {'result': validateWebhook(dict(body))}
  else:
    return {'message': 'Content type not supported.'}

  