from setuptools import find_packages, setup


def get_req(file_path):
    req_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line and not line.startswith('#'):
                req_list.append(line)
    return req_list


core_req = get_req('req/core.txt')
full_req = get_req('req/full.txt')

setup(
    name='html_alg_lib',
    version='2.0.1',
    packages=find_packages(include=['html_alg_lib*']),
    include_package_data=True,
    package_data={
        'html_alg_lib': ['html_simplify/assets/*.*'],
    },
    install_requires=core_req,
    extras_require={
        'full': full_req,
    },
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Qiu Jiantao',
    author_email='qiujiantao@pjlab.org.cn',
    python_requires='>=3.10',
)
