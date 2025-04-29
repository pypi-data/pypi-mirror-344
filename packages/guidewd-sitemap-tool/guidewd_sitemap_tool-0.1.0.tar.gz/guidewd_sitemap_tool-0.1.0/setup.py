from setuptools import setup, find_packages

setup(
    name="guidewd-sitemap-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'guidewd=guidewd.analyze_sitemap:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    author="Purva Tijare",
    author_email="your-email@example.com",  # <-- Replace or remove
    description="Analyze sitemap XML files for SEO optimization with suggestions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/guidewd-sitemap-seo-tool",  # <-- Replace or remove
)
