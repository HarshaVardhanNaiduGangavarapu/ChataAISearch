from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from log_config import setup_logger
from string_constants_util import StringConstantUtil
from flask import Flask, request, jsonify
from flask_caching import Cache
import json
import os

# Author: Harsha Gangavarapu
# Description: Service layer for Chata AI search API service application
app = Flask(__name__)

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

# Configure Swagger UI
SWAGGER_URL = StringConstantUtil.SWAGGER
API_URL = StringConstantUtil.SWAGGER_JSON
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Chata Search API"
    }
)
# Register Swagger
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Setup logging
logger = setup_logger('app.py')


# Log API requests INFO
@app.before_request
def log_api_req_info():
    logger.info(StringConstantUtil.REQUEST_INFO, request.method, request.url)
    if request.method == StringConstantUtil.POST:
        logger.info(StringConstantUtil.REQUEST_BODY, request.data)


@app.after_request
def after_request(response):
    # skip swagger APIs response logging
    if 'swagger' in request.url:
        return response
    status_code = response.status_code
    # Log the response
    if 200 <= status_code <= 299:
        logger.info(StringConstantUtil.RESPONSE_INFO, status_code, response.get_data())
    elif 400 <= status_code <= 499:
        logger.warn(StringConstantUtil.RESPONSE_INFO, status_code, response.get_data())
    elif 500 <= status_code <= 599:
        logger.error(StringConstantUtil.RESPONSE_INFO, status_code, response.get_data())
    else:
        logger.critical(StringConstantUtil.RESPONSE_INFO, status_code, response.get_data())
    return response


@app.route(StringConstantUtil.SWAGGER_JSON)
def swagger():
    with open(StringConstantUtil.FILE_SWAGGER_JSON, StringConstantUtil.READ_PERM) as file:
        return jsonify(json.load(file))


@app.route(StringConstantUtil.HEALTH)
def health():
    return jsonify({"status": "healthy"})


@app.before_request
def check_file_modification():
    try:
        filename = StringConstantUtil.RESOURCES_KING_FILE
        current_mtime = get_file_mtime(filename)
        cached_mtime = cache.get(f'{filename}_mtime')

        if cached_mtime is None or current_mtime != cached_mtime:
            cache.delete_memoized(load_text_file, filename)
            cache.set(f'{filename}_mtime', current_mtime)
    except Exception as ex:
        logger.error(StringConstantUtil.EXCEPTION_INFO, ex)
        return jsonify({StringConstantUtil.ERROR: StringConstantUtil.CONTACT_ADMIN_MSG}), 500


@app.route(StringConstantUtil.SEARCH, methods=[StringConstantUtil.POST])
def search():
    try:
        if request.data is None or request.data == b'':
            return jsonify({StringConstantUtil.BAD_REQUEST: StringConstantUtil.INVALID_REQ_DATA_MSG}), 400
        data = request.get_json()
        if len(data) > 1:
            return jsonify({StringConstantUtil.BAD_REQUEST: StringConstantUtil.MULTIPLE_KEYS_MSG}), 400
        elif data.get(StringConstantUtil.SEARCH_STR) is None:
            return jsonify({StringConstantUtil.BAD_REQUEST: StringConstantUtil.MISSING_STR_KEY_MSG}), 400
        elif data.get(StringConstantUtil.SEARCH_STR) == '':
            return jsonify({StringConstantUtil.BAD_REQUEST: StringConstantUtil.MISSING_STR_VALUE_MSG}), 400

        # logic to search from the text
        filename = StringConstantUtil.RESOURCES_KING_FILE
        content, mtime = load_text_file(filename)
        search_str = data.get(StringConstantUtil.SEARCH_STR)
        start_indices, end_indices, line_numbers, sentences = find_search_match_locations(content, search_str)
        occurrences = []
        for index in range(len(start_indices)):
            obj = {
                "line": line_numbers[index],
                "start": start_indices[index],
                "end": end_indices[index],
                "in_sentence": sentences[index]
            }
            occurrences.append(obj)

        response_data = {
            "query_text": search_str,
            "number_of_occurrences": len(start_indices),
            "occurences": occurrences
        }
        return jsonify(response_data)
    except UnsupportedMediaType:
        return jsonify({StringConstantUtil.ERROR: StringConstantUtil.UNSUPPORTED_MEDIA_TYPE_MSG}), 415
    except (json.JSONDecodeError, BadRequest):
        return jsonify({StringConstantUtil.BAD_REQUEST: StringConstantUtil.INVALID_JSON_REQ_BODY}), 400
    except Exception as ex:
        logger.error(StringConstantUtil.EXCEPTION_INFO, ex)
        return jsonify({StringConstantUtil.ERROR: StringConstantUtil.CONTACT_ADMIN_MSG}), 500


@cache.memoize()
def find_search_match_locations(text, search_string):
    final_start_indices = []
    final_end_indices = []
    final_line_numbers = []
    actual_start_indices = []
    text_start_length = 0

    # split the lines based on \n
    current_line_number = 1
    lines = text.split(StringConstantUtil.NEW_LINE)
    for line in lines:
        start_indices = search_kmp_algo(line, search_string)
        if len(start_indices) > 0:
            final_start_indices.extend(start_indices)
            end_indices = [start_index + len(search_string) for start_index in start_indices]
            final_end_indices.extend(end_indices)
            final_line_numbers.append(current_line_number)
            actual_start_indices.append(text_start_length)
        current_line_number = current_line_number + 1
        text_start_length = text_start_length + (len(line) - 1)

    # Find the sentences containing the word
    final_matching_sentences = find_sentences(text, search_string)

    return final_start_indices, final_end_indices, final_line_numbers, final_matching_sentences


def find_sentences(text, search_string):
    start_indices = search_kmp_algo(text, search_string)
    end_indices = [start_index + len(search_string) - 1 for start_index in start_indices]

    # Find the sentences containing the word
    sentences = text.split(StringConstantUtil.FULL_STOP)
    matching_sentences = []

    for i in range(len(start_indices)):
        sentence_start = 0
        for sentence in sentences:
            sentence_end = sentence_start + len(sentence) - 1
            if start_indices[i] >= sentence_start and end_indices[i] <= sentence_end:
                matching_sentences.append(sentence.strip() + StringConstantUtil.FULL_STOP)
            sentence_start += len(sentence) + 1

    return matching_sentences


def find_string_in_text(text, search_string):
    # Use the KMP algorithm to find occurrences of search_string in the text
    start_indices = search_kmp_algo(text, search_string)
    end_indices = [start_index + len(search_string) - 1 for start_index in start_indices]

    # Find line numbers for each start index
    lines = text.split(StringConstantUtil.NEW_LINE)
    line_start = 0
    line_numbers = []
    current_line_number = 1

    for start_index in start_indices:
        while start_index >= line_start + len(lines[current_line_number - 1]):
            line_start += len(lines[current_line_number - 1]) + 1
            current_line_number += 1
        line_numbers.append(current_line_number)

    # Find the sentences containing the word
    sentences = text.split(StringConstantUtil.FULL_STOP)
    matching_sentences = []

    for i in range(len(start_indices)):
        sentence_start = 0
        for sentence in sentences:
            sentence_end = sentence_start + len(sentence) - 1
            if start_indices[i] >= sentence_start and end_indices[i] <= sentence_end:
                matching_sentences.append(sentence.strip())
            sentence_start += len(sentence) + 1

    return start_indices, end_indices, line_numbers, matching_sentences


def search_kmp_algo(text, search_str):
    text_len = len(text)
    search_str_len = len(search_str)
    if search_str_len == 0:
        return []

    # Compute the match table for the given search str
    match_table = find_lps_match(search_str)

    # Initialize variables
    matching_indexes = []
    j = 0

    # Loop through the text to find matches
    for i in range(text_len):
        while j > 0 and text[i] != search_str[j]:
            j = match_table[j - 1]
        if text[i] == search_str[j]:
            j += 1
        if j == search_str_len:
            # if a match is found
            matching_indexes.append(i - search_str_len + 2)
            j = match_table[j - 1]
    return matching_indexes


def find_lps_match(pattern):
    # Initialize the partial match table
    match_table = [0] * len(pattern)
    length = 0

    # Loop through the pattern to populate the table
    for i in range(1, len(pattern)):
        while length > 0 and pattern[i] != pattern[length]:
            length = match_table[length - 1]
        if pattern[i] == pattern[length]:
            length += 1
        match_table[i] = length
    return match_table


def get_file_mtime(filename):
    return os.path.getmtime(filename)


@cache.memoize()
def load_text_file(filename):
    file_modified_time = get_file_mtime(filename)
    with open(filename, StringConstantUtil.READ_PERM) as file:
        content = file.read()
    return content, file_modified_time


if __name__ == '__main__':
    app.run()
