from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, request, jsonify
from flask_caching import Cache
import json
import os

app = Flask(__name__)
# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Chata Search API"
    }
)

# Register Swagger
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


@app.route('/health')
def health():
    return jsonify({"Status": "Healthy"})


@app.before_request
def check_file_modification():
    try:
        filename = 'resources/king-i-150.txt'
        current_mtime = get_file_mtime(filename)
        cached_mtime = cache.get(f'{filename}_mtime')

        if cached_mtime is None or current_mtime != cached_mtime:
            cache.delete_memoized(load_text_file, filename)
            cache.set(f'{filename}_mtime', current_mtime)
    except Exception as ex:
        return jsonify({"Error": "Please contact administrator."}), 500


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        if len(data) > 1:
            return jsonify({"Bad Request": "Request body should contain only 'str' as key."}), 400
        elif data.get('str') is None:
            return jsonify({"Bad Request": "Request body should contain 'str' as key."}), 400
        # verify JSON data body validity
        if data is not None:
            filename = 'resources/king-i-150.txt'
            content, mtime = load_text_file(filename)
            search_str = data.get('str')
            if search_str is not None:
                start_indices, end_indices, line_numbers, sentences = find_search_match_locations(content, search_str)
                occurences = []
                for index in range(len(start_indices)):
                    obj = {
                        "line": line_numbers[index],
                        "start": start_indices[index],
                        "end": end_indices[index],
                        "in_sentence": sentences[index]
                    }
                    occurences.append(obj)

                response_data = {
                    "query_text": search_str,
                    "number_of_occurrences": len(start_indices),
                    "occurences": occurences
                }

                return jsonify(response_data)
            else:
                return jsonify({"Invalid key. Please use 'str' as JSON Key."}), 400
        else:
            return jsonify({"Invalid data. Please use JSON data format."}), 400
    except Exception as ex:
        return jsonify({"Error": "Please contact administrator."}), 500


@cache.memoize()
def find_search_match_locations(text, search_string):
    final_start_indices = []
    final_end_indices = []
    final_line_numbers = []
    actual_start_indices = []
    text_start_length = 0

    # split the lines based on \n
    current_line_number = 1
    lines = text.split('\n')
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
    end_indices = [start_index + len(search_string)-1 for start_index in start_indices]

    # Find the sentences containing the word
    sentences = text.split('.')
    matching_sentences = []

    for i in range(len(start_indices)):
        sentence_start = 0
        for sentence in sentences:
            sentence_end = sentence_start + len(sentence) - 1
            if start_indices[i] >= sentence_start and end_indices[i] <= sentence_end:
                matching_sentences.append(sentence.strip() + '.')
            sentence_start += len(sentence) + 1

    return matching_sentences


def find_string_in_text(text, search_string):
    # Use the KMP algorithm to find occurrences of search_string in the text
    start_indices = search_kmp_algo(text, search_string)
    end_indices = [start_index + len(search_string) - 1 for start_index in start_indices]

    # Find line numbers for each start index
    lines = text.split('\n')
    line_start = 0
    line_numbers = []
    current_line_number = 1

    for start_index in start_indices:
        while start_index >= line_start + len(lines[current_line_number - 1]):
            line_start += len(lines[current_line_number - 1]) + 1
            current_line_number += 1
        line_numbers.append(current_line_number)

    # Find the sentences containing the word
    sentences = text.split('.')
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
    with open(filename, 'r') as file:
        content = file.read()
    return content, file_modified_time


if __name__ == '__main__':
    app.run()
