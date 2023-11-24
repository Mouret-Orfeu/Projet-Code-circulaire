import os
from datetime import datetime, timedelta


def format_execution_time(execution_time):
    # Convert execution_time to a timedelta object
    execution_duration = timedelta(seconds=execution_time)

    # Format the duration into hours, minutes, seconds, and milliseconds
    formatted_duration = str(execution_duration).split('.')[0]  # This gives hh:mm:ss
    milliseconds = f"{execution_time:.3f}".split('.')[1]  # This gives milliseconds

    # Combine formatted_duration and milliseconds
    formatted_time = f"{formatted_duration}.{milliseconds}"
    return formatted_time

def get_formatted_datetime():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

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
