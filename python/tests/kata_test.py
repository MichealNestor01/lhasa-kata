import unittest
from src.lhasakata.kata import any_red_circles, count_svg_elements, any_colour_of_shape, only_colour_of_shape, blue_circles_categorisation, text_containing_message, compare_all_shape_with_attribute, check_line_length, compare_shape_attribute

# fake functions used for testing
def return_true(*args):
    return True

def return_false(*args):
    return False

def echo_first(val, *args):
    return val


class TestAnyRedCircles(unittest.TestCase):
    def test_no_circles(self):
        svg_dict = {}
        self.assertFalse(any_red_circles(svg_dict))

    def test_one_blue_circle(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertFalse(any_red_circles(svg_dict))

    def test_no_red_circles(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'green'}]}
        self.assertFalse(any_red_circles(svg_dict))

    def test_red_circles_present(self):
        svg_dict = {"circle": {'@fill': 'red'}}
        self.assertTrue(any_red_circles(svg_dict))

class TestAnyColourOfShape(unittest.TestCase):
    def test_no_shape(self):
        svg_dict = {}
        self.assertFalse(any_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_shape_unmatch_colour(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertFalse(any_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_colour_unmatch_shape(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertFalse(any_colour_of_shape(svg_dict, "blue", "rect"))

    def test_match_shape_unmatch_many_colour(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'green'}]}
        self.assertFalse(any_colour_of_shape(svg_dict, "black", "circle"))

    def test_match_colour_and_shape(self):
        svg_dict = {"circle": {'@fill': 'red'}}
        self.assertTrue(any_colour_of_shape(svg_dict, "red", "circle"))
    
    def test_match_shape_and_a_colour(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'red'}]}
        self.assertTrue(any_colour_of_shape(svg_dict, "red", "circle"))


class TestOnlyColourOfShape(unittest.TestCase):
    def test_no_shape(self):
        svg_dict = {}
        self.assertFalse(only_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_shape_unmatch_colour(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertFalse(only_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_colour_unmatch_shape(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertFalse(only_colour_of_shape(svg_dict, "blue", "rect"))

    def test_match_shape_unmatch_many_colour(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'green'}]}
        self.assertFalse(only_colour_of_shape(svg_dict, "black", "circle"))
    
    def test_match_shape_and_a_colour(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'red'}]}
        self.assertFalse(only_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_a_shape_and_all_colour(self):
        svg_dict = {
            "circle": [{'@fill': 'red'}, {'@fill': 'red'}],
            "rect": [{'@fill': 'red'}, {'@fill': 'red'}]
        }
        self.assertFalse(only_colour_of_shape(svg_dict, "red", "circle"))
    
    def test_match_shape_and_all_colour(self):
        svg_dict = {"circle": [{'@fill': 'red'}, {'@fill': 'red'}]}
        self.assertTrue(only_colour_of_shape(svg_dict, "red", "circle"))

    def test_match_colour_and_shape(self):
        svg_dict = {"rect": {'@fill': 'red'}}
        self.assertTrue(only_colour_of_shape(svg_dict, "red", "rect"))

class TestBlueCirclesCategorisation(unittest.TestCase):
    # not writing tests for scenarios that are not possible
    # eg this being called when there are not only blue
    # circles.
    def test_all_less_than_50(self):
        svg_dict = {"circle": [{'@r': '10'}, {'@r': '20'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 3)

    def test_a_less_than_50(self):
        svg_dict = {"circle": [{'@r': '49'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 3)
    
    def test_all_less_than_100_some_less_than_50(self):
        svg_dict = {"circle": [{'@r': '10'}, {'@r': '20'}, {'@r': '51'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 2)
    
    def test_all_less_than_100_greater_than_50(self):
        svg_dict = {"circle": [{'@r': '56'}, {'@r': '99'}, {'@r': '51'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 2)
    
    def test_all_greater_than_100(self):
        svg_dict = {"circle": [{'@r': '102'}, {'@r': '202'}, {'@r': '531'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 1)

    def test_some_greater_than_100(self):
        svg_dict = {"circle": [{'@r': '102'}, {'@r': '20'}, {'@r': '531'}]}
        self.assertEqual(blue_circles_categorisation(svg_dict), 1)

class TestTextContainingMessage(unittest.TestCase):
    def test_no_text(self):
        svg_dict = {}
        self.assertFalse(text_containing_message(svg_dict, "hello world"))

    def test_a_text_no_match(self):
        svg_dict = {"text": {'#text': 'b'}}
        self.assertFalse(text_containing_message(svg_dict, "a"))

    def test_some_text_no_match(self):
        svg_dict = {"text": [{'#text': 'b'}, {'#text': 'c'}]}
        self.assertFalse(text_containing_message(svg_dict, "a"))

    def test_a_text_full_match(self):
        svg_dict = {"text": {'#text': 'a'}}
        self.assertTrue(text_containing_message(svg_dict, "a"))
    
    def test_a_text_partial_match(self):
        svg_dict = {"text": {'#text': 'ab'}}
        self.assertTrue(text_containing_message(svg_dict, "a"))

    def test_some_text_partial_match(self):
        svg_dict = {"text": [{'#text': 'c'}, {'#text': 'ab'}]}
        self.assertTrue(text_containing_message(svg_dict, "a"))

class TestCountSVGElements(unittest.TestCase):
    def test_no_elements(self):
        svg_dict = {}
        self.assertEqual(count_svg_elements(svg_dict), 0)

    def test_1_element(self):
        svg_dict = {"circle": {'@fill': 'blue'}}
        self.assertEqual(count_svg_elements(svg_dict), 1)
    
    def test_2_elements_same_shape(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'blue'}]}
        self.assertEqual(count_svg_elements(svg_dict), 2)
    
    def test_2_elements_different_shape(self):
        svg_dict = {"circle": {'@fill': 'blue'}, "rect": {'@fill': 'red'}}
        self.assertEqual(count_svg_elements(svg_dict), 2)
    
    def test_2_elements_1_nested(self):
        svg_dict = {"circle": {'@fill': 'blue', "rect": {"@fill": "blue"}}}
        self.assertEqual(count_svg_elements(svg_dict), 2)

    def test_3_elements_same_shape(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'blue'}, {'@fill': 'red'}]}
        self.assertEqual(count_svg_elements(svg_dict), 3)
    
    def test_3_elements_1_nested_shape(self):
        svg_dict = {"circle": [{'@fill': 'blue'}, {'@fill': 'blue'}, {'circle': {"@fill": "green"}}]}
        self.assertEqual(count_svg_elements(svg_dict), 3)

class TestCompareAllShapesWithAttribute(unittest.TestCase):
    def test_no_shapes(self):
        svg_dict = {}
        self.assertFalse(compare_all_shape_with_attribute(svg_dict, "rect", return_true, None))

    def test_no_matching_shapes(self):
        svg_dict = {"line": {}}
        self.assertFalse(compare_all_shape_with_attribute(svg_dict, "rect", return_true, None))

    def test_a_matching_shape_comp_fail(self):
        svg_dict = {"line": {}}
        self.assertFalse(compare_all_shape_with_attribute(svg_dict, "line", return_false, None))

    def test_a_matching_shape_comp_pass(self):
        svg_dict = {"line": {}}
        self.assertTrue(compare_all_shape_with_attribute(svg_dict, "line", return_true, None))

    def test_matching_shapes_some_comp_fail(self):
        svg_dict = {"line": [True, False]}
        self.assertFalse(compare_all_shape_with_attribute(svg_dict, "line", echo_first, None))

    def test_matching_shapes_all_comp_pass(self):
        svg_dict = {"line": [True, True]}
        self.assertTrue(compare_all_shape_with_attribute(svg_dict, "line", echo_first, None))

    def test_matching_shapes_some_comp_fail(self):
        svg_dict = {"line": [True, False]}
        self.assertFalse(compare_all_shape_with_attribute(svg_dict, "line", echo_first, None))

    def test_matching_shapes_all_comp_pass(self):
        svg_dict = {"line": [True, False], "rect": [True, True]}
        self.assertTrue(compare_all_shape_with_attribute(svg_dict, "rect", echo_first, None))

class TestCheckLineLength(unittest.TestCase):
    length_5 = {"@x1": "0", "@y1": "0", "@x2": "5", "@y2": "0"};

    def test_less_with_less(self):
        self.assertTrue(check_line_length(self.length_5, {"target_length":6, "compare":-1}))
    
    def test_less_with_equal(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":5, "compare":-1}))

    def test_less_with_more(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":4, "compare":-1}))
    
    def test_equal_with_less(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":6, "compare":0}))
    
    def test_equal_with_equal(self):
        self.assertTrue(check_line_length(self.length_5, {"target_length":5, "compare":0}))

    def test_equal_with_more(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":4, "compare":0}))

    def test_more_with_less(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":6, "compare":1}))
    
    def test_more_with_equal(self):
        self.assertFalse(check_line_length(self.length_5, {"target_length":5, "compare":1}))

    def test_more_with_more(self):
        self.assertTrue(check_line_length(self.length_5, {"target_length":4, "compare":1}))

    def test_diagonal(self):
        length_5_dagonal = {"@x1": "0", "@y1": "4", "@x2": "3", "@y2": "0"};
        self.assertTrue(check_line_length(length_5_dagonal, {"target_length":5, "compare":0}))

    def test_negative_point(self):
        length_5_dagonal_cross_axis = {"@x1": "-4", "@y1": "2", "@x2": "-7", "@y2": "-2"};
        self.assertTrue(check_line_length(length_5_dagonal_cross_axis, {"target_length":5, "compare":0}))

    def test_misslabelled_point(self):
        misslabelled_point = {"x1": "-4", "@y1": "2", "@x2": "-7", "@y2": "-2"};
        self.assertFalse(check_line_length(misslabelled_point, {"target_length":0, "compare":0}))

    def test_none_number_point(self):
        none_number_point = {"x1": "four", "@y1": "2", "@x2": "-7", "@y2": "-2"};
        self.assertFalse(check_line_length(none_number_point, {"target_length":0, "compare":0}))

class TestCompareShapeAttribute(unittest.TestCase):
    shape = {"a": 5};

    def test_less_with_less(self):
        self.assertTrue(compare_shape_attribute(self.shape, {"target":6, "attribute":"a", "compare":-1}))
    
    def test_less_with_equal(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":5, "attribute":"a", "compare":-1}))

    def test_less_with_more(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":4, "attribute":"a", "compare":-1}))
    
    def test_equal_with_less(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":6, "attribute":"a", "compare":0}))
    
    def test_equal_with_equal(self):
        self.assertTrue(compare_shape_attribute(self.shape, {"target":5, "attribute":"a", "compare":0}))

    def test_equal_with_more(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":4, "attribute":"a", "compare":0}))

    def test_more_with_less(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":6, "attribute":"a", "compare":1}))
    
    def test_more_with_equal(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":5, "attribute":"a", "compare":1}))

    def test_more_with_more(self):
        self.assertTrue(compare_shape_attribute(self.shape, {"target":4, "attribute":"a", "compare":1}))

    def test_missing_arg(self):
        self.assertFalse(compare_shape_attribute(self.shape, {"target":5, "compare":0}))

    def test_missing_attr(self):
        missing_a = {"b": 5};
        self.assertFalse(compare_shape_attribute(missing_a, {"target":0, "attribute":"a", "compare":0}))

    def test_none_number_point(self):
        none_number_point = {"a", "four"};
        self.assertFalse(compare_shape_attribute(none_number_point, {"target_length":0, "attribute":"a", "compare":0}))

if __name__ == '__main__':  
    unittest.main()
