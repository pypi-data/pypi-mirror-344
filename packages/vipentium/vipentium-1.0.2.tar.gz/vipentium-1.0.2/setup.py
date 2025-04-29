from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vipentium",
    version="1.0.2",  # Replace with your desired version
    author="suresh",  # Replace with your name or organization
    description="Powerful & user-friendly Python testing – streamlined workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Suresh-pyhobbyist/vipentium",  # Replace with your project's GitHub URL
    packages=find_packages(),
    install_requires=[],  # List any dependencies your framework needs
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
    entry_points={
    'console_scripts': [
        'vipentium-runner = vipentium.vipentium_runner:main'
    ],
}
)



