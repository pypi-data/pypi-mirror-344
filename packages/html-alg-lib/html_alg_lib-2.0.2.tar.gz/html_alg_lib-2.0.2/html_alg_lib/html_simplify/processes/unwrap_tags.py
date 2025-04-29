from html_alg_lib.html_simplify.dom_framework import (NodeIdxHelper,
                                                      is_block_tag,
                                                      is_media_tag)
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


class UnwrapSingleChildDivTag(BaseProcess):
    def setup(self):
        self.node_idx_attr = self.config['attributes']['node_idxs']

    def apply(self, input_data: DataPack) -> DataPack:
        root = input_data.root
        node_idx_helper = NodeIdxHelper(self.node_idx_attr)
        divs_need_to_short_cut = []
        for elem in root.iter():
            if not elem.tag == 'div':
                continue
            parent = elem.getparent()
            if parent is None:
                continue
            if len(parent) > 1:
                continue
            if len(elem) > 1:
                continue
            divs_need_to_short_cut.append(elem)
        for elem in divs_need_to_short_cut:
            children = list(elem.getchildren())
            if len(children) == 1 and elem.getparent() is not None:
                if not is_block_tag(children[0].tag) and not is_media_tag(children[0].tag):
                    children[0].tag = 'div'
                node_idx_helper.merge_node_idx_to_target(children[0], elem)
                elem.drop_tag()
        return DataPack(root=root, info={})
