import pandas as pd

def separate_data_with_missing_values(file_path):
    # Load the dataset
    data = pd.read_csv(file_path, header=None)
    
    # Identify rows with any missing values
    rows_with_missing_values = data.isnull().any(axis=1)
    
    # Separate the data into two DataFrames
    data_without_missing = data[~rows_with_missing_values]
    data_with_missing = data[rows_with_missing_values]
    
    # Define paths for the new CSV files
    data_without_missing_path = 'final_data_without_missing.csv'
    data_with_missing_path = 'final_data_with_missing.csv'
    
    # Save the DataFrames into two new CSV files
    data_without_missing.to_csv(data_without_missing_path, index=False, header=False)
    data_with_missing.to_csv(data_with_missing_path, index=False, header=False)
    
    print(f"Data without missing values saved to: {data_without_missing_path}")
    print(f"Data with missing values saved to: {data_with_missing_path}")

# Example usage
file_path = 'final_data.csv'
separate_data_with_missing_values(file_path)
