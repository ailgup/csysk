import os
import json

def create_meta(directory_path = "transcripts", output_file="metadata.json"):
    # Initialize an empty dictionary to store metadata from JSON files
    metadata = {}

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                print("Processing:", filename)
                # Load JSON data from the file
                json_data = json.load(file)
                #print(json_data["result"])
                # Extract key information and append to metadata dictionary
                metadata[filename] = {
                    "result": json_data["result"]["metadata"],
                    # Add more keys as needed
                }

    # Write metadata to the output file
    with open(output_file, 'w') as output:
        json.dump(metadata, output, indent=4)

# Example usage:
create_meta()
