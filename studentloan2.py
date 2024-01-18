#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ved Agrawal

DS 2500

9/28

Analyzing number of borrowers who have had their student loans forgiven
and the borrowers outstanding balances
"""

import csv
import re
import matplotlib.pyplot as plt

# Constants

DATA_FILE_BORROWERS = 'pslf_borrowers.csv'
DATA_FILE_BALANCE = 'pslf_balance.csv'

# Function to clean and convert data from strings to floats

def clean_and_convert_data(filename, is_balance_data=False):
    """
    Cleans and converts data in the CSV file to integers or numerical balances.

    Args:
        filename (str): The name of the CSV data file.
        is_balance_data (bool): True if the file contains balance data, False otherwise.

    Returns:
        list: A list of lists representing the cleaned data.
    """
    with open(filename, 'r') as data_file:
        data = list(csv.reader(data_file))

    # Clean and convert data
    
    for row in data:
        for i in range(1, len(row)):
            row[i] = float(re.sub(r'[^\d.]', '', row[i]))

    return data

# Function to add up values in the last column

def sum_last_column(data):
    total = sum(row[-1] for row in data[1:])
    return total

# Function to find the state with the greatest increase and smallest increase

def find_max_min_increase(data):
    max_increase = float('-inf')
    min_increase = float('inf')
    max_increase_state = ""
    min_increase_state = ""

    for row in data[1:]:
        state = row[0]
        may_2022_balance = row[1]
        march_2023_balance = row[-1]
        increase = march_2023_balance - may_2022_balance

        if increase > max_increase:
            max_increase = increase
            max_increase_state = state
        if increase < min_increase:
            min_increase = increase
            min_increase_state = state

    return max_increase_state, max_increase, min_increase_state, min_increase

# Function to calculate average monthly increase for a given state

def calculate_avg_monthly_increase(state_name, data):
    for row in data[1:]:
        if row[0].lower() == state_name.lower():
            may_2022_balance = row[1]
            march_2023_balance = row[-1]
            
            # Number of months from May 2022 to March 2023
           
            num_months = len(row) - 2  
            monthly_increase = (march_2023_balance - may_2022_balance) / num_months
            return monthly_increase
    return None

# Function to create a histogram 

def plot_histogram(data):
    state_names = [row[0] for row in data[1:]]
    average_balances_nov_2022 = [(row[2] + row[3]) / 2 for row in data[1:]]  

  
    average_balances_nov_2022 = [x * 100 for x in average_balances_nov_2022]

    plt.figure(figsize=(12, 6))
    plt.hist(average_balances_nov_2022, bins=7, edgecolor='black')
    plt.xlabel('Average Balance per borrower in dollars')
    plt.ylabel('Number of States')
    plt.title('Distribution of Average Outstanding Balance per Borrower (November 2022)')
    plt.grid(axis='y', alpha=0.75)
        
    plt.savefig('histogram.png')
    plt.show()

# Function to create a line chart 

def plot_line_chart(data, state1, state2):
    state1_data = None
    state2_data = None

    for row in data[1:]:
        if row[0].lower() == state1.lower():
            state1_data = row[1:]
        elif row[0].lower() == state2.lower():
            state2_data = row[1:]

    # Check if both states have data
    
    if state1_data is None or state2_data is None:
        print("One or both states not found in the data.")
        return

    

    months = ['Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 'March 2023']
    
    scaling_factor = 100  
    state1_data = [x * scaling_factor for x in state1_data]
    state2_data = [x * scaling_factor for x in state2_data]

    plt.figure(figsize=(12, 6))
    plt.plot(months, state1_data[:len(months)], marker='o', label=state1)
    plt.plot(months, state2_data[:len(months)], marker='o', label=state2)
    plt.xlabel('Month')
    plt.ylabel('Average balance in dollars  ')
    plt.title('Change in Average Outstanding Balance Over Time')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('line_chart.png')
    
    plt.show()

# Main function to answer the questions and create the plots

def main():
   
    # Clean and convert data from both files
    
    borrowers_data = clean_and_convert_data(DATA_FILE_BORROWERS)
    balance_data = clean_and_convert_data(DATA_FILE_BALANCE)

    # Answer the questions
    
    # 1. How many total borrowers had their PSLF application discharged as of March 2023?
   
    total_borrowers_march_2023 = sum_last_column(borrowers_data)
    print(f"1. Total borrowers in March 2023: {total_borrowers_march_2023:.0f}")

    # 2. What is the total outstanding balance for all students as of March 2023?
    
    total_balance_march_2023 = sum_last_column(balance_data)
   
    # Multiply by 1,000,000 to convert to dollars
  
    total_balance_march_2023 *= 1000000
    print(f"2. Total balance in March 2023: ${total_balance_march_2023:.2f}")

    # 3. What is the average outstanding balance per student as of March 2023?
   
    average_balance_march_2023 = total_balance_march_2023 / total_borrowers_march_2023
    print(f"3. Average balance per student in March 2023: ${average_balance_march_2023:.2f}")

    # 4 & 5. Which state had the greatest and smallest increase in outstanding balance from May 2022 to March 2023?
   
    max_increase_state, max_increase, min_increase_state, min_increase = find_max_min_increase(balance_data)
  
    # Multiply the increase values by 1,000,000 to convert to dollars
  
    max_increase *= 1000000
    min_increase *= 1000000
    print(f"4. State with the greatest increase: {max_increase_state}")
    print(f"5. Increase in balance: ${max_increase:.2f}")
    print(f"6. State with the smallest increase: {min_increase_state}")
    print(f"7. Increase in balance: ${min_increase:.2f}")

    # 8. On average, how much did the outstanding balance in a given state increase per month?
    
    state_name = input("8. Enter a state name to calculate the average monthly increase: ")
    avg_monthly_increase = calculate_avg_monthly_increase(state_name, balance_data)
    if avg_monthly_increase is not None:
        
        # Multiply the monthly increase by 1,000,000 to convert to dollars
        
        avg_monthly_increase *= 100000
        print(f"8. Average monthly increase in {state_name} is: ${avg_monthly_increase:.2f}")
    else:
        print("8. State not found in the data")

    # Create and display the plots
    
    plot_histogram(balance_data)
    state1 = input("Enter the first state for the comparison: ")
    state2 = input("Enter the second state for the comparison: ")
    plot_line_chart(balance_data, state1, state2)

if __name__ == "__main__":
    main()
