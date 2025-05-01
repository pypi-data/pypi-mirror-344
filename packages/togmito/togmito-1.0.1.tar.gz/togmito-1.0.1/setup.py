from setuptools import setup, find_packages

setup(
    name='togmito',
    version='1.0.1',  # her yüklemede farklı olmalı
    description='Kick ve Instagram için Telegram kontrollü AI bot',
    author='Aytunç',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mtranslate',
        'ollama',
        'selenium',
        'soundcard',
        'soundfile',
        'speechrecognition',
        'undetected-chromedriver',
        'certifi',
        'python-telegram-bot==20.7'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
