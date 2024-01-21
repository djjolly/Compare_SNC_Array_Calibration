# SNC Calibration File Comparator

This Python script allows you to compare calibration files from Sun Nuclear Corporation (SNC) for SRS MapCHECK or other devices. The comparison is based on percentage differences between corresponding numeric values in the files.

## Prerequisites

Before running the script, ensure you have:

- Python installed on your system.
- Two SNC calibration files (`file1.cal` and `file2.cal`) to compare.

## Usage

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/djjolly/Compare_SNC_Array_Calibration.git
    ```

2. Navigate to the project directory:

    ```bash
    cd compare-snc-calibration
    ```

3. Edit the script (`compare_snc_cal.py`) and provide the correct paths for `base_directory_path`, `file1_name`, `file2_name`, and adjust the `percentage_threshold` if needed.

4. Run the script:

    ```bash
    python compare_snc_cal.py
    ```

5. Review the script output, which will indicate if there are differences above the specified threshold.

## Customization

- You can modify the `percentage_threshold` variable to set the desired percentage difference threshold.
- Adjust the file paths (`base_directory_path`, `file1_name`, `file2_name`) according to your file locations.

Feel free to customize the script to fit your specific use case or integrate it into your workflow.

