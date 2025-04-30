from setuptools import setup, find_packages

setup(
    name='qte-parts-crawler',
    version='0.1.2',
    packages=find_packages(),
    description='A web crawler for QTE parts data',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Allen Yan',
    author_email='wsyanligang@gmail.com',
    url='https://github.com/yourusername/qte-parts-crawler',  # 可改为你的 GitHub 地址
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        '2captcha-python',
        'certifi',
        'charset-normalizer',
        'idna',
        'selenium',
        'urllib3',
        'websocket-client',
        'Flask',
        'gunicorn',
        'Werkzeug',
        'dotenv'
        # 添加你的其他依赖
    ],
    entry_points={
        'console_scripts': [
            'qte-parts-crawler-cli=qte_parts_crawler.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
