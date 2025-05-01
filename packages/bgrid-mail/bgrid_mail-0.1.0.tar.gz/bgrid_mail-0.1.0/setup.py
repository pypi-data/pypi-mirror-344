from setuptools import setup, find_packages

setup(
    name="bgrid_mail",  # Changed name to bgrid_mail
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="you@example.com",
    description="Simple HTML email sender via SMTP with user input for credentials",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bgrid_mail",  # Update URL if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
