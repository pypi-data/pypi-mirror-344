from typing import Optional

from html_alg_lib.html_simplify.dom_framework import NodeIdxHelper
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


class AlgReadable(BaseProcess):
    """
    为了方便LLM理解，将html转换为算法可读的html
    1. 将原本经过处理的idx字符串（"1 2 L3 L4"）转换为算法可读的idx字符串（"1"）
    2. 移除所有

    Args:
        BaseProcess (_type_): _description_
    """

    def setup(self, remained_attr: list[str], replace_unenclosed_text_tag: str):
        self.remained_attr = remained_attr
        self.replace_unenclosed_text_tag = replace_unenclosed_text_tag
        self.alg_idx_attr = self.config['attributes']['alg_node_idxs']
        self.unenclosed_text_tag = self.config['tags']['unclosed_text']
        self.node_idx_attr = self.config['attributes']['node_idxs']

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        item_id_map = {}
        item_id = 0
        node_idx_helper = NodeIdxHelper(self.node_idx_attr)
        remained_attr = tuple([self.alg_idx_attr] + self.remained_attr)
        for elem in root.iter():
            if elem.tag == self.unenclosed_text_tag:
                elem.tag = self.replace_unenclosed_text_tag
            idx_str = node_idx_helper.get_idx_str(elem)
            if node_idx_helper.has_leaf_idx(idx_str):
                elem.attrib[self.alg_idx_attr] = str(item_id)
                item_id_map[str(item_id)] = idx_str
                item_id += 1

            for attr in list(elem.attrib.keys()):
                if attr not in remained_attr:
                    elem.attrib.pop(attr)
        return DataPack(root=root, info={'item_id_map': item_id_map})


class ClsAlgReadable(BaseProcess):
    """
    将html转换为cls算法可读的html
    """
    def setup(self, remained_attr: Optional[list[str]] = None):
        self.remained_attr = remained_attr
        self.unenclosed_text_tag = self.config['tags']['unclosed_text']

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        for elem in root.iter():
            if elem.tag == self.unenclosed_text_tag:
                elem.drop_tag()
            if self.remained_attr is not None:
                for attr in list(elem.attrib.keys()):
                    if attr not in self.remained_attr:
                        elem.attrib.pop(attr)
        return DataPack(root=root, info={})
