# 使用code-clean代码仓库中 app/format/html/html2text.py 的代码
# 原作者： https://github.com/jinzhenj
# 这里进行了一些简化：
# 1. 不进行markdown的转义
# 2. 不使用markdown的表格，而使用简单表格
# 3. 不包括markdown的各种格式（加粗斜体等）

import re
from typing import Tuple, Union

from lxml import etree, html
from lxml.etree import _Element

# fmt: off
newline_chars = set('\n\r')
space_chars = set(' \t\n\r\f\v')

newline_tags = set(['li', 'dd', 'th', 'td'])

block_tags = set([
    # only block
    'article', 'aside', 'section', 'footer', 'header', 'main',
    'hgroup', 'search', 'div', 'nav', 'option', 'center', 'address',
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'form', 'pre',
    'table', 'ul', 'ol', 'dir', 'menu', 'dl', 'blockquote',
    'figure', 'figcaption', 'fieldset', 'legend',
    'details', 'summary', 'html', 'body', 'hr', 'dt',
])

# not used: _{}[]()+!
escaped_chars = r'[\\`*_{}\[\]()>#.!+-]'
# fmt: on


def _try_parse_int(s, default=None):
    try:
        return int(s) if s else default
    except Exception:
        return default


def is_newline(c: str):
    return c in newline_chars


def is_space(c: str):
    return c in space_chars


def chomp(text: str, newline_only=False) -> Tuple[str, str, str]:
    fn = is_newline if newline_only else is_space
    a, b, length = 0, 0, len(text)
    while a < length and fn(text[a]):
        a += 1
    while b < (length - a) and fn(text[length - b - 1]):
        b += 1
    return text[:a], text[a : length - b], text[length - b :]


def fold_space(text: Union[str, None]) -> Tuple[int, str, int]:
    if text is None:
        return 0, '', 0
    left, mid, right = chomp(text)
    left = 1 if len(left) else 0
    mid = re.sub(r'[ \t\n\r\f\v]+', ' ', mid)
    right = 1 if len(right) else 0
    return left, mid, right


def keep_space(text: Union[str, None]) -> Tuple[int, str, int]:
    return 0, (text or ''), 0


def indent(text: str, mark='', skip_first_line=False):
    mark = mark or '  '
    ret = ''
    next_lines = False
    for line in text.split('\n'):
        ret += '\n' if next_lines else ''
        ret += mark if next_lines or not skip_first_line else ''
        ret += line
        next_lines = True
    return ret


def _md_add_code(text: str):
    left, mid, right = chomp(text)
    return f'{left}`{mid}`{right}' if (mid and '```' not in mid) else text


_md_handlers = {
    'code': _md_add_code,
}


def html_to_text(html: Union[_Element, str]) -> str:
    """1. media is ignored.
    2. table with different num of columns(colspan), is not convertible.
    3. table with cell's content has newline, is not convertible."""

    def get_rows(table: _Element):
        for sub_elem in table:
            if sub_elem.tag == 'tr':
                yield sub_elem
            elif sub_elem.tag in ['thead', 'tbody', 'tfoot']:
                yield from get_rows(sub_elem)

    def is_head_row(row: _Element):
        parent = row.getparent()
        if parent is not None and parent.tag == 'thead':
            return True
        cells = [c for c in row if c.tag in ['th', 'td']]
        return all([c.tag == 'th' for c in cells])

    def render_plain_table(cap: list, rows: list, has_head_row: bool):
        row_texts = []
        for row in rows:
            row_text = ''
            for cell in row:
                row_text += f'{cell[1]} '
            row_texts.append(row_text)
        caption = f'{cap[0][1]}\n\n' if cap else ''
        return caption + '\n'.join(row_texts)

    def helper(elem: _Element, in_pre=False, in_table=False, li_idx=0):
        """return (left, text, right):
        left/right: 0[no space], 1[has space], 2[has newline] 3[block]"""

        if elem.tag == 'br':
            return 0, '\n', 0
        if elem.tag == 'hr':
            return 3, '---', 3

        sub_in_pre = in_pre or elem.tag == 'pre'

        if sub_in_pre:
            fn = keep_space
        else:
            fn = fold_space

        sub_li_idx = 0
        if elem.tag == 'ol':
            sub_li_idx = max(1, _try_parse_int(elem.attrib.get('start'), 0))

        if not in_pre and elem.tag == 'table':
            cap = []
            if len(elem) and elem[0].tag == 'caption':
                cap.append(helper(elem[0], sub_in_pre, in_table, sub_li_idx))

            rows = []
            has_head_row = False
            for idx, row in enumerate(get_rows(elem)):
                rows.append([])
                if idx == 0:
                    has_head_row = is_head_row(row)
                for cell in [c for c in row if c.tag in ['th', 'td']]:
                    rows[-1].append(helper(cell, sub_in_pre, True, sub_li_idx))

            table_md = render_plain_table(cap, rows, has_head_row)
            if table_md:
                return 3, table_md, 3

            lst = [*cap]
            for row in rows:
                lst.extend(row)

        else:
            lst = [fn(elem.text)]
            for sub_elem in elem:
                lst.append(helper(sub_elem, sub_in_pre, in_table, sub_li_idx))
                lst.append(fn(sub_elem.tail))
                sub_li_idx += 1 if sub_li_idx and sub_elem.tag == 'li' else 0

        pre, text, post = 0, '', 0

        for left, mid, right in lst:
            pre = max(pre, 0 if text else left)
            post = max(post, left)

            if mid and text and post:
                if post == 3:
                    text += '\n\n'
                elif post == 2:
                    text += '\n'
                elif not (is_space(text[-1]) or is_space(mid[0])):
                    text += ' '
            if mid:
                text += mid
                post = 0

            pre = max(pre, 0 if text else right)
            post = max(post, right)

        if elem.tag in block_tags:
            pre, post = 3, 3
        elif elem.tag in newline_tags:
            pre, post = max(pre, 2), max(post, 2)

        if not in_pre and text:
            handler = _md_handlers.get(elem.tag)
            if handler is not None:
                text = handler(text)

            if not in_table:
                if elem.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    left, mid, right = chomp(text, newline_only=True)
                    text = left + ('#' * int(elem.tag[1])) + ' ' + mid + right
                elif elem.tag in ['li', 'dd']:
                    bp = f'{li_idx}. ' if li_idx else '- '
                    text = bp + indent(text, mark=' ' * len(bp), skip_first_line=True)
                elif elem.tag == 'blockquote':
                    text = indent(text, mark='> ')
                elif elem.tag == 'pre':
                    text = f'```\n{text}\n```'

        return pre, text, post

    if isinstance(html, str):
        html = etree.HTML(html)

    return helper(html)[1]


def sub_continuous_space_and_newline(text: str) -> str:
    # 将连续的空格（不包括换行符）替换为单个空格
    text = re.sub(r'\s+', ' ', text)
    # 将\n空行\n替换为\n
    text = re.sub(r'\n\s*\n', '\n', text)
    return text


def html_to_text_fast(element: html.HtmlElement) -> str:
    return sub_continuous_space_and_newline(element.text_content())
