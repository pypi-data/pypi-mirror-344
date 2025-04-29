import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="bogging",
    version="1.0.0",
    author="zzqq2199",
    author_email="zhouquanjs@qq.com",
    description="A copy of official logging module, to prevent conflict with other logging modules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["bogging"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)