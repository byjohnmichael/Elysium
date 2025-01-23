import json

def save(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
def load(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")