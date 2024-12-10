import numpy as np
import matplotlib.pyplot as plt

# Import src
from nistrng import *


def read_hex_strings_from_file(file_path):
    hex_strings = []
    # Open the file and read each line
    with open(file_path, 'r') as file:
        # Read each line from the file
        for line in file:
            # Split the line by spaces to get multiple hexadecimal strings
            hex_strings.extend(line.strip().split())  # Add all hex strings in the line to the list
    return hex_strings


def write_test_summary_to_file(test_results, output_file):
    with open(output_file, 'w') as f:
        for name, data in test_results.items():
            pass_fail_status = f"Passes: {data['pass']}, Fails: {data['fail']}"
            avg_entropy = np.mean(data['entropy_scores'])
            f.write(f"Test: {name}\n")
            f.write(f"{pass_fail_status}\n")
            f.write(f"Average Entropy Score: {avg_entropy:.4f}\n\n")
        f.write("Summary: End of tests.\n")


if __name__ == "__main__":
    # Step 1: Read the hexadecimal strings from the file
    file_path = 'image_hex_hashes.txt'  # Make sure this file exists and contains hex strings
    hex_strings = read_hex_strings_from_file(file_path)

    # Dictionary to hold the aggregated results by test name
    test_results = {}

    # Step 2: Process each hexadecimal string
    for hex_string in hex_strings:
        # Convert the hex string to bytes
        byte_data = bytes.fromhex(hex_string)

        # Convert the byte data to a list of bits
        bit_data = [bit for byte in byte_data for bit in format(byte, '08b')]

        # Convert the bit list into a numpy array (this is the format needed for the NIST test)
        binary_sequence = np.array([int(bit) for bit in bit_data])

        # Unpack the sequence to check the correctness of the packing process
        unpack_sequence(binary_sequence)

        # Check the eligibility of the test and generate an eligible battery from the default NIST-sp800-22r1a battery
        eligible_battery: dict = check_eligibility_all_battery(binary_sequence, SP800_22R1A_BATTERY)

        # Test the sequence on the eligible tests
        results = run_all_battery(binary_sequence, eligible_battery, False)

        # Store the results for each test
        for result, elapsed_time in results:
            if result.name not in test_results:
                test_results[result.name] = {'pass': 0, 'fail': 0, 'entropy_scores': []}

            # Increment pass/fail count
            if result.passed:
                test_results[result.name]['pass'] += 1
            else:
                test_results[result.name]['fail'] += 1

            # Add the entropy score to the list
            test_results[result.name]['entropy_scores'].append(result.score)

    # 1. Pass/Fail Graph (Pass/Fail per Test)
    unique_tests = list(test_results.keys())  # Use the keys (test names) from test_results
    pass_counts = [test_results[test]['pass'] for test in unique_tests]  # Count passes for each test
    fail_counts = [test_results[test]['fail'] for test in unique_tests]  # Count fails for each test

    # Set up bar chart for Pass/Fail
    plt.figure(figsize=(16, 8))  # Adjust size to handle many test names
    width = 0.35  # Bar width for grouped bars

    # Create bars for Passes and Fails
    plt.bar(unique_tests, pass_counts, width, label='Passes', color='green')
    plt.bar(unique_tests, fail_counts, width, bottom=pass_counts, label='Fails', color='red')

    plt.xlabel('Test Names', fontsize=10)
    plt.ylabel('Count', fontsize=10)
    plt.title('Pass/Fail Results per Test', fontsize=14)
    plt.xticks(rotation=90, fontsize=8)  # Rotate labels to avoid overlap
    plt.legend()
    plt.tight_layout()

    # Save the pass/fail graph as a PNG
    plt.savefig('pass_fail_per_test.png', format='png')
    plt.close()

    # 2. Average Entropy Graph (Entropy per Test)
    # Calculate the average entropy for each test (average score from all runs)
    average_entropy_per_test = [
        np.mean(test_results[test]['entropy_scores']) for test in unique_tests
    ]

    plt.figure(figsize=(16, 8))  # Adjust size to handle many test names
    plt.bar(unique_tests, average_entropy_per_test, color='blue')

    plt.xlabel('Test Names', fontsize=10)
    plt.ylabel('Average Entropy / Score', fontsize=10)
    plt.title('Average Entropy per Test (Between 0 and 1)', fontsize=14)
    plt.xticks(rotation=90, fontsize=8)  # Rotate labels to avoid overlap
    plt.ylim(0, 1)  # Ensure entropy is scaled between 0 and 1
    plt.tight_layout()

    # Save the average entropy graph as a PNG
    plt.savefig('average_entropy_per_test.png', format='png')
    plt.close()

    # 3. Write test summary to a text file
    write_test_summary_to_file(test_results, 'test_summary.txt')
