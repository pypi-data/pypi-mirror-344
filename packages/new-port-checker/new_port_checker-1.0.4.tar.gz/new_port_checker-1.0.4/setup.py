from setuptools import setup, find_packages

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'A Python tool for checking port availability'

setup(
    name='new_port_checker',
    # 修改为新的版本号
    version='1.0.4',
    description='A Python tool for checking port availability',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='liuxiaojian',
    author_email='107773270@qq.com',
    py_modules=['port_checker'],
    entry_points={
        'console_scripts': [
            'new_port_checker = port_checker:main',
        ],
    },
    url='https://github.com/yourusername/new_port_checker',  # 替换为实际项目地址
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)