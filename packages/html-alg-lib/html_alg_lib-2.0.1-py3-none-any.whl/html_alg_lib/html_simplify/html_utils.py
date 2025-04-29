from lxml import html


def html_to_element(html_str: str) -> html.HtmlElement:
    parser = html.HTMLParser(
        collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True
    )
    # Convert string to bytes if it contains an encoding declaration
    if isinstance(html_str, str) and (
        '<?xml' in html_str or '<meta charset' in html_str or 'encoding=' in html_str
    ):
        html_str = html_str.encode('utf-8')

    root = html.fromstring(html_str, parser=parser)
    return root


def pretty_print_html(html_str: str) -> str:
    from bs4 import BeautifulSoup

    return BeautifulSoup(html_str, 'html.parser').prettify()


def element_to_html(root: html.HtmlElement, pretty_print=False) -> str:
    html_str = html.tostring(root, encoding='utf-8').decode()
    if pretty_print:
        html_str = pretty_print_html(html_str)
    return html_str
