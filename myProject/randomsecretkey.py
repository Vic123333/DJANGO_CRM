import requests
import binascii

def fetch_quantum_random_bytes(num_bytes):
    """Fetch quantum random bytes from the ANU QRNG service."""
    url = 'https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8'.format(num_bytes)
    response = requests.get(url)
    data = response.json()
    
    if data['success']:
        # Convert the list of numbers to bytes
        random_bytes = bytearray(data['data'])
        return random_bytes
    else:
        raise RuntimeError("Failed to fetch quantum random data.")

def generate_secret_key(num_bytes):
    """Generate a secret key of the specified length using quantum random bytes."""
    random_bytes = fetch_quantum_random_bytes(num_bytes)
    secret_key = binascii.hexlify(random_bytes).decode('utf-8')
    return secret_key

# Specify the length of the key in bytes
key_length = 64  # Example: 64 bytes

# Generate the secret key
secret_key = generate_secret_key(key_length)
print("Quantum-generated Secret Key:", secret_key)
