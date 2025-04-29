import copy

import jieba
from bs4 import BeautifulSoup
from ltp import StnSplit
from lxml import html
from rouge_score.rouge_scorer import _summary_level_lcs

from html_alg_lib.html_simplify.dom_framework import NodeIdxHelper
from html_alg_lib.html_simplify.html_utils import (element_to_html,
                                                   html_to_element)

sentence_splitter_list = []


def get_sentence_splitter():
    """
    获取分句器
    """
    if len(sentence_splitter_list) == 0:
        sentence_splitter_list.append(StnSplit())
    return sentence_splitter_list[0]


def get_score(target: str, prediction: str) -> dict:
    """
    计算给定的参考文本和候选文本之间的rouge-L的precision，recall and F1 score

    Args:
        target (str): 参考文本
        prediction (str): 候选文本

    Returns:
        dict: 包含precision, recall, f1-score的字典
    """

    def get_sents(text):
        # 分句
        sents = get_sentence_splitter().split(text)
        sents = [x for x in sents if len(x)]
        return sents

    target_tokens_list = [
        [x for x in jieba.lcut(s) if x != ' '] for s in get_sents(target)
    ]
    prediction_tokens_list = [
        [x for x in jieba.lcut(s) if x != ' '] for s in get_sents(prediction)
    ]

    scoress = _summary_level_lcs(target_tokens_list, prediction_tokens_list)
    return scoress


def rouge_eval(target: str, prediction: str) -> dict:
    """
    计算给定的参考文本和候选文本之间的rouge-L的precision，recall and F1 score

    Args:
        target (str): Ground truth文本
        prediction (str): 预测文本

    Returns:
        dict: 包含precision, recall, f1-score的字典
    """
    t = {'prec': 1, 'rec': 1, 'f1': 1}
    if target == prediction:
        return t
    score = get_score(target, prediction)
    t['prec'] = score.precision
    t['rec'] = score.recall
    t['f1'] = score.fmeasure
    return t


# 该函数系原来的metric使用，继续保留
def get_content_text(html: str) -> str:
    """
    从html中提取文本内容

    Args:
        html (str): html字符串

    Returns:
        str: 文本内容
    """
    soup = BeautifulSoup(html, 'lxml')
    # 使用get_text()方法抽取所有文本内容，参数"\n"作为不同标签间的分隔符，strip=True去除多余空白
    text_content = soup.get_text('\n', strip=True)
    return text_content


def merge_labels_and_map(
    labels: dict[str, str], item_id_map: dict[str, str]
) -> dict[str, str]:
    """
    labels is the ["main", "other", "addi"] label of each algorithm node
    labels is like {alg_node_id_str: node_label_str}
    {"1": "main", "2": "other"} means alg_node_id_str 1 is main node, alg_node_id_str 2 is other node

    item_id_map is the map from pre_normalized_node_id_str to alg_node_id_str
    item_id_map is like {alg_node_id_str: pre_normalized_node_id_str}
    the pre_normalized_node_id_str is like "L1 L2 L3"
    {"1": "L1 L2 L3"} means alg_node_id_str 1 is the pre_normalized_node_id_str "L1 L2 L3"

    Example:
    labels = {"1": "main", "2": "other"}
    item_id_map = {"1": "L1 L2 L3", "2": "L4 L5"}
    result_map = {"L1": "main", "L2": "main", "L3": "main", "L4": "other", "L5": "other"}


    Args:
        labels (dict[str, str]): labels of each algorithm node
        item_id_map (dict[str, str]): map from pre_normalized_node_id_str to alg_node_id_str
    Returns:
        dict[str, str]: map from pre_normalized_node_id_str to label
    """
    result_map = {}
    for label_idx, raw_ids_str in item_id_map.items():
        raw_ids = raw_ids_str.split(' ')
        for raw_id in raw_ids:
            result_map[raw_id] = labels.get(label_idx, 'other')
    return result_map


def get_index_by_type(labels: dict[str, str], label: str) -> list[str]:
    """
    get the index list of the given label

    Example:
    labels = {"L1": "main", "L2": "main", "L3": "main", "L4": "other", "L5": "other"}
    label = "main"
    result = ["L1", "L2", "L3"]

    Args:
        labels (dict[str, str]): map from pre_normalized_node_id_str to label
        label (str): the label to filter
    Returns:
        list[str]: the index list of the given label
    """

    return [k for k, v in labels.items() if v == label]


def prune_html_element(
    root: html.HtmlElement, index_list: list[str], node_id_attr: str = 'cc-alg-node-idxs'
) -> html.HtmlElement:
    """
    prune the html element with the given index list
    remove all leaf nodes that are not in the index list

    Args:
        root (html.HtmlElement): the root element
        index_list (list[str]): the index list to show
    Returns:
        html.HtmlElement: the root element pruned with the given index list
    """
    # record the leaf elements to remained
    leaf_elements_to_remained = set()
    node_id_helper = NodeIdxHelper(node_id_attr)
    for element in root.iter():
        node_id_str = node_id_helper.get_idx_str(element)
        # if the node_id is not a leaf node, continue
        if not node_id_str.startswith('L'):
            continue

        # if the node_id is in the index_list, record the element to remained
        if node_id_str in index_list:
            leaf_elements_to_remained.add(element)

    all_elements_to_remained = leaf_elements_to_remained.copy()
    for leaf_element in leaf_elements_to_remained:
        # record all ancestor
        for ancestor in leaf_element.iterancestors():
            if ancestor not in all_elements_to_remained:
                all_elements_to_remained.add(ancestor)
            else:
                # if an ancestor is already in all_elements_to_remained, break
                break
    all_element_to_drop = []
    for element in root.iter():
        if element not in all_elements_to_remained:
            all_element_to_drop.append(element)
    for element in all_element_to_drop:
        if element.getparent() is not None:
            element.drop_tree()
    return root


def extract_with_label(
    html_str: str,
    labels: dict[str, str],
    item_id_map: dict[str, str],
    label_types: list[str] = ['main', 'other', 'addi'],
) -> dict[str, str]:
    """
    extract the html content with the given labels

    Args:
        html_str (str): the html string
        labels (dict[str, str]): the labels of each algorithm node
        item_id_map (dict[str, str]): the map from pre_normalized_node_id_str to alg_node_id_str
        label_types (list[str], optional): the labels to extract. Defaults to ["main", "other", "addi"].

    Returns:
        dict[str, str]: the extracted html content
    """

    ori_root = html_to_element(html_str)
    pre_normalized_node_labels = merge_labels_and_map(labels, item_id_map)
    html_map = {}
    for label in label_types:
        root = copy.deepcopy(ori_root)
        index_list = get_index_by_type(pre_normalized_node_labels, label)
        root = prune_html_element(root, index_list)
        html_map[label] = element_to_html(root)
        html_map[label + '_content'] = get_content_text(html_map[label])

    return html_map
