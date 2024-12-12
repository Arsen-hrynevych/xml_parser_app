import unittest

from main import (
    parse_xml_to_dict,
    build_xml_structure,
    extract_xml_elements
)


class TestXMLParsing(unittest.TestCase):
    """
    A test suite for XML parsing functions.

    This class contains unit tests for the functions extract_xml_elements,
    build_xml_structure, and parse_xml_to_dict.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method is called before each test. It initializes a sample XML string
        that will be used in the tests.
        """
        self.xml_data = """
        <root>
        <user>
         <email>123@gmail.com</email>
         <name>name1</name>
        </user>
        <user>
         <email>321@gmail.com</email>
         <name>name2</name>
        </user>
        <value1>1</value1>
        <value2>2</value2>
        <meta>
         <date>today</date>
         <x>33</x>
        </meta>
        </root>
        """
        
    def test_extract_xml_elements(self):
        """
        This test checks if the function correctly extracts XML elements
        (tags and text content) from the input XML string.
        """
        expected_elements = [
            "<root>", "<user>", "<email>", "123@gmail.com", "</email>", 
            "<name>", "name1", "</name>", "</user>", 
            "<user>", "<email>", "321@gmail.com", "</email>", 
            "<name>", "name2", "</name>", "</user>", 
            "<value1>", "1", "</value1>", 
            "<value2>", "2", "</value2>", 
            "<meta>", "<date>", "today", "</date>", 
            "<x>", "33", "</x>", "</meta>", "</root>"
        ]
        
        result = extract_xml_elements(self.xml_data)
        self.assertEqual(result, expected_elements)
    
    def test_build_xml_structure(self):
        """
        This test checks if the function correctly builds a dictionary
        representing the XML structure from the list of extracted XML elements.
        """
        xml_elements = extract_xml_elements(self.xml_data)
        expected_structure = {
            'root': {
                'user': [
                    {'email': '123@gmail.com', 'name': 'name1'},
                    {'email': '321@gmail.com', 'name': 'name2'}
                ],
                'value1': 1,
                'value2': 2,
                'meta': {'date': 'today', 'x': 33}
            }
        }

        result = build_xml_structure(xml_elements)
        self.assertEqual(result, expected_structure)

    def test_parse_xml_to_dict(self):
        """
        This test checks if the function correctly parses the XML string
        into a dictionary representation.
        """
        expected_parsed_dict = {
            'root': {
                'user': [
                    {'email': '123@gmail.com', 'name': 'name1'},
                    {'email': '321@gmail.com', 'name': 'name2'}
                ],
                'value1': 1,
                'value2': 2,
                'meta': {'date': 'today', 'x': 33}
            }
        }
        result = parse_xml_to_dict(self.xml_data)
        self.assertEqual(result, expected_parsed_dict)

    def test_empty_xml(self):
        """
        This test checks if the parse_xml_to_dict function handles
        an empty XML string correctly.
        """
        empty_xml = ""
        expected_result = {'root': {'user': []}}
        result = parse_xml_to_dict(empty_xml)
        self.assertEqual(result, expected_result)
        
    def test_malformed_xml(self):
        """
        This test checks if the extract_xml_elements function raises
        a ValueError when given malformed XML.
        """
        malformed_xml = "<root><user><email>123@gmail.com<name>name1</root>"
        with self.assertRaises(ValueError):
            extract_xml_elements(malformed_xml)

if __name__ == '__main__':
    unittest.main()
