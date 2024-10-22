import os
import shutil

def process_files(input_directory, output_directory, max_rows=7):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        input_path = os.path.join(input_directory, filename)
        if os.path.isfile(input_path):
            with open(input_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) <= max_rows:
                    os.remove(input_path)
                    print(f"Removed {filename} (rows: {len(lines)})")
                else:
                    output_path = os.path.join(output_directory, filename)
                    shutil.copy2(input_path, output_path)
                    print(f"Copied {filename} to new folder (rows: {len(lines)})")

def main():
    input_directory = "/home/bice/dev/BlackWell-LiA/web_scraping_project/cleaned_diagnoses"
    output_directory = "/home/bice/dev/BlackWell-LiA/web_scraping_project/filtered_diagnoses"
    process_files(input_directory, output_directory)

if __name__ == "__main__":
    main()