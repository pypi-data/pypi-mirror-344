import copy
from collections import defaultdict
from dataclasses import dataclass
from typing import Union

from lxml import html

from html_alg_lib.html_simplify.html2text import html_to_text
from html_alg_lib.html_simplify.html_utils import html_to_element


@dataclass
class Feature:
    node_idx: str
    node_text: str
    node_tag: str
    node_xpath: str
    node_tags: list[str]
    node_xpaths: list[str]
    class_trace: dict[int, str]
    id_trace: dict[int, str]

    def as_dict(self) -> dict:
        return self.__dict__


def prune_tree_by_xpath_list(
    raw_tree: html.HtmlElement, xpath_list: list[str]
) -> html.HtmlElement:
    """
    根据xpath列表修剪树，只保留xpath列表中的节点及其祖先节点
    假定xpath列表中的xpath是按照从上到下的顺序排列的，并且都是raw_tree的子节点

    Args:
        raw_tree (html.HtmlElement): 原始树
        xpath_list (list[str]): xpath列表

    Returns:
        html.HtmlElement: 修剪后的树
    """
    tree = copy.deepcopy(raw_tree)
    # 存储需要保留的父子关系：父节点 -> {子节点集合}
    parent_children_map = defaultdict(set)
    # 存储所有需要保留的节点（路径上的节点及其祖先）
    kept_nodes = set()

    # 遍历所有 XPath，收集父子关系和需保留的节点
    for xpath in xpath_list:
        elements = tree.xpath(xpath)
        for elem in elements:
            # 从当前元素向上遍历到根，构建完整路径
            path = []
            current = elem
            while current is not None:
                path.append(current)
                current = current.getparent()
            path.reverse()  # 调整为从根到元素的顺序

            # 记录每个层级父节点到子节点的关系
            for i in range(len(path) - 1):
                parent = path[i]
                child = path[i + 1]
                parent_children_map[parent].add(child)
                kept_nodes.update([parent, child])

    # 处理每个父节点：删除不在保留列表中的子节点
    for parent, allowed_children in parent_children_map.items():
        # 遍历当前父节点的所有子节点（复制列表避免迭代时修改）
        for child in list(parent.getchildren()):
            if child not in allowed_children:
                parent.remove(child)

    # 二次清理：删除未被任何路径引用的残留节点
    for node in tree.iter():
        if node not in kept_nodes and node != tree:
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)

    return tree


def extract_feature(
    pre_normalized_html: Union[str, html.HtmlElement],
    label_alg_readable_html: Union[str, html.HtmlElement],
    item_id_map: dict,
    node_idx_attr: str,
    alg_idx_attr: str,
    text_source: str = 'pre',
) -> list[dict]:
    """
    提取NeuScraper架构所需要的节点级特征
    针对label_alg_readable_html中的每个节点，通过映射到pre_normalized_html中的节点，获取特征
    特征包括：
    - 节点文本
    - 节点标签
    - 节点xpath
    - 节点class trace
    - 节点id trace
    最终以list[dict]的形式返回

    Args:
        pre_normalized_html (Union[str, html.HtmlElement]): 预归一化html 参见simplify.process_to_label_alg_html的输出
        label_alg_readable_html (Union[str, html.HtmlElement]): Algorithm化后的html 参见simplify.process_to_label_alg_html的输出
        item_id_map (dict): 节点id映射 参见simplify.process_to_label_alg_html的输出
        node_idx_attr (str): 节点id属性名 pre_normalized_html中的结点index的属性名 默认是cc-alg-node-idxs
        alg_idx_attr (str): 节点id属性名 label_alg_readable_html中的结点index的属性名 默认是_item_id
        text_source (str, optional): 提取文本特征的来源 默认是pre 即使用pre_normalized_html中的文本特征 可选值为alg 即使用label_alg_readable_html中的文本特征

    Raises:
        ValueError: 如果pre_normalized_html中没有找到node_idx_attr属性 或者label_alg_readable_html中没有找到alg_idx_attr属性
        ValueError: 如果pre_normalized_html中找到的node_idx_attr属性值不唯一 或者label_alg_readable_html中找到的alg_idx_attr属性值不唯一

    Returns:
        list[dict]: 节点级特征列表
    """
    # 如果传入的pre_normalized_html和label_alg_readable_html是字符串，则将其转换为html.HtmlElement
    if isinstance(pre_normalized_html, str):
        pre_normalized_root = html_to_element(pre_normalized_html)
    else:
        pre_normalized_root = pre_normalized_html
    if isinstance(label_alg_readable_html, str):
        label_alg_readable_root = html_to_element(label_alg_readable_html)
    else:
        label_alg_readable_root = label_alg_readable_html

    # 逐个结点的处理特征
    feature_list = []
    for alg_node in label_alg_readable_root.iter():

        # 如果alg_node没有alg_idx_attr属性，则跳过
        if alg_idx_attr not in alg_node.attrib:
            continue

        # 根据item_id_map获取pre_normalized_root中对应的node_idx_str
        # 并只保留叶子结点的node_idx
        alg_idx = alg_node.attrib[alg_idx_attr]
        pre_node_idx_str = item_id_map[alg_idx]
        pre_node_idx_list = [
            idx for idx in pre_node_idx_str.split(' ') if idx.startswith('L')
        ]
        if len(pre_node_idx_list) == 0:
            raise ValueError(f'pre_node_idx_list is empty for alg_idx: {alg_idx}')

        # 根据pre_node_idx_list获取pre_normalized_root中对应的node对象
        pre_node_list = []
        for pre_normalized_node_idx in pre_node_idx_list:
            # 这个xpath是寻找<XXX {node_idx_attr}="pre_normalized_node_idx">的结点
            pre_normalized_node = pre_normalized_root.xpath(
                f'//*[@{node_idx_attr}="{pre_normalized_node_idx}"]'
            )
            # 由于node_idx是唯一的，所以pre_normalized_node_idx对应的结点也是唯一的
            if not len(pre_normalized_node) == 1:
                raise ValueError(
                    f'pre_normalized_node_idx: {pre_normalized_node_idx} has {len(pre_normalized_node)} nodes'
                )
            pre_node_list.append(pre_normalized_node[0])

        # 获取xpath列表
        global_root = pre_normalized_root.getroottree()
        xpath_list = [global_root.getpath(pre_node) for pre_node in pre_node_list]
        tag_list = [pre_node.tag for pre_node in pre_node_list]

        # 从当前结点一直向上遍历，直到根结点，不断获取class和id，最后反序
        # 使用pre_node_list[0]来计算class_trace和id_trace
        current_node = pre_node_list[0]

        class_trace = []
        id_trace = []
        while current_node is not None:  # 包含根节点
            class_trace.append(current_node.attrib.get('class', None))
            id_trace.append(current_node.attrib.get('id', None))
            current_node = current_node.getparent()

        class_trace.reverse()
        id_trace.reverse()

        # 由于class和id可能是稀疏的，所以使用dict来存储
        class_trace = {
            i: class_str for i, class_str in enumerate(class_trace) if class_str
        }
        id_trace = {i: id_str for i, id_str in enumerate(id_trace) if id_str}

        # 根据text_source获取tag_text
        if text_source == 'alg':
            tag_text = html_to_text(alg_node)
        elif text_source == 'pre':
            # 修剪pre_normalized_root，只保留xpath_list中的节点及其祖先节点
            sub_tree = prune_tree_by_xpath_list(pre_normalized_root, xpath_list)
            tag_text = html_to_text(sub_tree)
        else:
            raise ValueError(f'text_source: {text_source} is not supported')

        # 构建Feature对象
        feature = Feature(
            node_idx=alg_idx,
            node_text=tag_text,
            node_tag=tag_list[0],
            node_xpath=xpath_list[0],
            node_tags=tag_list,
            node_xpaths=xpath_list,
            class_trace=class_trace,
            id_trace=id_trace,
        )
        feature_list.append(feature.as_dict())
    return feature_list


if __name__ == '__main__':
    html_file = '/home/qiujiuantao/project/html-alg-project/html-alg-lib/test.html'
    test_html = open(html_file, 'r').read()
    from html_alg_lib.simplify import process_to_label_alg_html

    result = process_to_label_alg_html(test_html)
    feature_list = extract_feature(
        result['pre_normalized'],
        result['alg'],
        result['item_id_map'],
        'cc-alg-node-idxs',
        '_item_id',
    )
    import json

    with open('features.json', 'w') as f:
        json.dump(feature_list, f, ensure_ascii=False, indent=4)
