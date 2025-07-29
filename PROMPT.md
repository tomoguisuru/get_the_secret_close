In a file named, copilot_prompt.py, create a python function that take a url as a parameter and will make a GET request using that url to retrieve the "traits" and "key" values. "traits" should be a list of string and "key" should be a string.

Using blake2b hash with the key value and a digest size of 64, encode each of the values from "traits" into a list called encoded_values

Send a POST request to the url using the encoded_values as json. Do not use an object, post the encoded_values directly

Return the response text if successful