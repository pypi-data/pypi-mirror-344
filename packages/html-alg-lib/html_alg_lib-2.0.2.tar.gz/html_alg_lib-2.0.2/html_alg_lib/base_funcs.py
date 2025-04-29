import json

import chardet
from lxml import html

from html_alg_lib.html_simplify.html2text import html_to_text
from html_alg_lib.html_simplify.html_utils import html_to_element


def read_html_file(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        html_bytes = f.read()
    encoding = chardet.detect(html_bytes)['encoding']
    html_str = html_bytes.decode(encoding)

    try:
        json_res = json.loads(html_str)
        if isinstance(json_res, str):
            html_str = json_res
    except json.JSONDecodeError:
        pass
    return html_str


def get_title(root: html.HtmlElement) -> str:
    """
    Get the title of the html page

    Args:
        root (html.HtmlElement): The root of the html page

    Returns:
        str: The title of the html page
    """
    title = root.xpath('//title/text()')

    return title[0] if len(title) > 0 else None


def calc_tree_without_tags_length(root: html.HtmlElement) -> int:
    text = html_to_text(root)
    return len(text)


def calc_leaf_nodes(node: html.HtmlElement) -> int:
    if isinstance(node, str):
        node = html_to_element(node)
    count = 0
    if node.text and node.text.strip():
        count += 1
    for child in node:
        count += calc_leaf_nodes(child)
        if child.tail and child.tail.strip():
            count += 1
    return count
