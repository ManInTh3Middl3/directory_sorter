import csv
import datetime
import os
from collections import defaultdict

# Get the directory path from the user
dir_path = input("Enter the directory path: ")

# Scan the directory for files
files = os.listdir(dir_path)

# Get the file type for each file
file_types = defaultdict(int)
for file in files:
    file_type = os.path.splitext(file)[1][1:].upper()  # Get the file extension and convert to uppercase
    file_types[file_type] += 1

# Print the file types and the number of corresponding files
print("Here is the breakdown of file types and their counts:")
for file_type, count in file_types.items():
    print(f"{file_type}: {count}")

# Ask the user if they would like to sort the files
sort_choice = input("Would you like to sort the files? (y/n): ")

if sort_choice.lower() == "y":
    # Provide a list of sorting options
    print("Please choose a sorting option:")
    print("1. Sort by file type")
    print("2. Sort by file size")
    print("3. Sort by date created")
    print("4. Sort by file name")
    print("5. Sort by last modified date")
    
    # Get the user's selected sorting option
    sort_option = int(input("Choose Your Sorting Option: "))
    
    try:
        # Sort the files based on the user's selected sorting option and move them to subfolders
        if sort_option == 1:
            # Sort by file type and move to subfolders
            for file_type in file_types:
                type_folder = os.path.join(dir_path, file_type)
                if not os.path.exists(type_folder):
                    os.mkdir(type_folder)
                for file in files:
                    if os.path.splitext(file)[1][1:].upper() == file_type:
                        os.rename(os.path.join(dir_path, file), os.path.join(type_folder, file))
        elif sort_option == 2:
            # Sort by file size and move to subfolders
            sorted_files = sorted(files, key=lambda file: os.path.getsize(os.path.join(dir_path, file)))
            for file in sorted_files:
                file_size = os.path.getsize(os.path.join(dir_path, file))
                size_folder = os.path.join(dir_path, f"{file_size} bytes")
                if not os.path.exists(size_folder):
                    os.mkdir(size_folder)
                os.rename(os.path.join(dir_path, file), os.path.join(size_folder, file))
        elif sort_option == 3:
            # Sort by date created and move to subfolders
            sorted_files = sorted(files, key=lambda file: os.path.getctime(os.path.join(dir_path, file)))
            for file in sorted_files:
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(dir_path, file)))
                date_folder = os.path.join(dir_path, creation_time.strftime("%Y-%m-%d"))
                if not os.path.exists(date_folder):
                    os.mkdir(date_folder)
                os.rename(os.path.join(dir_path, file), os.path.join(date_folder, file))
        elif sort_option == 4:
            # Sort by file name and move to subfolders
            sorted_files = sorted(files)
            for file in sorted_files:
                file_name, file_ext = os.path.splitext(file)
                folder_name = os.path.join(dir_path, file_name)
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                os.rename(os.path.join(dir_path, file), os.path.join(folder_name, file))

        elif sort_option == 5:
            # Sort by last modified date and move to subfolders
            sorted_files = sorted(files, key=os.path.getmtime)
            for file in sorted_files:
                file_name, file_ext = os.path.splitext(file)
                folder_name = os.path.join(dir_path, f"{datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(dir_path, file))).strftime('%Y-%m-%d')}")
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                os.rename(os.path.join(dir_path, file), os.path.join(folder_name, file))

        else:
            print("Invalid sorting option selected.")
            sorted_files = files

        # Output a CSV file containing the sorted file names and their file types
        csv_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), datetime.datetime.now().strftime("%Y-%m-%d") + ".csv")
        with open(csv_filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["File Name", "File Type"])
            for file in sorted_files:
                writer.writerow([file, os.path.splitext(file)[1][1:].upper()])

    except Exception as e:
        print(f"An error occurred: {e}")
else:
    # Print the unsorted files
    for file in files:
        print(file)