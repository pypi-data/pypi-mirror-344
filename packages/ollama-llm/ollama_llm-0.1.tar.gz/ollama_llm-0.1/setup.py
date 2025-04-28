from setuptools import setup, find_packages

setup(
    name='ollama_llm',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'mss',
        'Pillow',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ollama_llm = ollama_llm:main'
        ]
    }
)
