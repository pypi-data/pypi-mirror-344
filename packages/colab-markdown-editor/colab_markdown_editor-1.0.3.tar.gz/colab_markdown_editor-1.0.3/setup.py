from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="colab_markdown_editor",
    version="1.0.3",
    author="Thinh Vu",
    author_email="support@vnstocks.com",
    description="Interactive Markdown Editor for Google Colab Notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thinh-vu/colab_markdown_editor",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # "ipywidgets>=7.6"
    ],
    entry_points={
        "console_scripts": [
            "colab-markdown-editor = colab_markdown_editor.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: IPython",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Editors",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="markdown editor google colab ipywidgets",
    license="MIT",
    python_requires=">=3.11"
)
