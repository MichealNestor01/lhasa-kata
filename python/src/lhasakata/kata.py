import os
import sys
import shutil
import xmltodict

# If no argument is provided, default to './svgs'
base_dir = sys.argv[1] if len(sys.argv) > 1 else './test-data'


# Parse SVG file into a dictionary
def parse_svg_xmltodict(file_path):
    with open(file_path, 'r') as file:
        return xmltodict.parse(file.read())

# checks for any red circles in the svg
def any_red_circles(svg_dict):
    return False;

# Determine the category based on SVG content
def determine_category(file_path):
    # use the following variable if you prefer xmltodict
    svg_dict = parse_svg_xmltodict(file_path)
    if (any_red_circles(svg_dict)):
        return 3;
    print(svg_dict)
    exit(0)
    # use the following variable if you prefer Beautiful Soup
    # TODO add rules here
    return -1


# Copy the SVG file to its respective sub-folder based on its category
def copy_file_to_sub_folder(file, category):
    old_path = os.path.join(base_dir, "input", file)
    new_path = os.path.join(base_dir, "output",  category, file)

    # Create the sub-folder if it doesn't exist
    os.makedirs(os.path.join(base_dir, "output", category), exist_ok=True)

    # Copy the file
    shutil.copy2(old_path, new_path)
    print(f"Copied {file} to {category} folder.")


def process_svg_files():
    for file in os.listdir(os.path.join(base_dir, "input")):
        if file.endswith('.svg'):
            category = determine_category(
                os.path.join(base_dir, "input", file))
            category_str = ""
            # Convert category number to string
            switcher = {
                1: "Cat1",
                2: "Cat2",
                3: "Cat3"
            }
            category_str = switcher.get(category, "Unclassified")
            copy_file_to_sub_folder(file, category_str)


if __name__ == "__main__":
    process_svg_files()
