import binascii


def file_to_hex(file_path):
    with open(file_path, "rb") as file:
        binary_data = file.read()
        hex_data = binascii.hexlify(binary_data).decode("utf-8")
    return hex_data


def hex_to_file(hex_data, file_path):
    binary_data = binascii.unhexlify(hex_data)
    with open(file_path, "wb") as file:
        file.write(binary_data)


def convert_binary_to_hex(input_binary_location, output_hex_location):
    """
    Read binary from file and convert to hex
    """
    hex_data = file_to_hex(input_file)
    with open("input.hex", "w") as f:
        f.write(hex_data)


def convert_hex_to_binary(input_hex_location, output_binary_location):
    """
    Read hex from file and convert to binary
    """
    raw_hex_data = ""
    with open(input_hex_location, "r") as f:
        raw_hex_data = f.read()

    # write binary to file
    hex_to_file(raw_hex_data, output_binary_location)


# Example usage
input_file = "input.mp4"
hex_file = "hex_file.txt"
# Convert file to hex

convert_hex_to_binary("./input.hex", "./output.mp4")
