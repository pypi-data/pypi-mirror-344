from setuptools import setup, Extension, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="alphagram",
    version="1.0.4",
    description="Easier access and Less Waits library for pyrogram",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://t.me/North_Yankton",
    author="Alpha",
    author_email="imr@outlook.in",
    license="MIT",
    keywords="alphagram library pyrogram tgcrypto telegram telethon python-telegram-bot",
    project_urls={
        "Tracker": "https://github.com/Alpha-Like/alphagram/issues",
        "Community": "https://t.me/SpLBots",
        "Source": "https://github.com/Alpha-Like/alphagram",
        "Documentation": "https://t.me/SpLBots",
    },
    python_requires="~=3.7",
    packages=find_packages(),
    test_suite="tests",
    zip_safe=False,
    install_requires = [
        'tgcrypto',
        'pyaes==1.6.1',
        'pysocks==1.7.1'
    ]
)

print("AlphaGram OP !")
