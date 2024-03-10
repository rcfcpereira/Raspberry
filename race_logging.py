# race_logging.py

import os
import csv

def initialize_race_log(filename):
    """
    Initialize a new race log file with headers.

    Args:
        filename (str): The name of the CSV file to initialize.

    Returns:
        None
    """
    headers = ["Race Number", "Left Racer Time (s)", "Right Racer Time (s)", "Left Racer Status", "Right Racer Status"]
    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def append_race_log(filename, race_number, left_time, right_time, left_status, right_status):
    """
    Append a new race log entry to the CSV file.

    Args:
        filename (str): The name of the CSV file to append to.
        race_number (int): The race number.
        left_time (float): The time taken by the left racer.
        right_time (float): The time taken by the right racer.
        left_status (str): The status of the left racer.
        right_status (str): The status of the right racer.

    Returns:
        None
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([race_number, left_time, right_time, left_status, right_status])

def get_last_race_number(filename):
    """
    Get the last race number from the CSV file.

    Args:
        filename (str): The name of the CSV file to read from.

    Returns:
        int: The last race number found in the file, or 0 if no race numbers are found.
    """
    last_race_number = 0
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].isdigit():
                    last_race_number = max(last_race_number, int(row[0]))
    return last_race_number

def get_next_race_number(filename):
    """
    Get the next race number by incrementing the last race number.

    Args:
        filename (str): The name of the CSV file to read from.

    Returns:
        int: The next race number.
    """
    last_race_number = get_last_race_number(filename)
    return last_race_number + 1
