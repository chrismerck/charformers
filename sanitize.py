#!/usr/bin/env python3
import sys
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet."""
    with open(file_path, 'rb') as file:
        # Read a sample to detect encoding
        raw_data = file.read(10000)  # Read first 10KB for detection
        result = chardet.detect(raw_data)
    return result

def sanitize(raw_text):
    """
    Sanitize text to only include lowercase a-z, space, period, comma, question mark, apostrophe, and newline.
    
    Specifically:
    - Convert accented characters to the closest English equivalent
    - Convert text to lowercase
    - Convert ! to .
    - Convert quotes to apostrophes
    - Keep newlines
    - Replace other symbols with spaces
    
    Returns sanitized text with only the 32 allowed characters: a-z, space, .,?'\n
    """
    # Convert to lowercase first
    text = raw_text.lower()
    
    # Dictionary for accent mappings
    accent_map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ñ': 'n',
        'ç': 'c'
    }
    
    # Create a character mapping for all transformations
    char_map = {}
    
    # Add accent mappings
    for accented, plain in accent_map.items():
        char_map[accented] = plain
    
    # Convert exclamation marks to periods
    char_map['!'] = '.'
    
    # Convert quotes to apostrophes
    char_map['"'] = "'"
    char_map['`'] = "'"
    char_map['"'] = "'"
    char_map['"'] = "'"
    
    # Define allowed characters
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz .,?\'\n')
    
    # Process text character by character
    result = []
    for char in text:
        # Apply specific mappings
        if char in char_map:
            result.append(char_map[char])
        # Keep allowed characters
        elif char in allowed_chars:
            result.append(char)
        # Replace other characters with space
        elif char != '\n':  # except newlines
            result.append(' ')
        else:
            result.append(char)
    
    return ''.join(result)

def main():
    # Check if file paths are provided
    if len(sys.argv) < 3:
        print("Usage: python sanitize.py <input_file_path> <output_file_path> [encoding]")
        print("If encoding is not specified, it will be auto-detected.")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    # Check if encoding is explicitly provided
    specified_encoding = None
    if len(sys.argv) > 3:
        specified_encoding = sys.argv[3]
    
    try:
        # First, try to detect the encoding
        if not specified_encoding:
            encoding_info = detect_encoding(input_file_path)
            encoding = encoding_info['encoding']
            confidence = encoding_info['confidence']
            print(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
        else:
            encoding = specified_encoding
            print(f"Using specified encoding: {encoding}")
        
        # Read the input file with the detected or specified encoding
        with open(input_file_path, 'r', encoding=encoding, errors='replace') as file:
            content = file.read()
        
        # Sanitize the content
        sanitized_content = sanitize(content)
        
        # Write sanitized content to output file
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(sanitized_content)
        
        print(f"Sanitized text saved to {output_file_path}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{input_file_path}' with encoding {encoding}.")
        print("Try specifying a different encoding: python sanitize.py input.txt output.txt encoding")
        print("Common encodings: latin-1, cp1252, iso-8859-1")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
