import os
from itertools import zip_longest

# Provide the base directory path using double backslashes or single forward slash
base_directory_path = "C:\\Users\\david.jolly\\dev\\Compare_SNC_Array_Calibration"

# Specify the file names
file1_name = "file1.cal"
file2_name = "file2.cal"

# Construct the full paths
file1_path = os.path.join(base_directory_path, file1_name)
file2_path = os.path.join(base_directory_path, file2_name)

# Specify the threshold
threshold = 0.5

def is_percentage(value):
    try:
        return 0 <= float(value.rstrip('%')) <= 100
    except ValueError:
        return False

def calculate_percentage_difference(val1, val2):
    num1 = float(val1.rstrip('%'))
    num2 = float(val2.rstrip('%'))

    if num1 == 0 and num2 == 0:
        return 0

    return abs(num1 - num2) / max(num1, num2) * 100

def find_start_line(file_contents):
    start_line = 0
    if 'Calibration Factors\n' in file_contents:
        start_line = file_contents.index('Calibration Factors\n') + 1
    elif 'Calibration Factors AP\n' in file_contents:
        start_line = file_contents.index('Calibration Factors AP\n') + 1
    return start_line

def compare_cal_files(file1_path, file2_path, threshold):
    # Read the contents of the two .cal files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_contents = file1.readlines()
        file2_contents = file2.readlines()

    # Find the starting line number for each file
    start_line_file1 = find_start_line(file1_contents)
    start_line_file2 = find_start_line(file2_contents)

    # Initialize variables to store maximum percentage difference
    max_percentage_diff = 0
    max_percentage_diff_line = 0

    # Iterate through lines starting from the specified line
    for i, (line1, line2) in enumerate(zip_longest(file1_contents[start_line_file1:], file2_contents[start_line_file2:], fillvalue=''), start=start_line_file1):
        # Stop comparison if the line starts with 'Angular dependence'
        if line1.startswith('Angular dependence'):
            break

        parts1 = line1.split('\t')
        parts2 = line2.split('\t')

        # Check if both lines have the same number of fields
        if len(parts1) == len(parts2):
            # Iterate through columns in the lines
            for col1, col2 in zip(parts1, parts2):
                if is_percentage(col1) and is_percentage(col2):
                    # Calculate the percentage difference
                    percentage_diff = calculate_percentage_difference(col1, col2)

                    # Update maximum percentage difference if needed
                    if percentage_diff > max_percentage_diff:
                        max_percentage_diff = percentage_diff
                        max_percentage_diff_line = i

    # Prepare the output message based on whether differences were detected
    if max_percentage_diff > threshold:
        first_value = file1_contents[max_percentage_diff_line].split('\t')[0]
        print(f"Maximum percentage difference of {max_percentage_diff:.2f}% detected at line {max_percentage_diff_line}: Diode Location is {first_value}")
        print("\nPlease consider replacing the existing array calibration.")
    else:
        print(f"Comparison completed, no differences of more than {threshold}% detected.")

# Run the comparison
compare_cal_files(file1_path, file2_path, threshold)
