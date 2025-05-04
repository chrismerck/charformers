#!/usr/bin/env python3
import sys
from collections import Counter
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet."""
    with open(file_path, 'rb') as file:
        # Read a sample to detect encoding
        raw_data = file.read(10000)  # Read first 10KB for detection
        result = chardet.detect(raw_data)
    return result

def main():
    # Check if file path is provided
    if len(sys.argv) < 2:
        print("Usage: python data_raw_proc.py <file_path> [encoding]")
        print("If encoding is not specified, it will be auto-detected.")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Check if encoding is explicitly provided
    specified_encoding = None
    if len(sys.argv) > 2:
        specified_encoding = sys.argv[2]
    
    try:
        # First, try to detect the encoding
        if not specified_encoding:
            encoding_info = detect_encoding(file_path)
            encoding = encoding_info['encoding']
            confidence = encoding_info['confidence']
            print(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
        else:
            encoding = specified_encoding
            print(f"Using specified encoding: {encoding}")
        
        # Read the file with the detected or specified encoding
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            content = file.read()
        
        # Build frequency table
        char_counter = Counter(content)
        
        # Sort by frequency (most common first)
        sorted_chars = char_counter.most_common()
        
        # Print the frequency table
        print("Character Frequency Table (sorted by most common):")
        print("Char\tCount\tUnicode")
        for char, count in sorted_chars:
            # Format special characters for readability
            display_char = char
            if char.isspace():
                if char == ' ':
                    display_char = 'SPACE'
                elif char == '\n':
                    display_char = '\\n'
                elif char == '\t':
                    display_char = '\\t'
                elif char == '\r':
                    display_char = '\\r'
            
            # Print character, count, and unicode point
            print(f"{display_char}\t{count}\t{ord(char)}")
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{file_path}' with encoding {encoding}.")
        print("Try specifying a different encoding: python data_raw_proc.py filename.txt encoding")
        print("Common encodings: latin-1, cp1252, iso-8859-1")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
