# Enigma Python Library Overview

The Enigma Python library is designed to provide a simple and efficient way to encrypt and decrypt data using a custom cipher. It can be used for personal or educational purposes, and it supports both command-line and programmatic usage.

## Features

- Custom cipher encryption and decryption
- File encryption and decryption
- Generate secure encryption keys
- Supports Python 3.12 and higher

## Structure

The library has the following components:

- `cipher.py`: Defines the `Enigma` class which handles encryption and decryption.
- `config.py`: Stores the configurable settings, such as symbols and key lengths.
- `read.py`: Provides methods for file encryption and decryption.
- `utilitis.py`: Contains utility functions for converting between arrays and strings.

## Usage

To get started with the Enigma Python library, you'll need to have Python installed on your system. Then, simply install Enigma using pip:

```python
pip install seal-py
```


### Programmatic Usage

To use the Enigma library programmatically, import the classes and functions as needed. Here's an example:

```python
from seal_py.read import CipherReader

# Initialize CipherReader with the file path
cipher_reader = CipherReader("path/to/your/file.txt")

# Encrypt the file
encryption_key = cipher_reader.cipher_file(rewrite=True, key_lenght=32)

# Decrypt the file
decrypted_text = cipher_reader.anti_cipher_file(encryption_key)
```

Make sure you have the correct imports and paths set up based on your Python project structure.
# pyproject.toml Documentation

This documentation provides usage information and describes methods for the `pyproject.toml` file.

## Usage

The `pyproject.toml` file is used in a Python project to configure and specify various settings. This includes package information, project metadata, dependencies, and build system settings. Here's how you can use the file:

1. **Define project metadata**: Set the name, version, description, authors, and license for your project. This information is used when publishing your package to a package repository, such as PyPI.
2. **Specify package information**: Include the directory containing the package in the `packages` section. In this example, the `seal-py` directory is included.
3. **List dependencies**: Define the required dependencies for your project under the `dependencies` section. In this case, `python` has been specified with a version constraint `^3.12`, indicating that the project is compatible with any Python version 3.12 and higher.
4. **Configure build system**: Specify the required build system and build backend in the `build-system` section. This allows you to use tools like `poetry` to build your project.

## Methods

There are no methods in the `pyproject.toml` file as it is a configuration file, not a code module. However, here's a description of important sections:

- [tool.poetry]: Contains Poetry-specific configuration settings for the project.
- [tool.poetry.name], [tool.poetry.version], [tool.poetry.description], [tool.poetry.authors] and [tool.poetry.license]: Provide information about the project name, version, description, authors, and license.
- [tool.poetry.readme]: Specifies the `README.md` file for the project.
- [tool.poetry.packages]: Defines the package directory to be included in the project.
- [tool.poetry.dependencies]: Specifies the Python dependencies required for the project.
- [build-system]: Configures the build system and build backend for building the project.

Remember, this is an additional documentation for the `pyproject.toml` file and not a full documentation.
# seal-py/cipher.py

This documentation outlines the usage of the `Enigma` class within the `cipher.py` file. This class is meant for encrypting and decrypting text using a generated encryption key.

## Usage

Creating an instance of the `Enigma` class:

```python
enigma = Enigma()
```

### Methods

#### `cipher_text(self, key: str, text: str) -> str`
- **Description**: Encrypts a text string using the provided key. The resulting cipher text is returned.
- **Arguments**:
  - `key` (str): The encryption key.
  - `text` (str): The text to be encrypted.
- **Returns**: Encrypted text (str).

```python
encrypted_text = enigma.cipher_text("34!2ab4", "Hello, World!")
```

#### `anti_cipher_text(self, key:str, text:str)`
- **Description**: Decrypts a cipher text string using the provided key. The resulting decrypted text is returned.
- **Arguments**:
  - `key` (str): The decryption key.
  - `text` (str): The cipher text to be decrypted.
- **Returns**: Decrypted text (str).

```python
decrypted_text = enigma.anti_cipher_text("34!2ab4", "Ifmmp, Xpsme!")
```

#### `generate_key(self, key_length)`
- **Description**: Generates a random encryption key with the specified length. The generated key can be used in the `cipher_text` method.
- **Arguments**:
  - `key_length` (int): Length of the key.
- **Returns**: Generated key (str).

```python
key = enigma.generate_key(8)
ciphered_text = enigma.cipher_text(key, "This is a test.")
```

Feel free to let your creativity shine while using the `Enigma` class in your projects!
# seal-py Configuration

This documentation provides information about the `config.py` file in the seal-py project, specifically focusing on the usage and descriptions of the methods provided in the file.

## SYMBWOL

The `SYMBWOL` list is an array containing uppercase letters of the English alphabet. It is used for defining possible symbols in the Enigma cipher. For example:

```python
SYMBWOL = ['A', 'B', 'C', 'D', 'E',
           'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O',
           'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y',
           'Z']
```

Each element in the list represents a valid symbol for the Enigma cipher. You can modify the symbols included in this list to use a custom set of letters and/or numbers for your purposes.

## Usage

You can use the `SYMBWOL` list to configure the available symbols for the Enigma cipher. It is included in the seal-py project and can be easily imported into your code for quick reference.

```python
import config

# Example of using SYMBWOL
for symbol in config.SYMBWOL:
    print(symbol)
```

This code snippet demonstrates how to iterate through the `SYMBWOL` list, printing each element as it goes. Feel free to modify or extend the list as needed.

## Additional Notes

Remember that the `config.py` file is just a component of the seal-py project and might not contain a full range of documentation. Make sure to refer to other documentation sources or the project's main repository for a more complete understanding of the platform.

Enjoy coding with the seal-py Enigma cipher!
# seal-py/read.py

This module contains classes and methods for reading and encrypting files using the Enigma cipher.

## Usage

1. Import the necessary classes and methods from the `read` module.

```python
from read import CipherReader
```

2. Create an instance of the `CipherReader` class with a file path.

```python
cipher_reader = CipherReader(file_path="path/to/your/file.txt")
```

3. Encrypt a file using a random key or your own key.

```python
# Encrypt with a random key
key = cipher_reader.cipher_file()

# Encrypt with a custom key
custom_key = "your-custom-key"
cipher_reader.cipher_file(key_code=custom_key)
```

4. Decrypt a file using the appropriate key.

```python
# Decrypt using the previously generated key
decrypted_file = cipher_reader.anti_cipher_file(key=key)

# Decrypt using a custom key
cipher_reader.anti_cipher_file(key=custom_key)
```

## Methods

### `__init__(self, file_path: str)`

Initializes the `CipherReader` instance by setting the file path. It reads the file contents for future encryption or decryption.

Parameter: `file_path` - The path to the file being read.

### `cipher_file(self, key_code: str=None, rewrite: bool = False, key_lenght: int = 32) -> str`

Encrypts the file content using the Enigma cipher. It either uses a randomly generated key or a custom key provided by the user.

Parameters:
- `key_code` - The custom key for encryption. If `None` (default), a random key will be generated.
- `rewrite` - If `True`, the encrypted content will overwrite the original file. If `False` (default), a new file will be created.
- `key_length` - The key length for the random key generation (default: 32).

Returns: The key used for encryption.

### `anti_cipher_file(self, key: str)`

Decrypts the file content using the Enigma cipher.

Parameter: `key` - The key used for decryption.

### `__get_path(self, path: str, addon_name, count_endpoints: int = 1) -> str`

Helper method for creating the output file path based on the original file path. It splits the file path, removes the specified number of endpoints, and adds the specified `addon_name` to the file name.

Parameters:
- `path` - The original file path.
- `addon_name` - The name of the addon for the new file.
- `count_endpoints` - Number of endpoints to remove from the original file path (default: 1).
# utils.py

This module provides utility functions to assist with various tasks in the Seal-Py library. The current utility provided is `get_text_from_array`.

## sealpy_utilitis.get_text_from_array

```python
def get_text_from_array(arr: list) -> str
```

- **Description:** This utility function concatenates the characters from a list of characters (a 1-dimensional array) into a single string.
- **Parameters:**
    - `arr` (list): A list containing characters as elements.
- **Returns:**
    - `exit_str` (str): The concatenated string created from the input list of characters.
- **Usage:**
    ```python
    from sealpy.utilitis import get_text_from_array
    
    char_list = ['h', 'e', 'l', 'l', 'o']
    text = get_text_from_array(char_list)
    assert text == 'hello'
    ```
