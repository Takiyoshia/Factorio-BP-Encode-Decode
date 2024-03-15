import os
import zlib
import base64
import json

# Functions for blueprint processing

def blueprint_string_check(s):
    return s.startswith("0")

def blueprint_check(b):
    return isinstance(b, dict)

def add_preamble(s):
    return "0" + s

def strip_preamble(s):
    return s[1:]

def json_encode(b):
    return json.dumps(b)

def json_decode(s):
    return json.loads(s)

def b64_encode(s):
    return base64.b64encode(s).decode('utf-8')

def b64_decode(s):
    return base64.b64decode(s)

def zlib_deflate(s):
    return zlib.compress(s.encode())

def zlib_inflate(s):
    return zlib.decompress(s).decode()

def decode_blueprint(blueprint_string):
    if not blueprint_string_check(blueprint_string):
        raise ValueError("Invalid blueprint string format")
    
    stripped = strip_preamble(blueprint_string)
    decoded = b64_decode(stripped)
    inflated = zlib_inflate(decoded)
    decoded_json = json_decode(inflated)
    return decoded_json

def encode_blueprint(blueprint):
    if not blueprint_check(blueprint):
        raise ValueError("Invalid blueprint format")
    
    encoded_json = json_encode(blueprint)
    deflated = zlib_deflate(encoded_json)
    b64_encoded = b64_encode(deflated)
    with_preamble = add_preamble(b64_encoded)
    return with_preamble

def get_input_source():
    while True:
        choice = input("Would you like to decode blueprint strings or encode JSON files? (Enter 'decode' or 'encode'): ").strip().lower()
        if choice in ['decode', 'encode']:
            return choice
        else:
            print("Invalid input. Please enter 'decode' or 'encode'.")

def get_blueprint_string_or_json(choice, file_path):
    if choice == 'str':
        try:
            with open(file_path, 'r') as file:
                blueprint_string = file.read()
        except FileNotFoundError:
            blueprint_string = input("Please enter the blueprint string: ")
        return decode_blueprint(blueprint_string)
    else:  # choice == 'json'
        try:
            with open(file_path, 'r') as file:
                blueprint_json = json.load(file)
            return blueprint_json
        except FileNotFoundError:
            print("Blueprint file not found.")
            exit()

def get_output_filename(base_filename):
    base_name, extension = os.path.splitext(base_filename)
    index = 1
    while os.path.exists(base_filename):
        base_filename = f"{base_name}{index}{extension}"
        index += 1
    return base_filename

def process_files_in_directory(input_directory, output_directory, process_function):
    files = os.listdir(input_directory)
    for file_name in files:
        input_path = os.path.join(input_directory, file_name)
        if os.path.isfile(input_path):
            try:
                with open(input_path, 'r') as file:
                    input_data = file.read()
                if process_function == encode_blueprint:
                    input_data = json.loads(input_data)  # Parse JSON before encoding
                output_data = process_function(input_data)

                base_name, _ = os.path.splitext(file_name)
                output_filename = get_output_filename(os.path.join(output_directory, f'{base_name}.json' if choice == 'decode' else f'{base_name}.txt'))

                with open(output_filename, 'w') as output_file:
                    if choice == 'decode':
                        json.dump(output_data, output_file, indent=4)
                    else:
                        output_file.write(output_data)
            except Exception as e:
                print(f"Error processing file {input_path}: {e}")

# Main part of the script

choice = get_input_source()

if choice == 'decode':
    input_directory_path = r"BPString"
    output_directory_path = r"Decoded"
    process_function = decode_blueprint
else:  # choice == 'encode'
    input_directory_path = r"BPJson"
    output_directory_path = r"Encoded"
    process_function = encode_blueprint

process_files_in_directory(input_directory_path, output_directory_path, process_function)

print("Processing completed.")