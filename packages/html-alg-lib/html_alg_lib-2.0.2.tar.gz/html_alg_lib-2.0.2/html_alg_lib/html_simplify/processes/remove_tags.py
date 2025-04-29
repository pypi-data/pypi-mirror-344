from collections import deque

from lxml import html

from html_alg_lib.html_simplify.base_operations import (
    is_display_none, remove_tags_by_types, remove_tags_with_condition)
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


def remove_empty_tags_recursive(root: html.HtmlElement, predefined_non_empty_tags: set[str]) -> html.HtmlElement:
    leaf_elements = deque([node for node in root.iter() if len(node) == 0])

    while leaf_elements:
        leaf_element = leaf_elements.pop()
        parent = leaf_element.getparent()

        # 如果父节点为None，则说明该元素为根节点，跳过
        if parent is None:
            continue

        # 如果叶子节点为预定义的非空标签，则跳过
        if leaf_element.tag in predefined_non_empty_tags:
            continue

        # 如果叶子节点有文本内容，则跳过
        if leaf_element.text and leaf_element.text.strip():
            continue

        # 前面的条件都没触发，这是一个空标签，从父节点中删除
        parent.remove(leaf_element)

        # 如果经过删除操作后，父节点变成了叶子节点，则将父节点加入到叶子节点列表中
        if len(parent) == 0:
            leaf_elements.append(parent)
    return root


class RemoveEmptyTags(BaseProcess):
    """
    Remove all empty tags from the html page
    """
    def setup(self, predefined_non_empty_tags: list[str] = ['img', 'br']):
        self.predefined_non_empty_tags = set(predefined_non_empty_tags)

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        root = remove_empty_tags_recursive(root, self.predefined_non_empty_tags)
        return DataPack(root=root, info={})


class RemoveInvisibleTags(BaseProcess):
    """
    Remove all invisible tags from the html page
    """
    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        root = remove_tags_with_condition(root, is_display_none)
        return DataPack(root=root, info={})


class RemovePredefinedStylesTags(BaseProcess):
    """
    Remove all tags from the html page
    """
    def setup(self, tag_list: list[str]):
        for tag in tag_list:
            if not isinstance(tag, str):
                raise TypeError(f'tag_list must be a list of strings, got {type(tag)}')
        self.tag_list = tag_list

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        root = remove_tags_by_types(root, self.tag_list)
        return DataPack(root=root, info={})
