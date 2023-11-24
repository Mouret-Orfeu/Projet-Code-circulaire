import os


def delete_empty_and_not_in_use_output_files():
    for file in os.listdir():
        print(file)
        if file.startswith("output-") and file.endswith(".txt"):
            try:
                # Try to open the file in append mode. If it's in use, an exception will be raised.
                with open(file, 'a'):
                    pass
                # Check if the file is empty
                if os.path.getsize(file) == 0:
                    os.remove(file)
            except Exception as e:
                print(f"Could not delete {file}: {e}")
