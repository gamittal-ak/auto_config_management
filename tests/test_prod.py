import requests  # Import the requests library, which allows you to send HTTP requests in Python


def get_response(url):
    """
    Sends a GET request to the specified URL with custom headers and returns the response.

    Parameters:
        url (str): The URL to which the GET request is sent.

    Returns:
        response (Response): The HTTP response received from the server.
    """
    # Define the custom headers to be sent with the request
    headers = {
        'Connection': 'keep-alive',  # Keep the connection open for possible reuse
        'Host': 'www.cyberabstract.com',
        'Pragma': (
            'akamai-x-get-cache-tags, X-Akamai-Request-ID, akamai-x-get-request-id,'
            'X-Akamai-UA, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable,'
            'akamai-x-get-cache-key, akamai-x-get-nonces, akamai-x-get-true-cache-key,'
            'akamai-x-serial-no, X-Akamai-Session-info, akamai-x-get-extracted-values,'
            'akamai-x-get-ssl-client-session-id, X-Akamai-CacheTrack,'
            'akamai-x-get-client-ip, akamai-x-feo-trace, akamai-x-tapioca-trace, Akamai-Request-BC'
        )  # Pragma header containing various Akamai-specific request and response tracing/debugging parameters
    }

    # Send a GET request to the specified URL with the headers defined above
    response = requests.get(url, headers=headers)

    # Return the HTTP response object received from the server
    return response


# Pytest tests case for 4xx or 3xx responses (optional, depending on your use case)
def test_get_response_status_code_in_range():
    """
    Test to ensure that the get_response function returns a status code in 2xx, 3xx, or 4xx ranges.
    """
    url = 'http://www.cyberabstract.com'
    response = get_response(url)

    # Assert that the status code is in the range 200-499
    assert 200 <= response.status_code < 500, f"Expected status code between 200 and 499, but got {response.status_code}"
