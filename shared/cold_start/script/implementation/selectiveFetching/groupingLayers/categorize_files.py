import re
from collections import Counter

# log file path
LOG_FILE = "combined_startup_logs.log"

# pattern to match 'open' system calls
OPEN_PATTERN = r'openat\(.*?, "([^"]+)",'

def parse_strace_logs(log_file):
    """
    Parse the strace log file and extract all file paths from 'open' system calls.
    """
    accessed_files = []
    with open(log_file, "r") as file:
        for line in file:
            match = re.search(OPEN_PATTERN, line)
            if match:
                accessed_files.append(match.group(1))
    return accessed_files

def categorize_files(file_paths, threshold=2):
    """
    Categorize files into critical and non-critical based on access frequency.
    """
    file_counts = Counter(file_paths)
    critical_files = {file for file, count in file_counts.items() if count >= threshold}
    non_critical_files = {file for file, count in file_counts.items() if count < threshold}
    return critical_files, non_critical_files

def write_to_file(file_list, output_path):
    """
    Write a list of files to an output file.
    """
    with open(output_path, "w") as file:
        for item in sorted(file_list):
            file.write(f"{item}\n")

if __name__ == "__main__":
    # parse the strace logs
    accessed_files = parse_strace_logs(LOG_FILE)

    # categorize files
    critical_files, non_critical_files = categorize_files(accessed_files)

    # output the results
    write_to_file(critical_files, "critical_files.txt")
    write_to_file(non_critical_files, "non_critical_files.txt")

    print(f"Analysis complete!")
    print(f"Critical files written to: critical_files.txt")
    print(f"Non-critical files written to: non_critical_files.txt")
