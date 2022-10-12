## Monta Config

- What does it do?
    - Configuration file is a place that stores API keys for your system, and other sensitive information.
- JSONParser
    - Json Parser, are helper functions that make it easier for you to retrieve certain information from the config
      file.

# Functions

## get_config

- get_config
    - Returns the config file as a dictionary.

## Google Client ID

- get_google_client_id
    - Returns the Google Client ID from the config file.
    - Returns: String
    - Example: `get_google_client_id()`
    - Example Output: `1234567890-1234567890.apps.googleusercontent.com`
- update_google_client_id
    - Updates the Google Client ID in the config file.
    - Returns: None
    - Example: `update_google_client_id("1234567890-1234567890.apps.googleusercontent.com")`

# Google Client Secret

- get_google_client_secret
    - Returns the Google Client Secret from the config file.
    - Returns: String
    - Example: `get_google_client_secret()`
    - Example Output: `1234567890-1234567890.apps.googleusercontent.com`
- update_google_client_secret
    - Updates the Google Client Secret in the config file.
    - Returns: None
    - Example: `update_google_client_secret("1234567890-1234567890.apps.googleusercontent.com")`

# Google API Key

- get_google_api_key
    - Returns the Google API Key from the config file.
    - Returns: String
    - Example: `get_google_api_key()`
    - Example Output: `1234567890-1234567890.apps.googleusercontent.com`
- update_google_api_key
    - Updates the Google API Key in the config file.
    - Returns: None
    - Example: `update_google_api_key("1234567890-1234567890.apps.googleusercontent.com")`