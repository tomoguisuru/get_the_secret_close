import requests
import hashlib
import json
from typing import Dict, List, Any


def process_traits_with_hash(url: str) -> Dict[str, Any]:
    """
    Fetches traits and key from URL, hashes traits using blake2b, and posts results back.

    Args:
        url (str): The URL to make requests to

    Returns:
        Dict[str, Any]: Response from the POST request

    Raises:
        requests.RequestException: If any HTTP request fails
        KeyError: If required fields are missing from response
    """
    try:
        # Get initial data
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract required fields
        traits: List[str] = data.get("traits", [])
        key: str = data.get("key", "")

        if not traits or not key:
            raise KeyError("Missing required 'traits' or 'key' in response")

        # Hash each trait using blake2b
        hashed_traits = []
        for trait in traits:
            hash_obj = hashlib.blake2b(digest_size=64, key=key.encode())
            hash_obj.update(trait.encode())
            hashed_traits.append(hash_obj.hexdigest())

        # Post hashed results back
        post_response = requests.post(url, json=hashed_traits)
        post_response.raise_for_status()

        return post_response.json()

    except requests.RequestException as e:
        raise Exception(f"HTTP request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Data validation failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


url = "https://api.close.com/buildwithus"
response = process_traits_with_hash(url)
print(response)
