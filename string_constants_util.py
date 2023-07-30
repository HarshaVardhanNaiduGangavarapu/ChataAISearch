# This file holds the strings constant information

class StringConstantUtil:
    READ_PERM = 'r'
    POST = 'POST'
    NEW_LINE = '\n'
    FULL_STOP = '.'
    SWAGGER = '/swagger'
    HEALTH = '/health'
    SEARCH = '/search'
    SEARCH_STR = 'str'
    SWAGGER_JSON = '/swagger.json'
    FILE_SWAGGER_JSON = 'swagger.json'
    RESOURCES_KING_FILE = 'resources/king-i-150.txt'

    # Error messages
    ERROR = 'Error'
    BAD_REQUEST = 'Bad Request'
    CONTACT_ADMIN_MSG = 'Please contact administrator.'
    INVALID_REQ_DATA_MSG = "Invalid request data. Please use JSON data format with 'str' as key and <search_text> as " \
                           "value."
    INVALID_JSON_REQ_BODY = "Invalid JSON request body. Please use JSON data format with 'str' as key and " \
                            "<search_text> as value."
    MULTIPLE_KEYS_MSG = "Request body should contain only 'str' as key."
    MISSING_STR_KEY_MSG = "Request body should contain 'str' as key."
    MISSING_STR_VALUE_MSG = "Request body should contain 'str' value and cannot be empty."
    UNSUPPORTED_MEDIA_TYPE_MSG = "Unsupported media type. Please use 'application/json' format."

    # Logs constants
    REQUEST_INFO = 'API Request Info: %s %s'
    REQUEST_BODY = 'API Request Body Info: %s'
    RESPONSE_INFO = 'API Response Info: %s %s'
    EXCEPTION_INFO = 'Exception MSG: %s'
    LOG_FILE_NAME_PATH = 'logs/chataAISearch.log'

