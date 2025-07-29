import requests
import hashlib
import json

from typing import List


class RequestException(Exception):
    """
    Custom error handler that will allow an error_code to be provided
    """

    def __init__(self, message: str, error_code: int):
        self.message = message
        self.error_code = error_code

        super().__init__(message)


def load_request(url: str) -> dict:
    """
    Performs a request to a url to retrieve a traits list
    """

    try:
        resp = requests.get(url)

        if resp.status_code != 200:
            raise RequestException(f"Response error", resp.status_code)

        return resp.json()
    except Exception as ex:
        raise Exception(f"Failed to retrieve traits: {str(ex)}")


def encode_values(values: List[str], key: str) -> List[str]:
    """
    Encodes a list of values using blake2b hash
    """
    encoded_values = []

    for value in values:
        hasher = hashlib.blake2b(key=key.encode("utf-8"), digest_size=64)
        hasher.update(value.encode("utf-8"))
        encoded_values.append(hasher.hexdigest())

    return encoded_values


def get_encoded_values(url: str) -> List[str]:
    """
    Reads a url and encodes the traits
    """
    data = load_request(url=url)

    for _key in ["traits", "key"]:
        if _key not in data:
            raise Exception(f"Response is missing {_key}")

    encoded = encode_values(data["traits"], data["key"])

    return encoded


def post_encoded_values(url: str, encoded_values: list[str]):
    try:
        resp = requests.post(url=url, data=json.dumps(encoded_values))
        if resp.status_code != 200:
            raise RequestException(f"Response error - {resp.reason}", resp.status_code)

        return resp.text
    except Exception as ex:
        raise Exception(f"Failed to retrieve traits: {str(ex)}")


def ingest_and_verify(url: str):
    encoded_values = get_encoded_values(url=url)
    return post_encoded_values(url=url, encoded_values=encoded_values)


url = "https://api.close.com/buildwithus"

ingest_and_verify(url=url)
