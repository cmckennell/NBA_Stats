import pandas as pd
import numpy as np
import os
from pathlib import Path

class InitialExploration:
    def __init__(self, dataset_file_path:str):
        reader_dict = {
            "csv":pd.read_csv,
            "xlsx": pd.read_excel
        }
        extension = Path(dataset_file_path).suffix[1:]
        try:
            self.data = reader_dict[extension](dataset_file_path)

        except KeyError:  
            raise KeyError(f"Unknown File Type: .{extension}")
            
        except FileNotFoundError:  
            raise FileExistsError(f"File not found: {dataset_file_path}")  
        except Exception as e:  
            raise Exception(f"Error loading file: {str(e)}")  

    def shape(self):
        df = self.data
        print("\n")
        print("Shape")
        print("============================================================\n")

        print(f"There are {df.shape[1]} columns and {df.shape[0]} rows.")
        print("------------------------------------------------------\n")

        print("First Five Rows:")
        print("------------------------------------------------------")
        print(df.head())
        print("------------------------------------------------------\n")     

    def data_types(self):
        df = self.data
        max_column_length = (max(len(col) for col in df.columns))
        print("Data Types")
        print("============================================================\n")

        for col in df.columns:
            column_adjustment_spacing = " " * (max_column_length - len(col))
            adjusted_column = col + ":" + column_adjustment_spacing
            dtype = df[col].dtype

            print(f"{adjusted_column} {dtype}")


        print("------------------------------------------------------\n")

    def missing_data(self):
        def print_formatted_data(column_name, max_column_length, value):
            column_adjustment_spacing = " " * (max_column_length - len(column_name))
            adjusted_column_name = column_name + ":" + column_adjustment_spacing
            print(f"{adjusted_column_name} {value * 100: .2f}%")

        df = self.data

        print("Missing Data")
        print("============================================================\n")
        total_rows = len(df)
        max_column_length = (max(len(col) for col in df.columns))

        buckets = {
            'none_missing': {},
            'some_missing': {},
            'most_missing': {}
            }

        for col in df.columns:
            value_count = df[col].count()
            percent_present = value_count / total_rows

            if percent_present == 1:
                bucket = 'none_missing'

            elif percent_present == 0:
                bucket = 'most_missing' 

            elif percent_present >= .85:
                bucket = 'some_missing'

            else:
                bucket = 'most_missing'


            buckets[bucket][col] = percent_present
        
        for bucket, column_values in buckets.items():
            if bucket == 'none_missing':
                print("Rows without missing data:")
                print("------------------------------------------------------")
                for column, value in column_values.items():
                    print_formatted_data(column, max_column_length, value)
                print('\n')


            if bucket == 'some_missing':
                print("Rows with some missing data:")
                print("------------------------------------------------------")
                for column, value in column_values.items():
                    print_formatted_data(column, max_column_length, value)
                print('\n')

            if bucket == 'most_missing':
                print("Rows with a lot of missing data:")
                print("------------------------------------------------------")
                for column, value in column_values.items():
                        print_formatted_data(column, max_column_length, value)
                print('\n')        
        print("------------------------------------------------------\n")

    def duplicate_rows(self):
        num_dupes = self.data.duplicated().sum()
        print(f"Duplicate Rows Found: {num_dupes}")
        print("============================================================\n")
        if num_dupes > 0:
            print(self.data[self.data.duplicated(keep=False)])  # Show duplicate rows if they exist
            print("------------------------------------------------------\n")

    def descriptive_statistics(self):

        print(f"Summary Statistics:")
        print("============================================================\n")

        print(f"Quantitative Columns:")
        print("------------------------------------------------------")
        quantitative = self.data.describe()
        print(quantitative)
        print("------------------------------------------------------\n")

        print(f"Qualitative Columns:")
        print("------------------------------------------------------")
        qualitative = self.data.describe(exclude=[np.number])
        print(qualitative)
        print("------------------------------------------------------\n")


        # Value Counts for Columns with less than 25 values
        columns_with_few_unique_values = []
        df_cat = self.data.select_dtypes(include=['object', 'category', 'boolean'])
        for column in df_cat.columns:
            if len(df_cat[column].unique()) <= 25:
                columns_with_few_unique_values.append(column)

        # Only show if there are columns to do this for
        if columns_with_few_unique_values:
            print("Value Counts for Columns with less than 25 unique values:")
            print("------------------------------------------------------\n")
            for column in columns_with_few_unique_values:
                print(df_cat[column].value_counts(normalize=True).mul(100).map(lambda x: f"{x: .2f}%"))
                print("------------------------------------------------------\n")

    def show_report(self):
        self.shape()
        self.data_types()
        self.missing_data()
        self.duplicate_rows()
        self.descriptive_statistics()

if __name__ == "__main__":
    d = InitialExploration(r"data/raw/Player Career Info.csv")
    d.descriptive_statistics()
    # print(len(d.data.pos.unique()))
    