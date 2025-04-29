from setuptools import setup, find_packages

setup(
    name="guidewd-sitemap-seo-tool",   # <-- New Correct Name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'streamlit',  # <- you are using streamlit in your project!
    ],
    entry_points={
        'console_scripts': [
            'guidewd-analyze=guidewd.analyze_sitemap:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    author="Purva Tijare",
    author_email="your-email@example.com",  # Optional: Add your email here
    description="Analyze sitemap XML files for SEO optimization with suggestions using Streamlit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/guidewd-sitemap-seo-tool",  # <-- link to GitHub if you have it
)
