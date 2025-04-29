import argparse
from .cipher import process_message

def main():
    """Main entry point for the Caesar cipher CLI."""
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a message.")
    parser.add_argument('sentence', type=str, help="The sentence to encrypt or decrypt.")
    parser.add_argument('key', type=int, help="The key for encryption or decryption.")
    parser.add_argument('-e', '--encrypt', action='store_true', help="Encrypt the message.")
    parser.add_argument('-d', '--decrypt', action='store_true', help="Decrypt the message.")

    args = parser.parse_args()

    # Ensure the user provides either -e or -d flag
    if not (args.encrypt or args.decrypt):
        print("You must specify either -e for encryption or -d for decryption.")
        exit()

    # Call the process_message function with the appropriate mode ('encrypt' or 'decrypt')
    if args.encrypt:
        print(process_message(args.sentence, args.key, mode='encrypt'))
    elif args.decrypt:
        print(process_message(args.sentence, args.key, mode='decrypt'))

if __name__ == "__main__":
    main()
