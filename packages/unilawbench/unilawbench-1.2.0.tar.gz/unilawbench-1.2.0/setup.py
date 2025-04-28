from setuptools import setup, find_packages

setup(
    name='unilawbench',
    version='1.2.0',
    packages=find_packages(),
    package_data={
        'unilawbench': ['dataset/mcq/*.csv', 'dataset/qa/*.jsonl']
    },
    install_requires=[
        'evalscope',
        'evalscope[opencompass]',
        'evalscope[vlmeval]',
        'evalscope[rag]',
        'evalscope[perf]',
        'evalscope[app]',
        'evalscope[all]'
    ],
    entry_points={
        'console_scripts': [
            'unilawbench=unilawbench.cli:main'
        ]
    }
)