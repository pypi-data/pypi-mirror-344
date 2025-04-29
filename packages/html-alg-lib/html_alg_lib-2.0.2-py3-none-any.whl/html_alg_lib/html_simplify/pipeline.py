import copy
from dataclasses import dataclass
from typing import List, Tuple, Union

from lxml import html

import html_alg_lib.html_simplify.processes as processes_module
from html_alg_lib.html_simplify.cfg_reader import read_cfg
from html_alg_lib.html_simplify.html_utils import (element_to_html,
                                                   html_to_element)
from html_alg_lib.html_simplify.processor import BaseProcess, DataPack


@dataclass
class ProcessPack:
    name: str
    instance: BaseProcess
    args: dict
    record_name: str

    def __str__(self):
        return f'ProcessPack(name={self.name}, instance={self.instance}, args={self.args}, record_name={self.record_name})'


class Pipeline:
    def __init__(self, processes: List[ProcessPack]):
        self.processes = processes
        self.info = {}
        self.record = {}

    @classmethod
    def from_cfg(cls, cfg: Union[dict, str]) -> 'Pipeline':
        if not isinstance(cfg, dict):
            cfg = read_cfg(cfg)
        processes = []
        for process_cfg in cfg['pipeline']:
            process_name = process_cfg['name']
            process_args = process_cfg['args']
            record_name = process_cfg.get('record_name', None)
            process_instance = getattr(processes_module, process_name)(config=cfg)
            process_instance.setup(**process_args)
            pack = ProcessPack(
                name=process_name,
                instance=process_instance,
                args=process_args,
                record_name=record_name,
            )
            processes.append(pack)
        return cls(processes)

    def _apply_process(self, root: html.HtmlElement) -> html.HtmlElement:
        self.info = {}
        self.record = {}
        for process_pack in self.processes:
            input_data = DataPack(root=root, info=self.info)
            output_data = process_pack.instance.apply(input_data)
            root = output_data.root
            self.info.update(output_data.info)
            if process_pack.record_name:
                self.record[process_pack.record_name] = element_to_html(root)
        return root

    def _apply_process_with_trace(
        self, root: html.HtmlElement
    ) -> List[html.HtmlElement]:
        self.info = {}
        self.record = {}
        root_trace = [{'stage': 'input', 'root': copy.deepcopy(root), 'config': None}]
        for process_pack in self.processes:
            input_data = DataPack(root=root, info=self.info)
            output_data = process_pack.instance.apply(input_data)
            root = output_data.root
            self.info.update(output_data.info)
            root_trace.append(
                {
                    'stage': process_pack.name,
                    'root': copy.deepcopy(root),
                    'config': process_pack.args,
                    'info': output_data.info,
                }
            )
            if process_pack.record_name:
                self.record[process_pack.record_name] = element_to_html(
                    root, pretty_print=False
                )
        return root_trace

    def apply_to_html(self, html_str: str) -> Tuple[dict, dict]:
        root = html_to_element(html_str)
        root = self._apply_process(root)
        return self.info, self.record

    def apply_to_html_with_trace(self, html_str: str) -> Tuple[List[dict], dict, dict]:
        root = html_to_element(html_str)
        root_trace = self._apply_process_with_trace(root)
        for trace in root_trace:
            trace['html'] = element_to_html(trace['root'])
            del trace['root']
        return root_trace, self.info, self.record
