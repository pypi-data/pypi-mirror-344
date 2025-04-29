from setuptools import setup, find_packages

setup(
    name='test-server', # PyPI 上的包名
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'test-server=test_server:main',
        ],
    },
    install_requires=[
        'fastapi==0.115.12',
        'mcp==1.6.0',
    ],
    author='MCP Demo',
    author_email='',
    description='A custom MCP SSE HTTP Server with parameter support.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Framework :: FastAPI',
    ],
)