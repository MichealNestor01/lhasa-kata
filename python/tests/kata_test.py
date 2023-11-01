import unittest
from src.lhasakata.kata import any_red_circles, count_svg_elements, any_colour_of_shape, only_colour_of_shape, blue_circles_categorisation, text_containing_message, compare_all_lines_with_length


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

class TestCompareAllLinesWithLength(unittest.TestCase):
    def test_no_lines(self):
        svg_dict = {}
        self.assertTrue(compare_all_lines_with_length(svg_dict, 10, 0))

    # TODO: finish task
    def finish_tests(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
