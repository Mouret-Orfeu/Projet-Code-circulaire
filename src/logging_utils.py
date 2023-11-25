from datetime import datetime, timedelta


def format_execution_time(execution_time: float) -> str:
    # Convert execution_time to a timedelta object
    execution_duration = timedelta(seconds=execution_time)

    # Format the duration into hours, minutes, seconds, and milliseconds
    formatted_duration = str(execution_duration).split('.')[0]  # This gives hh:mm:ss
    milliseconds = f"{execution_time:.3f}".split('.')[1]  # This gives milliseconds

    # Combine formatted_duration and milliseconds
    formatted_time = f"{formatted_duration}.{milliseconds}"
    return formatted_time

def get_formatted_datetime() -> str:
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def log_message(file_name: str, message: str, flush: bool=False) -> None:
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(message)
        if flush:
            file.flush()

def log_summary(file_name: str, n: int, count: int, start_time: float, end_time: float, full_logging: bool) -> None:
    execution_time = end_time - start_time
    formatted_time = format_execution_time(execution_time)
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"Nombre de codes de taille {n}: {count}\n")
        file.write(f"Temps d'exécution: {formatted_time}\n")
        file.write("\n")
    print(f"Nombre de codes de taille {n}: {count}")
    print(f"Temps d'exécution: {formatted_time}")
    print()
