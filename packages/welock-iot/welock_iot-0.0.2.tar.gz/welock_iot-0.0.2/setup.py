from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="welock_iot",
    version="0.0.2",
    author="hzjchina",
    author_email="hzjchina@yeah.net",
    description="welock_iot", 
    long_description=long_description,
    long_description_content_type="text/markdown",   
    # url="https://github.com/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "aiohttp>=3.8.1",
        "aiomqtt>=2.0.0,<3.0.0", 
    ],
    include_package_data=False,
    license='MIT'

)