from setuptools import setup, find_packages

setup(
    name="guidewd-sitemap-generator",
    version="0.1.1",
    description="A command-line tool to generate sitemaps for a given URL.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Raghava Lab",
    author_email="raghava@iiitd.ac.in",
    url="https://github.com/KartikeyDhaka/GuideWD",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "guidewd-sitemap-generator=guidewd_sitemap_generator.cli_sitemap_generator:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
