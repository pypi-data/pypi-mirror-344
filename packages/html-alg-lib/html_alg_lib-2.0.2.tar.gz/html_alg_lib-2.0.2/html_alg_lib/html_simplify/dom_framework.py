import json
import os
from enum import Enum
from functools import lru_cache
from typing import Optional, Union

from lxml import html


class NodeIdxHelper:

    @staticmethod
    def is_leaf_element(element: html.HtmlElement) -> bool:
        return len(element) == 0

    @staticmethod
    def idxs_to_str(idxs: list[str]) -> str:
        return ' '.join(idxs)

    @staticmethod
    def str_to_idxs(idx_str: str) -> list[str]:
        return idx_str.split(' ')

    @staticmethod
    def idx_to_int(idx_str: str) -> int:
        return int(idx_str) if not idx_str.startswith('L') else int(idx_str[1:])

    @staticmethod
    def has_leaf_idx(idx_str: str) -> bool:
        return 'L' in idx_str

    def __init__(self, node_idx_attr: str):
        self.node_idx_attr = node_idx_attr
        self._reset()

    def _reset(self):
        self.current_node_idx = 0

    def get_idx_str(self, element: html.HtmlElement) -> str:
        return element.get(self.node_idx_attr)

    def calc_next_node_idx_str(self, is_leaf: bool) -> str:
        prefix = 'L' if is_leaf else ''
        return f'{prefix}{self.current_node_idx}'

    def set_node_idx(self, element: html.HtmlElement):
        idx_attr = self.node_idx_attr
        idx_str = self.calc_next_node_idx_str(NodeIdxHelper.is_leaf_element(element))
        element.set(idx_attr, idx_str)
        self.current_node_idx += 1

    def merge_node_idx(self, elements: list[html.HtmlElement]) -> str:
        if len(elements) == 0:
            return ''
        idxs = []
        for element in elements:
            idxs.extend(NodeIdxHelper.str_to_idxs(element.get(self.node_idx_attr)))
        idxs = list(set(idxs))
        idxs = sorted(idxs, key=lambda x: NodeIdxHelper.idx_to_int(x))
        return NodeIdxHelper.idxs_to_str(idxs)

    def merge_node_idx_to_target(
        self,
        target: html.HtmlElement,
        elements: Union[list[html.HtmlElement], html.HtmlElement],
    ):
        if isinstance(elements, html.HtmlElement):
            elements = [elements]
        if target not in elements:
            elements.append(target)
        merged_idx_str = self.merge_node_idx(elements)
        target.set(self.node_idx_attr, merged_idx_str)


class MetaEnum(Enum):
    yes = 'yes'
    no = 'no'


class InlineBlockEnum(Enum):
    inline = 'inline'
    block = 'block'
    none = 'none'


class TextMediaEnum(Enum):
    text = 'text'
    media = 'media'
    none = 'none'
    svg = 'svg'


class InteractiveEnum(Enum):
    weak = 'weak'
    strong = 'strong'
    none = 'none'


class TagAttr:
    def __init__(
        self,
        tag: str,
        meta: MetaEnum,
        inline_block: InlineBlockEnum,
        text_media: TextMediaEnum,
        interactive: InteractiveEnum,
    ):
        self.tag = tag
        self.meta = meta
        self.inline_block = inline_block
        self.text_media = text_media
        self.interactive = interactive

    @classmethod
    def from_dict(cls, tag_attr_dict: dict) -> 'TagAttr':
        try:
            return cls(
                tag_attr_dict['tag'],
                MetaEnum(tag_attr_dict['meta']),
                InlineBlockEnum(tag_attr_dict['inline/block']),
                TextMediaEnum(tag_attr_dict['text/media']),
                InteractiveEnum(tag_attr_dict['interactive']),
            )
        except ValueError as e:
            print(
                f'Error parsing tag_attr_dict from {json.dumps(tag_attr_dict, indent=4, ensure_ascii=False)}'
            )
            raise e

    def to_dict(self) -> dict:
        return {
            'tag': self.tag,
            'meta': self.meta.value,
            'inline/block': self.inline_block.value,
            'text/media': self.text_media.value,
            'interactive': self.interactive.value,
        }

    def __str__(self) -> str:
        return f'TagAttr(tag={self.tag}, meta={self.meta.value}, inline/block={self.inline_block.value}, text/media={self.text_media.value}, interactive={self.interactive.value})'


def get_tags_attr(file_path: Optional[str] = None) -> dict:
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__),'assets', 'tags_attr.jsonl')
    tags_attr = {}
    with open(file_path, 'r') as f:
        for line in f:
            tag_attr = json.loads(line)
            tags_attr[tag_attr['tag']] = tag_attr
    return tags_attr


class TagsAttributesManager(dict):
    def __init__(self):
        tags_attr = {
            tag: TagAttr.from_dict(tag_attr)
            for tag, tag_attr in get_tags_attr().items()
        }
        super().__init__(tags_attr)

    def __getitem__(self, tag: str) -> TagAttr:
        return super().__getitem__(tag)


tags_attr = TagsAttributesManager()


@lru_cache(maxsize=1000)
def is_block_tag(tag: str, default: bool = False) -> bool:
    if tag not in tags_attr:
        return default
    return tags_attr[tag].inline_block == InlineBlockEnum.block


@lru_cache(maxsize=1000)
def is_media_tag(tag: str, default: bool = False) -> bool:
    if tag not in tags_attr:
        return default
    return tags_attr[tag].text_media in (TextMediaEnum.media, TextMediaEnum.svg)


@lru_cache(maxsize=1000)
def is_mergeable_tag(tag: str, default: bool = False) -> bool:
    return not (is_block_tag(tag, default) or is_media_tag(tag, default))


@lru_cache(maxsize=1000)
def is_void_tag(tag: str) -> bool:
    return tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr')
