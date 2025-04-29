import copy
import os
from typing import Union

from html_alg_lib.html_simplify.cfg_reader import read_cfg
from html_alg_lib.html_simplify.pipeline import Pipeline


def get_default_cfg(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'html_simplify/assets', file_name)


def process_to_label_alg_html(html_str: str, pipeline_cfg: Union[str, dict, None] = None) -> dict:

    if pipeline_cfg is None:
        pipeline_cfg = get_default_cfg('default_label_simplify_cfg.jsonc')
    cfg_dict = read_cfg(pipeline_cfg)
    pipeline = Pipeline.from_cfg(cfg_dict)
    info, record = pipeline.apply_to_html(html_str)

    return {
        'pre_normalized': record['pre_normalized'],
        'alg': record['alg'],
        'item_id_map': info['item_id_map'],
    }


def process_to_cls_alg_html(html_str: str, fast: bool = True, pipeline_cfg: Union[str, dict, None] = None) -> str:
    if pipeline_cfg is None:
        pipeline_cfg = get_default_cfg('default_cls_simplify_cfg.jsonc')
    pipeline_cfg = read_cfg(pipeline_cfg)
    if fast:
        pipeline_cfg = copy.deepcopy(pipeline_cfg)
        # 清除中间的记录 避免element_to_html的额外开销
        for process_cfg in pipeline_cfg['pipeline']:
            if 'record_name' in process_cfg and process_cfg['record_name'] != 'alg':
                process_cfg.pop('record_name')

    pipeline = Pipeline.from_cfg(pipeline_cfg)
    _, record = pipeline.apply_to_html(html_str)
    if fast:
        return record['alg']
    else:
        return {
            'pre_normalized': record['pre_normalized'],
            'normalized': record['normalized'],
            'post_normalized': record['post_normalized'],
            'alg': record['alg'],
        }


def general_simplify(html_str: str, fast: bool = True, pipeline_cfg: Union[str, dict, None] = None) -> str:
    if pipeline_cfg is None:
        pipeline_cfg = get_default_cfg('default_general_simplify_cfg.jsonc')
    pipeline_cfg = read_cfg(pipeline_cfg)
    if fast:
        pipeline_cfg = copy.deepcopy(pipeline_cfg)
        # 清除中间的记录 避免element_to_html的额外开销
        for process_cfg in pipeline_cfg['pipeline']:
            if 'record_name' in process_cfg and process_cfg['record_name'] != 'alg':
                process_cfg.pop('record_name')

    pipeline = Pipeline.from_cfg(pipeline_cfg)
    _, record = pipeline.apply_to_html(html_str)
    if fast:
        return record['alg']
    else:
        return {
            'pre_normalized': record['pre_normalized'],
            'normalized': record['normalized'],
            'post_normalized': record['post_normalized'],
            'alg': record['alg']
        }
