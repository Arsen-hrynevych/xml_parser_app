xml_data = """
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
<value2>1</value2>
<meta>
    <date>today</date>
    <x>33</x>
</meta>
</root>
"""


def extract_xml_elements(xml_content):
    """
    Extracts XML elements (tags and text content) from an XML string.

    Args:
    xml_content (str): The XML data as a string.

    Returns:
    list: A list of strings containing XML tags and text content.

    Raises:
    ValueError: If the XML is malformed.
    """
    xml_elements = []
    tag_stack = []
    index = 0
    xml_length = len(xml_content)

    while index < xml_length:
        # Skip whitespace
        while index < xml_length and xml_content[index] <= " ":
            index += 1

        if index >= xml_length:
            break

        if xml_content[index] == "<":
            # Tag detection
            tag_end = xml_content.find(">", index)
            if tag_end == -1:
                raise ValueError("Malformed XML: missing closing '>'")

            full_tag = xml_content[index : tag_end + 1]
            xml_elements.append(full_tag)

            # Check if it's a closing tag
            if full_tag[1] == "/":
                tag = full_tag[2:-1]
                if not tag_stack or tag_stack[-1] != tag:
                    raise ValueError(f"Malformed XML: mismatched closing tag for <{tag}>")
                tag_stack.pop()
            elif full_tag[-2] != "/":
                tag = full_tag[1 : full_tag.find(" ", 1) if " " in full_tag[1:-1] else -1]
                tag_stack.append(tag)

            index = tag_end + 1
        else:
            # Text content
            next_tag = xml_content.find("<", index)
            if next_tag == -1:
                next_tag = xml_length

            text = xml_content[index:next_tag].strip()
            if text:
                xml_elements.append(text)

            index = next_tag

    if tag_stack:
        raise ValueError(f"Malformed XML: unclosed tags {', '.join(tag_stack)}")

    return xml_elements


def build_xml_structure(xml_elements):
    """
    Builds a dictionary representing the XML structure based on the list of extracted XML elements.

    Args:
        xml_elements (list): A list of XML tags and text content extracted from the XML string.

    Returns:
        dict: A nested dictionary representing the XML structure.
    """
    xml_structure = {"root": {}}
    root_structure = xml_structure["root"]
    root_structure["user"] = []

    parser_context = {"parent": root_structure, "current_tag": None, "user_context": None, "meta_context": None}

    for element in xml_elements:
        if element[0] == "<" and element[1] != "/":  # Opening tag
            current_tag = element[1:-1].strip()

            if current_tag == "user":
                parser_context["user_context"] = {}
                parser_context["parent"]["user"].append(parser_context["user_context"])
                parser_context["current_tag"] = "user"
            elif current_tag == "meta":
                parser_context["meta_context"] = {}
                parser_context["parent"]["meta"] = parser_context["meta_context"]
                parser_context["current_tag"] = "meta"
            elif current_tag in ["email", "name", "date", "x", "value1", "value2"]:
                parser_context["current_tag"] = current_tag
            else:
                parser_context["current_tag"] = None

        elif element[0] == "<" and element[1] == "/":  # Closing tag
            parser_context["current_tag"] = None

        else:
            # Assign values to the relevant fields
            if parser_context["current_tag"] == "email" and parser_context["user_context"] is not None:
                parser_context["user_context"]["email"] = element
            elif parser_context["current_tag"] == "name" and parser_context["user_context"] is not None:
                parser_context["user_context"]["name"] = element
            elif parser_context["current_tag"] == "date" and parser_context["meta_context"] is not None:
                parser_context["meta_context"]["date"] = element
            elif parser_context["current_tag"] == "x" and parser_context["meta_context"] is not None:
                parser_context["meta_context"]["x"] = int(element)
            elif parser_context["current_tag"] == "value1":
                parser_context["parent"]["value1"] = int(element)
            elif parser_context["current_tag"] == "value2":
                parser_context["parent"]["value2"] = int(element)

    root_structure["user"] = [user for user in root_structure["user"] if "email" in user and "name" in user]

    return xml_structure


def parse_xml_to_dict(xml_content):
    """
    Parses the XML content into a dictionary representation.

    Args:
        xml_content (str): The XML data as a string.

    Returns:
        dict: The parsed XML content as a dictionary.
    """
    xml_elements = extract_xml_elements(xml_content)
    return build_xml_structure(xml_elements)


parsed_xml_result = parse_xml_to_dict(xml_data)
print(parsed_xml_result)
