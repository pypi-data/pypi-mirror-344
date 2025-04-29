from lxml import html

from html_alg_lib.html_simplify.dom_framework import is_block_tag
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


class WrapUnenclosedText(BaseProcess):

    def setup(self):
        self.unenclosed_text_tag = self.config['tags']['unclosed_text']

    def apply(self, input_data: DataPack) -> DataPack:
        """
        Wrap unenclosed text in a UNENCLOSED_TEXT_TAG tag

        Args:
            root (html.HtmlElement): The root of the html tree

        Returns:
            html.HtmlElement: The root of the html tree with unenclosed text wrapped
        """
        root = input_data.root
        for elem in root.iter():
            # if the element is inline and has no child, consider it as a text node
            # so we don't need to wrap it.
            if (not is_block_tag(elem.tag)) and len(elem) == 0:
                continue

            # if the element has child or the element is not inline
            # we need to wrap the text and tail in a UNENCLOSED_TEXT_TAG tag

            # check if the element has text and tail
            if elem.text and elem.text.strip():
                # wrap the text in a UNENCLOSED_TEXT_TAG tag
                text_tag = html.Element(self.unenclosed_text_tag)
                text_tag.text = elem.text
                elem.text = None
                elem.insert(0, text_tag)
            else:
                elem.text = None

            for child in elem.iterchildren():
                if child.tail and child.tail.strip():
                    # wrap the tail in a span tag
                    text_tag = html.Element(self.unenclosed_text_tag)
                    text_tag.text = child.tail
                    child.tail = None
                    child.addnext(text_tag)
                else:
                    child.tail = None
        return DataPack(root=root, info={})


class AddNodeIdx(BaseProcess):

    def setup(self):
        self.node_idx_attr = self.config['attributes']['node_idxs']

    def apply(self, input_data: DataPack) -> DataPack:
        """
        Add a unique node index to each node in the html tree

        Args:
            root (html.HtmlElement): The root of the html tree

        Returns:
            html.HtmlElement: The root of the html tree with node index
        """

        # 会遍历所有节点，设置节点索引
        # 每个节点的索引是 f"{prefix}{current_node_idx}"
        # prefix 当节点是叶子节点时为 "L"，否则为空
        # current_node_idx 是当前节点按root.iter()顺序的索引
        root = input_data.root
        node_idx = 0
        for elem in root.iter():
            idx_str = f"{'L' if len(elem) == 0 else ''}{node_idx}"
            elem.set(self.node_idx_attr, idx_str)
            node_idx += 1
        return DataPack(root=root, info={})
