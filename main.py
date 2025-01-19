import re

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import time


def read_input_file(file_path):

    """Reads the input file and extracts registration numbers."""

    registrations = []

    with open(file_path, 'r') as file:

        for line in file.readlines():

            match = re.search(r'\b[A-Z]{2}[0-9]{2}\s?[A-Z]{3}\b', line)

            if match:

                registrations.append(match.group())

    print("Input File Registration Numbers:")

    print(registrations)

    return registrations





def fetch_data_from_website(registrations, driver):

    """Fetches car details for each registration number from the website."""

    url = "https://motorway.co.uk/"  

    driver.get(url)



    car_details = {}

    for reg_number in registrations:

        try:

            search_input = driver.find_element(By.ID, "vrm-input")  # Replace with the actual ID of the input field

            search_input.clear()

            search_input.send_keys(reg_number, Keys.RETURN)



            time.sleep(5)  # Wait for page to load



            # Fetch car details (adjust selectors based on the site's actual implementation)

            details = driver.find_element(By.CSS_SELECTOR, "div.car-details").text

            car_details[reg_number] = details

        except Exception as e:

            print(f"Error fetching data for {reg_number}: {e}")

            car_details[reg_number] = None

    return car_details





def compare_with_output_file(fetched_data, output_file):

    """Compares the fetched data with the output file."""

    mismatches = []

    with open(output_file, 'r') as file:

        expected_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in file.readlines() if ":" in line}



    for reg, details in fetched_data.items():

        if expected_data.get(reg) != details:

            mismatches.append((reg, expected_data.get(reg), details))



    if mismatches:

        print("\nMismatches found:")

        for reg, expected, actual in mismatches:

            print(f"Reg: {reg}, Expected: {expected}, Actual: {actual}")

        return False

    else:

        print("\nAll data matches the output file.")

        return True





def main():

    input_file = r"C:/Users/Swathi/Desktop/car_input V4.txt"  # Replace with your input file path

    output_file = r"C:/Users/Swathi/Desktop/car_output V4.txt"  # Replace with your output file path



    # Step 1: Read input file to extract registration numbers

    registrations = read_input_file(input_file)



    # Step 2: Setup Selenium WebDriver

    driver = webdriver.Chrome()  



    # Step 3: Fetch data for each registration number

    fetched_data = fetch_data_from_website(registrations, driver)



    # Step 4: Compare fetched data with the output file

    test_passed = compare_with_output_file(fetched_data, output_file)



    # Step 5: Print final test result

    if test_passed:

        print("\nTEST PASSED: All data matches.")

    else:

        print("\nTEST FAILED: There are mismatches.")



    driver.quit()





if __name__ == "__main__":

    main()



