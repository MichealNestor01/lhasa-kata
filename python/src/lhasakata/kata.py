import math
import os
import sys
import shutil
import xmltodict

SVG_SHAPES = ["rect", "circle", "ellipse", "line", "polyline", "polygon"]
SVG_ELEMENTS = ['circle', 'rect', 'path', 'line', 'polyline', 'polygon', 'ellipse', 'text', 'image', 'g']

# If no argument is provided, default to './svgs'
base_dir = sys.argv[1] if len(sys.argv) > 1 else './test-data'


# Parse SVG file into a dictionary
def parse_svg_xmltodict(file_path):
    with open(file_path, 'r') as file:
        return xmltodict.parse(file.read())



# checks for any colour of a given shape in the svg
def any_colour_of_shape(svg_dict, colour, shape):
    if shape in svg_dict:
        if type(svg_dict[shape]) == list:
            for circle in svg_dict[shape]:
                if circle.get("@fill") == colour:
                    return True
        else:
             if svg_dict[shape].get("@fill") == colour:
                    return True
    return False;

# checks the exist ence, and only existence of given coloured shape
def only_colour_of_shape(svg_dict, colour, shape):
    # check if any shapes not shape are in the svg
    for bad_shape in [x for x in SVG_ELEMENTS if x != shape]:
        if bad_shape in svg_dict:
            return False
    # ensure that the desired shape does exist
    if shape in svg_dict:
        # ensure only the desired colour exists
        if type(svg_dict[shape]) == list:
            for circle in svg_dict[shape]:
                if circle.get("@fill") != colour:
                    return False
        else:
             if svg_dict[shape].get("@fill") != colour:
                    return False
    else:
        return False
    return True

def blue_circles_categorisation(svg_dict):
    # assuming for category 3 all need to be less then 50,
    # category 2 all need to be less then 100 etc...
    flag_larger_than_50 = False;
    flag_larger_than_100 = False;
    radii = []
    if type(svg_dict["circle"]) == list:
        for circle in svg_dict["circle"]:
            radii.append(int(circle["@r"]))
    else:
        radii.append(int(svg_dict["circle"]["@r"]))
    # check the radii size
    for r in radii:
        flag_larger_than_50 = r > 50 or flag_larger_than_50
        flag_larger_than_100 = r > 100 or flag_larger_than_100
    if flag_larger_than_100:
        return 1
    elif flag_larger_than_50:
        return 2
    return 3

def text_containing_message(svg_dict, message):
    if "text" in svg_dict:
        if type(svg_dict["text"]) == list:
            for text in svg_dict["text"]:
                if message in text.get("#text"):
                    return True
        else:
             if message in svg_dict["text"].get("#text"):
                    return True
    return False;

def count_svg_elements(svg_dict):
    count = 0
    for key, value in svg_dict.items():
        if key in svg_dict and key in SVG_ELEMENTS:
            if isinstance(value, list):
                for item in value:
                    if list(item.keys())[0] in SVG_ELEMENTS:
                        count += count_svg_elements(item)
                    else:
                        count += 1;
            elif isinstance(value, dict):
                count += 1 + count_svg_elements(value)
    return count

# compare == -1, all lines less than length
# compare == 0, all lines equal to length
# compare == 1, all lines more than length
def check_line_length(line_dict, args):
    target_length = args.get("target_length")
    compare = args.get("compare")
    x1 = line_dict.get("@x1")
    x2 = line_dict.get("@x2")
    y1 = line_dict.get("@y1")
    y2 = line_dict.get("@y2")
    if x1 is None or x2 is None or y1 is None or y2 is None or target_length is None or compare is None:
        return False # missing/invalid points or args
    # get length:
    try:
        length = math.sqrt(abs(float(x2)-float(x1))**2 + abs(float(y2)-float(y1))**2)
    except TypeError: # ensure points are numbers
        return False
    if compare == -1:
        return length < target_length
    elif compare == 0:
        return length == target_length
    elif compare == 1:
        return length > target_length
    return False # invalid compare value

# compare == -1, all lines less than length
# compare == 0, all lines equal to length
# compare == 1, all lines more than length
def check_rect_area(line_dict, args):
    target_area = args.get("target_area")
    compare = args.get("compare")
    height = line_dict.get("@height")
    width = line_dict.get("@width")
    if height is None or width is None or target_area is None or compare is None:
        return False # missing/invalid points or args
    # get length:
    try:
        area = float(height) * float(width) 
    except TypeError: # ensure points are numbers
        return False
    if compare == -1:
        return area < target_area
    elif compare == 0:
        return area == target_area
    elif compare == 1:
        return area > target_area
    return False # invalid compare value

# compare == -1, all attribute less than val
# compare == 0, all attribute equal to val
# compare == 1, all attribute more than val
def compare_shape_attribute(shape_dict, args):
    target = args.get("target")
    attribute = args.get("attribute")
    compare = args.get("compare")
    if target is None or attribute is None or compare is None:
        return False # missing args
    val = shape_dict.get(attribute)
    if val is None:
        return False # missing matching attribute
    # get convert val to number:
    try:
        val = float(val)
    except TypeError: # ensure points are numbers
        return False
    if compare == -1:
        return val < target
    elif compare == 0:
        return val == target
    elif compare == 1:
        return val > target
    return False # invalid compare value

# requires a shape to exist
# any_satisfy = True: check a shape exists with given attribute
# any_satisfy = False: check all shapes exist with given attribute
def compare_all_shape_with_attribute(svg_dict, shape, attribute_checker, checker_args, any_satisfy=False):
    if shape in svg_dict:
        if type(svg_dict[shape]) == list:
            for item in svg_dict[shape]:
                has_attr = attribute_checker(item, checker_args)
                if any_satisfy:
                    if has_attr:
                        return True
                elif not has_attr:
                    return False   
        else:
            has_attr = attribute_checker(svg_dict[shape], checker_args)
            if any_satisfy:
                if has_attr:
                    return True
            elif not has_attr:
                return False   
    else:
        return False
    return True

# requires a shape to exist
# any_satisfy = True: check any shape exists with given attribute
# any_satisfy = False: check all shapes exist with given attribute
def compare_any_with_attribute(svg_dict, attribute_checker, checker_args):
    for element in SVG_ELEMENTS: 
        if element in svg_dict:
            if type(svg_dict[element]) == list:
                for item in svg_dict[element]:
                    if attribute_checker(item, checker_args):
                        return True
            else:
                if attribute_checker(svg_dict[element], checker_args):
                    return True 
    return False

# Determine the category based on SVG content
def determine_category(file_path):
    # use the following variable if you prefer xmltodict
    raw_dict = parse_svg_xmltodict(file_path)
    svg_dict = raw_dict.get("svg")
    if svg_dict is None:
        return -1
    
    # check any red circles
    if any_colour_of_shape(svg_dict, "red", "circle"):
        return 3;

    # check only blue circles; assuming this means only circles that are blue
    if only_colour_of_shape(svg_dict, "blue", "circle"):
        return blue_circles_categorisation(svg_dict)

    # any squares or rectangles? 
    # not putting generic tests in a funciton to test :P
    if "rect" in svg_dict:
        if "text" in svg_dict:
            # asume wants to know if any text exits that contains lhasa
            if text_containing_message(svg_dict, "lhasa"):
                return 1
            return 3
        return 2
    
    if "text" in svg_dict:
        # check for green rectangle
        if any_colour_of_shape(svg_dict, "green", "rect"):
            return 1

    # check more then one element in the file
    elemet_count = count_svg_elements(svg_dict)
    if elemet_count > 1:
        return 1

    # check for line:
    if "line" in svg_dict:
        if compare_all_shape_with_attribute(svg_dict, "line", check_line_length, {"target_length": 100, "compare": 1}):
            return 2
        return 3
    
    # check for elipse in shape
    if "elipse" in svg_dict:
        # check for any with height greater then 50
        if compare_all_shape_with_attribute(svg_dict, "elipse", compare_shape_attribute, {"target": 49.499, "attribute":"@height", "compare": 1}, any_satisfy=True):
            return 3
        # check any rectangle with area greater then 300
        if "rect" in svg_dict:
            if compare_all_shape_with_attribute(svg_dict, "rect", check_rect_area, {"target_area": 299.499, "compare": 1}, any_satisfy=True):
                return 1
        # check element count
        if elemet_count > 5:
            return 2
        return 3
    
    # check any elements with opacity less than 1
    if not compare_any_with_attribute(svg_dict, compare_shape_attribute, {"target": 1, "attribute":"@opacity", "compare": -1}):
        return 3
    

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


#Unused functions:
# checks for any red circles in the svg
def any_red_circles(svg_dict):
    if "circle" in svg_dict:
        if type(svg_dict['circle']) == list:
            for circle in svg_dict['circle']:
                if circle.get("@fill") == "red":
                    return True
        else:
             if svg_dict['circle'].get("@fill") == "red":
                    return True
    return False;