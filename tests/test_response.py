import requests
import sys

def get_response(url):
    """
    Sends a GET request to the specified URL with custom headers and returns the response.

    Parameters:
        url (str): The URL to which the GET request is sent.

    Returns:
        response (Response): The HTTP response received from the server.
    """
    # Define minimal custom headers
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.cyberabstract.com'
    }

    # Send a GET request to the specified URL with the headers defined above
    response = requests.get(url, headers=headers)

    # Return the HTTP response object received from the server
    return response


def test_get_response_status_code_in_range(url):
    """
    Test to ensure that the get_response function returns a status code in 2xx, 3xx,
    or returns 404 as a success.
    """
    response = get_response(url)

    # Assert that the status code is in the range 200-399 or 404
    assert (200 <= response.status_code < 400) or response.status_code == 404, \
        f"Expected status code between 200-399 or 404, but got {response.status_code}"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 test_response.py <environment>")
        print("Example: python3 test_response.py staging")
        print("Example: python3 test_response.py production")
        exit(1)

    # Get the environment (production or staging) from command-line arguments
    environment = sys.argv[1].lower()

    # Set the appropriate URL based on the environment
    if environment == 'staging':
        url = 'http://www.cyberabstract.com.edgesuite-staging.net'
    elif environment == 'production':
        url = 'http://www.cyberabstract.com'
    else:
        print(f"Invalid environment: {environment}. Use 'staging' or 'production'.")
        exit(1)

    # Run the test for the appropriate environment
    test_get_response_status_code_in_range(url)
    print(f"Test passed for {environment} environment.")
