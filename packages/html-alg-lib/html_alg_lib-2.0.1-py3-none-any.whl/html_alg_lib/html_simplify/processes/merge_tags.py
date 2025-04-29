from functools import lru_cache

from lxml import html

from html_alg_lib.html_simplify.dom_framework import (NodeIdxHelper,
                                                      is_mergeable_tag,
                                                      is_void_tag)
from html_alg_lib.html_simplify.html2text import (html_to_text,
                                                  html_to_text_fast)
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


# block is unmergeable
# 这个函数只会被find_no_block_element_recursive调用。
# 目前在处理同一个网页的时候，这个函数从第一次调用到最后一次调用之间，
# tag树是不会被修改的。所以可以lru_cache。
# 而切到下一个网页的时候，会创建新的root对象，所以LRU会失效。
# TODO 修改成使用手动的dict缓存。
@lru_cache(maxsize=None)
def has_unmergeable_element_recursive(root: html.HtmlElement) -> bool:
    # if the element is block tag, it has block child
    if not is_mergeable_tag(root.tag):
        return True
    else:
        # if the element has any child `has_block_element_recursive` is True
        # it is an element has block element
        return any(
            has_unmergeable_element_recursive(child) for child in root.getchildren()
        )


def find_no_block_element_recursive(root: html.HtmlElement) -> list[html.HtmlElement]:
    elements_with_no_block_element = []
    bfs_queue = [root]
    while bfs_queue:
        # handle current element
        current_element = bfs_queue.pop(0)
        if not has_unmergeable_element_recursive(current_element):
            # if current element has no block element
            # add to elements_with_no_block_element
            # and don't need to handle its children
            elements_with_no_block_element.append(current_element)

        else:
            # if current element has block element
            # try to find no block element in its children
            for child in current_element.getchildren():
                bfs_queue.append(child)
    return elements_with_no_block_element


class MergeNoBlockElement(BaseProcess):

    def setup(self):
        self.use_fast_html_to_text = self.config.get('use_fast_html_to_text', False)
        self.node_idx_attr = self.config['attributes']['node_idxs']
        self.html_to_text = (
            html_to_text_fast if self.use_fast_html_to_text else html_to_text
        )

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        node_idx_helper = NodeIdxHelper(self.node_idx_attr)
        elements_with_no_block_element = find_no_block_element_recursive(root)
        for element in elements_with_no_block_element:
            # merge the element with its parent
            element_text = self.html_to_text(element)
            # merge all children of element (recursively) to itself
            node_idx_helper.merge_node_idx_to_target(element, list(element.iter()))
            # add element_text to element
            element.text = element_text
            # remove all children of element
            for child in element.getchildren():
                element.remove(child)
        return DataPack(root=root, info={})


class MergeContinuousInlineLeafElement(BaseProcess):
    def setup(self):
        self.node_idx_attr = self.config['attributes']['node_idxs']
        self.use_fast_html_to_text = self.config.get('use_fast_html_to_text', False)
        self.html_to_text = (
            html_to_text_fast if self.use_fast_html_to_text else html_to_text
        )

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        node_idx_helper = NodeIdxHelper(self.node_idx_attr)
        for element in root.iter():
            child_list = list(element.getchildren())
            continue_inline_leaf_element_list = [[]]
            for child in child_list:
                if is_mergeable_tag(child.tag) and len(child) == 0:
                    continue_inline_leaf_element_list[-1].append(child)
                else:
                    continue_inline_leaf_element_list.append([])
            for inline_leaf_element_list in continue_inline_leaf_element_list:
                if len(inline_leaf_element_list) <= 1:
                    continue
                else:
                    merged_text = ' '.join(
                        [
                            self.html_to_text(element)
                            for element in inline_leaf_element_list
                        ]
                    )
                    if is_void_tag(inline_leaf_element_list[0].tag):
                        inline_leaf_element_list[0].tag = 'span'
                    inline_leaf_element_list[0].text = merged_text

                    node_idx_helper.merge_node_idx_to_target(
                        inline_leaf_element_list[0], inline_leaf_element_list
                    )
                    for child in inline_leaf_element_list[1:]:
                        element.remove(child)
        return DataPack(root=root, info={})
