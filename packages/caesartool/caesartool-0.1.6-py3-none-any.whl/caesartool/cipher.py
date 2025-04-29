def process_message(sentence, key, mode='encrypt'):
    """Encrypt or decrypt a message based on the mode."""
    if not isinstance(key, int):
        print("Invalid key. Terminating.")
        exit()

    result = ""

    for ch in sentence:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = key if mode == 'encrypt' else -key
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch  # <--- Just keep spaces and punctuation as-is
    return result
