import base64

def decode_b64(text: str) -> str:
    decoded_bytes = base64.b64decode(text)
    return decoded_bytes.decode('utf-8')

def decode_b32(text: str) -> str:
    decoded_bytes = base64.b32decode(text)
    return decoded_bytes.decode('utf-8')

def decode_b16(text: str) -> str:
    decoded_bytes = base64.b16decode(text)
    return decoded_bytes.decode('utf-8')

def encode_b64(text: str) -> str:
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def encode_b32(text: str) -> str:
    encoded_bytes = base64.b32encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def encode_b16(text: str) -> str:
    encoded_bytes = base64.b16encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')
