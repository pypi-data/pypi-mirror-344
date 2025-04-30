from setuptools import setup, find_packages

setup(
    name='qte-parts-crawler',
    version='0.1.0',
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
        # 添加你的其他依赖
    ],
    entry_points={
        'console_scripts': [
            'qte-crawl=qte_parts_crawler.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)