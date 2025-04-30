import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="adbpg-mcp-server",
  version="1.0.0",
  author="Yutian Qiu",
  author_email="qiuytian@gmail.com",
  description="ADBPG MCP Server",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/aliyun/alibabacloud-adbpg-mcp-server",
  packages=setuptools.find_packages(),
  install_requires=[
    "psycopg>=3.1.0",
    "mcp>=1.4.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
  ],
  python_requires='>=3.10',
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)