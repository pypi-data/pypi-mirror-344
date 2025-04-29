from typing import Callable, Reversible

from lxml import html


def remove_reversely(element_list: Reversible[html.HtmlElement]):
    for element in reversed(element_list):
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)


def remove_tags_by_types(
    root: html.HtmlElement, tag_type_list: list[str]
) -> html.HtmlElement:
    if not tag_type_list:
        return root
    xpath = '|'.join([f'.//{tag}' for tag in tag_type_list])
    remove_targets = root.xpath(xpath)
    remove_reversely(remove_targets)
    return root


def is_display_none(element: html.HtmlElement) -> bool:
    style = element.get('style', '').replace(' ', '').lower()
    if 'display:none' in style:
        return True


def remove_tags_with_condition(
    root: html.HtmlElement, condition: Callable[[html.HtmlElement], bool]
) -> html.HtmlElement:
    remove_targets = [element for element in root.iter() if condition(element)]
    remove_reversely(remove_targets)
    return root
