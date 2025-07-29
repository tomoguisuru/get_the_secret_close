from hashlib import blake2b
import json
import requests


# Fetch traits and key from URL


def process_traits(url):
    response = requests.get(url)
    data = response.json()
    traits = data["traits"]
    key = data["key"]

    # Generate hashes for each trait
    trait_hashes = []
    for trait in traits:
        # Create blake2b hash object with digest size 64
        h = blake2b(digest_size=64, key=key.encode())
        # Update hash with trait
        h.update(trait.encode())
        # Get hex digest and add to list
        trait_hashes.append(h.hexdigest())

    # Convert to JSON
    json_output = json.dumps(trait_hashes, indent=2)

    # Submit JSON data via POST request
    response = requests.post(url, json=trait_hashes)

    # Check if response is OK (200)
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error: Status code {response.status_code}")

    return json_output


url = "https://api.close.com/buildwithus"
response = process_traits(url)
print(response)
