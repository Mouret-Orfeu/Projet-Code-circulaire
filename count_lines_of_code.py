import os

# Set this to your directory path
directory_path = 'C:\\Users\\mdrou\\OneDrive\\TPS\\3A\\Bioinformatique\\Projet-Code\\src'

# Function to count non-empty lines in a file
def count_non_empty_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file if line.strip())

# Counters for test and non-test files
test_lines = 0
non_test_lines = 0

# Process each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.py'):  # Check if it's a Python file
        file_path = os.path.join(directory_path, filename)
        if filename.startswith('test_'):  # Check if it's a test file
            test_lines += count_non_empty_lines(file_path)
        else:
            non_test_lines += count_non_empty_lines(file_path)

# Print the results
print(f"Total non-empty lines in test files: {test_lines}")
print(f"Total non-empty lines in non-test files: {non_test_lines}")
