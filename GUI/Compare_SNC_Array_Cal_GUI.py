import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from itertools import zip_longest

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

def compare_cal_files(file1_path, file2_path, threshold, output_text):
    # Read the contents of the two .cal files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_contents = file1.readlines()
        file2_contents = file2.readlines()

    # Find the starting line number for each file
    start_line_file1 = find_start_line(file1_contents)
    start_line_file2 = find_start_line(file2_contents)

    # Extract SNC software version
    version_line1 = file1_contents[2].strip()
    version_line2 = file2_contents[2].strip()

    # Output a warning if version difference is detected
    if version_line1 != version_line2:
        output_text.insert(tk.END, "Differences in SNC software have been detected between the two .cal files, please proceed with caution as unexpected results may arise.\n")

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
        output_text.insert(tk.END, f"Maximum percentage difference of {max_percentage_diff:.2f}% detected at line {max_percentage_diff_line}: Diode Location is {first_value}\n")
        output_text.insert(tk.END, "\nPlease consider replacing the existing array calibration.\n")
    else:
        output_text.insert(tk.END, f"Comparison completed, no differences of more than {threshold}% detected.\n")

def browse_file(var):
    file_path = filedialog.askopenfilename(filetypes=[("CAL Files", "*.cal")])
    var.set(file_path)

def compare_files():
    file1_path = file1_var.get()
    file2_path = file2_var.get()
    threshold = float(threshold_var.get())
    
    # Clear previous output
    output_text.delete(1.0, tk.END)
    
    compare_cal_files(file1_path, file2_path, threshold, output_text)

# GUI setup
app = tk.Tk()
app.title("Compare SNC Calibration Files")

# File 1
file1_label = tk.Label(app, text="Select File 1:")
file1_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

file1_var = tk.StringVar()
file1_entry = tk.Entry(app, textvariable=file1_var, width=50, state="readonly")
file1_entry.grid(row=0, column=1, padx=10, pady=10)

file1_browse_button = tk.Button(app, text="Browse", command=lambda: browse_file(file1_var))
file1_browse_button.grid(row=0, column=2, padx=10, pady=10)

# File 2
file2_label = tk.Label(app, text="Select File 2:")
file2_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

file2_var = tk.StringVar()
file2_entry = tk.Entry(app, textvariable=file2_var, width=50, state="readonly")
file2_entry.grid(row=1, column=1, padx=10, pady=10)

file2_browse_button = tk.Button(app, text="Browse", command=lambda: browse_file(file2_var))
file2_browse_button.grid(row=1, column=2, padx=10, pady=10)

# Threshold
threshold_label = tk.Label(app, text="Threshold (%):")
threshold_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

threshold_var = tk.StringVar(value="0.5")
threshold_entry = tk.Entry(app, textvariable=threshold_var, width=10)
threshold_entry.grid(row=2, column=1, padx=10, pady=10)

# Compare button
compare_button = tk.Button(app, text="Compare Files", command=compare_files)
compare_button.grid(row=3, column=0, columnspan=3, pady=20)

# Output text
output_text = scrolledtext.ScrolledText(app, width=80, height=10, wrap=tk.WORD)
output_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI
app.mainloop()











