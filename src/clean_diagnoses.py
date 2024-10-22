import os

def clean_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Remove the first 10 rows
    cleaned_lines = lines[10:]

    # Remove section from "## Fördjupning" to the next heading
    final_lines = []
    skip_section = False
    for line in cleaned_lines:
        if line.strip().startswith("## Fördjupning"):
            skip_section = True
        elif skip_section and line.strip().startswith(("#", "##", "###", "####")):
            skip_section = False
        elif not skip_section:
            final_lines.append(line)

    # Find the index of "## PM-medlemskap" line
    try:
        pm_index = next(i for i, line in enumerate(final_lines) if line.strip() == "## PM-medlemskap")
        # Keep only the lines before "## PM-medlemskap"
        final_lines = final_lines[:pm_index]
    except StopIteration:
        # If "## PM-medlemskap" is not found, keep all lines
        pass

    # Write the cleaned content to the output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(final_lines)

def main():
    input_dir = "/home/bice/dev/BlackWell-LiA/web_scraping_project/diagnoses"
    output_dir = "/home/bice/dev/BlackWell-LiA/web_scraping_project/cleaned_diagnoses"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all files in the input directory
    for filename in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, filename)):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            clean_file(input_path, output_path)
            print(f"Cleaned {filename}")

if __name__ == "__main__":
    main()
