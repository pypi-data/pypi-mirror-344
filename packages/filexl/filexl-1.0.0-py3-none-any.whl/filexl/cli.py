import argparse
import os
import pandas as pd

def list_files(path, name=None, extensions=None, ignore_case=False):
    records = []

    for root, _, files in os.walk(path):
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            match_ext = file_ext
            if ignore_case:
                match_ext = file_ext.lower()

            if extensions:
                if ignore_case:
                    extensions = [e.lower() for e in extensions]
                if match_ext not in extensions:
                    continue

            records.append({
                "File Name": file_name,
                "Extension": file_ext.lstrip('.'),
                "Path": os.path.join(root, file),
                "Path Name": name or os.path.basename(path)
            })

    return pd.DataFrame(records)

def save_to_excel(df, filename, append=False):
    if append and os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} records to '{filename}'.")

def save_duplicates(df, filename):
    duplicated = df[df.duplicated(['File Name'], keep=False)]
    if not duplicated.empty:
        # Sort to group duplicates together
        duplicated = duplicated.sort_values(by=['File Name', 'Path'])
        duplicated.to_excel(filename, index=False)
        print(f"Saved {len(duplicated)} duplicate records to '{filename}'.")
    else:
        print("No duplicate file names found.")

def extract_duplicates_from_excel(input_file, output_file="duplicates.xlsx"):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return

    df = pd.read_excel(input_file)

    if 'File Name' not in df.columns:
        print("Error: 'File Name' column not found in the Excel file.")
        return

    duplicates = df[df.duplicated(subset='File Name', keep=False)]
    duplicates = duplicates.sort_values(by='File Name')

    if duplicates.empty:
        print("No duplicate file names found.")
    else:
        duplicates.to_excel(output_file, index=False)
        print(f"Duplicate records written to '{output_file}'.")

def main():
    parser = argparse.ArgumentParser(description="List files and export to Excel.")
    parser.add_argument("--path", required=True, help="Path to list files from.")
    parser.add_argument("--name", help="Optional name for the path.")
    parser.add_argument("--filename", help="Excel filename (default: output.xlsx).", default="output.xlsx")
    parser.add_argument("--ext", nargs='+', help="Filter by file extensions, space/comma separated.")
    parser.add_argument(
    "--only-duplicates",
    nargs='?',
    const="duplicates.xlsx",
    metavar="DUP_FILE",
    help="Export only duplicated file names. Optionally provide filename (default: duplicates.xlsx)."
)
    parser.add_argument("--ignore-case", action="store_true", help="Make extension filtering case-insensitive.")
    parser.add_argument('--extract-duplicates-from', help="Excel file to extract duplicates from")
    parser.add_argument('--out', help="Output Excel file for duplicates (default: duplicates.xlsx)")

    args = parser.parse_args()

    extensions = []
    if args.ext:
        for ext in args.ext:
            extensions.extend(ext.split(','))
        extensions = [e if e.startswith('.') else f'.{e}' for e in extensions]
    
    if args.extract_duplicates_from:
        extract_duplicates_from_excel(args.extract_duplicates_from, args.out or "duplicates.xlsx")
        return

    df = list_files(args.path, args.name, extensions or None, args.ignore_case)
    save_to_excel(df, args.filename, append=True)

    if args.only_duplicates:
        save_duplicates(df, args.only_duplicates)

if __name__ == "__main__":
    main()
