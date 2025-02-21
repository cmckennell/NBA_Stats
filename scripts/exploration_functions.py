import pandas as pd
import numpy as np
import os

class Initial_Exploration:
    def __init__(self, dataset_file_path:str):
        reader_dict = {
            "csv":pd.read_csv,
            "xlsx": pd.read_excel
        }
        extension = dataset_file_path.split(".")[-1]

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
        print(f"There are {df.shape[1]} columns and {df.shape[0]} rows.")
        print("------------------------------------------------------\n")

        print("First Five Rows:")
        print("------------------------------------------------------")
        print(df.head())
        print("------------------------------------------------------\n")     

    def data_types(self):
        df = self.data
        max_column_length = (max(len(col) for col in df.columns))
        print("------------------------------------------------------")

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
            elif percent_present >= .85:
                bucket = 'some_missing'
            else:
                bucket = 'most_missing'


            buckets[bucket][col] = percent_present
        
        print("\n")
        
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

if __name__ == "__main__":
    d = Initial_Exploration(r"C:\Users\Zcwmyxv\Downloads\NBA_Stats\data\raw\Player Season Info.csv")
    d.missing_data()