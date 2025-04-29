from setuptools import setup, find_packages, find_namespace_packages

setup(
    name="yx-weather",          # 包名（需全局唯一，不可与 PyPI 上的包名重复）
    version="0.1.0",            # 版本号（建议遵循语义化版本）
    author="yxff",         # 作者名
    author_email="spflovling@163.com",  # 作者邮箱
    description="这是一个通过高德API获取某一城市区域实时天气的server",  # 简短描述
    long_description=open("README.md").read(),  # 详细描述（从 README.md 读取）
    long_description_content_type="text/markdown",  # 描述格式（如 Markdown）
    url="",  # 项目主页（可选）
    packages=find_namespace_packages(),
    # packages=find_namespace_packages(where='src', exclude=["*test*"]),
    # package_dir={"": "src"},
    # 自动发现所有包（包括子包）
    install_requires=[          # 运行时依赖项（如需要）
        "mcp",
        "httpx"
    ],
    classifiers=[               # 包的分类信息（用于 PyPI 分类）
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",   # 明确指定 Python 版本（3.10.17）
)