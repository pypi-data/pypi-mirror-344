import json
import os

import aiohttp
import requests
from openai import AsyncOpenAI, OpenAI


class ClaudeshopClient:
    def __init__(self):
        self.Skey = self.get_default_key()
        self.url = 'https://api.claudeshop.top/v1/chat/completions'
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.Skey}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
        }

    def get_default_key(self):
        if 'GPT_KEY_FILE' not in os.environ:
            gpt_key_file = 'gpt_key.txt'
        else:
            gpt_key_file = os.environ['GPT_KEY_FILE']
        with open(gpt_key_file, 'r') as f:
            Skey = f.read().strip()
        return Skey

    def build_pay_load(self, prompt: str, model: str) -> dict:
        pay_load = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        }
        return json.dumps(pay_load, ensure_ascii=False)

    def call_api(self, prompt: str, model: str = 'gpt-4o') -> dict:
        payload = self.build_pay_load(prompt, model)
        response = requests.request(
            'POST', self.url, headers=self.headers, data=payload
        )
        data = response.json()
        return data

    async def call_api_async(self, prompt: str, model: str = 'gpt-4o') -> dict:
        payload = self.build_pay_load(prompt, model)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, headers=self.headers, data=payload
            ) as response:
                data = await response.json()
        return data


class AliCloudClient:
    def __init__(self):
        self.Skey = self.get_default_key()
        self.url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        self.client = OpenAI(api_key=self.Skey, base_url=self.url)
        self.async_client = AsyncOpenAI(api_key=self.Skey, base_url=self.url)

    def get_default_key(self):
        if 'ALI_KEY_FILE' not in os.environ:
            ali_key_file = 'ali_key.txt'
        else:
            ali_key_file = os.environ['ALI_KEY_FILE']
        with open(ali_key_file, 'r') as f:
            Skey = f.read().strip()
        return Skey

    def call_api(self, prompt: str, model: str = 'gpt-4o') -> dict:
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        return completion.to_dict()

    async def call_api_async(self, prompt: str, model: str = 'gpt-4o') -> dict:
        completion = await self.async_client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        return completion.to_dict()


def cut_for_json(input_str: str) -> str:
    # find first '{' and last '}'
    start = input_str.find('{')
    end = input_str.rfind('}')
    return input_str[start : end + 1]


def remove_comments(input_str: str) -> str:
    lines = input_str.split('\n')
    new_lines = []
    for line in lines:
        first_comment = line.find('//')
        if first_comment != -1:
            line = line[:first_comment]
        new_lines.append(line)
    return '\n'.join(new_lines)


def parse_json_smartly(json_str: dict) -> dict:

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(json_str)
        cut_json_str = cut_for_json(json_str)
        clean_json_str = remove_comments(cut_json_str)

    try:
        return json.loads(clean_json_str)
    except json.JSONDecodeError as e:
        print(clean_json_str)
        raise e


def get_node_annotations_prompt(data_dict: dict) -> str:
    node_annotations_prompt = f"""
你是一位熟悉HTML代码的前端工程师。现在需要通过阅读HTML代码来判断每一个元素的功能，并进一步判断该元素是否是该页面的主要内容还是其他内容。
具有以下特征的元素通常是主要内容：
  - 对于新闻，博客，文章，信息发布类网页，正文，正文中的配图，正文中需要被发布的信息属于主要内容，
  - 对于论坛，论坛的每一层，以及每一层的回复属于主要内容，
  - 对于问答类网站，问题和回答，以及针对问题的回复与每一个回答的回复等元素通常是主要内容。
具有以下特征的元素通常是补充信息：
  - 导航栏、侧边栏、页脚，相关文章，导航链接列表等元素通常属于其它信息。
  - 文章标题、正文的编者信息，评论内容的用户信息，点赞数，发布时间等元素通常是补充信息。注意，评论内容本身属于主要内容。

请针对每一个具有"_item_id"属性的元素，判断该元素的功能，并给出该元素是否是该页面的主要内容，其他内容。
如果是主要内容，你可以将元素记为"main"，如果是其他内容，你可以将元素记为"other"。

以下会提供一个经过简化的网页HTML代码，你需要判断出具有"_item_id"属性所在位置的元素的功能，并给出该元素是否是该页面的主要内容或是其他内容。
回答的格式例如：
{{
    "1": "other",
    "2": "main",
    "3": "other"
}}
以下是HTML代码：
```html
{data_dict["html"]}
```
注意不要输出解释性内容，json里也不要有注释。
"""
    return node_annotations_prompt


def get_gt_annotations_prompt(data_dict: dict) -> str:
    gt_annotations_prompt = f"""
你是一位熟悉HTML代码的前端工程师。现在需要通过阅读HTML代码来判断每一个元素是否是出现在人工抽取的主要内容中。
我会同时给你一份人工生成的网页抽取结果的文本，你需要以他作为金标准作为参考。如果网页中的某个元素属于主要内容，它对应的文本内容会出现在金标准中，如果不是主要内容，它对应的文本内容不会出现在金标准中。
你在判断这个元素是否属于主要内容的时候，需要先判断这个元素是否出现在金标准文本中。如果在那就是主要内容，否则是其他内容。
注意，同样的内容片段可能在一个网页中出现多次，请注意他们的相对位置和上下文，金标准的文本相当于你选取为main的所有元素用换行符连接起来的文本。所以同样内容的元素出现在不同的位置，可能会有不同的判断结果。

请针对每一个具有"_item_id"属性的元素，判断该元素的功能，并给出该元素是否是该页面的主要内容，其他内容。
如果是主要内容，你可以将元素记为"main"，如果是其他内容，你可以将元素记为"other"。
以下会提供一个经过简化的网页HTML代码和人工抽取的金标准文本，你需要判断出具有"_item_id"属性所在位置的元素的功能，并给出该元素是否是该页面的主要内容或是其他内容。
回答的格式例如：
{{
    "1": "other",
    "2": "main",
    "3": "other"
}}
以下是人工抽取的主要内容：
```txt
{data_dict["gt"]}
```
以下是HTML代码：
```html
{data_dict["html"]}
```
注意不要输出解释性内容，json里也不要有注释。
"""
    return gt_annotations_prompt


class ClientBuffer:
    def __init__(self):
        self._buffer = {}

    def get_client(self, client: str):
        if client not in self._buffer:
            if client == 'claudeshop':
                self._buffer[client] = ClaudeshopClient()
            elif client == 'aliyun':
                self._buffer[client] = AliCloudClient()
            else:
                raise ValueError(f'client {client} not supported')
        return self._buffer[client]


client_buffer = ClientBuffer()


def get_client_by_model(model: str):
    if model in ['gpt-4o', 'gpt-4o-mini']:
        return client_buffer.get_client('claudeshop')
    elif model == 'deepseek-r1':
        return client_buffer.get_client('aliyun')
    else:
        raise ValueError(f'model {model} not supported')


def get_prompt_by_mode(data_dict: dict, mode: str) -> str:
    if mode == 'node':
        return get_node_annotations_prompt(data_dict)
    elif mode == 'gt':
        return get_gt_annotations_prompt(data_dict)
    else:
        raise ValueError(f'mode {mode} not supported')


def call_node_annotations_api(
    data_dict: dict, model: str = 'gpt-4o', mode: str = 'node'
) -> dict:
    # "gpt-4o" or "gpt-4o-mini" use claudeshop
    # "deepseek-r1" use aliyun
    client = get_client_by_model(model)
    user_prompt = get_prompt_by_mode(data_dict, mode)
    data = client.call_api(user_prompt, model)
    content = data['choices'][0]['message']['content']
    return parse_json_smartly(content)


async def call_node_annotations_api_async(
    data_dict: dict, model: str = 'gpt-4o', mode: str = 'node'
) -> dict:
    # "gpt-4o" or "gpt-4o-mini" use claudeshop
    # "deepseek-r1" use aliyun
    client = get_client_by_model(model)
    user_prompt = get_prompt_by_mode(data_dict, mode)
    data = await client.call_api_async(user_prompt, model)
    content = data['choices'][0]['message']['content']
    return parse_json_smartly(content)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--html', type=str, help='HTML代码')
    args = parser.parse_args()
    with open(args.html, 'r') as f:
        html = f.read()
    import time

    start = time.time()
    data = call_node_annotations_api(html, model='gpt-4o-mini')
    total_time = time.time() - start

    print(data)
    print(f'Total time: {total_time:.2f}s')
