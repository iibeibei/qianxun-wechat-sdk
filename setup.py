import setuptools  # 导入 setuptools 打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qianxun-wechat-sdk",  # 用自己的名替换其中的 YourPackageName
    version="0.0.3",  # 包版本号，便于维护版本
    author="XiaoMeng Mai",  # 作者，可以写自己的姓名
    author_email="beibei857@foxmail.com",  # 作者联系方式，可写自己的邮箱地址
    description="千寻微信框架SDK包",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",  # 包的详细介绍格式为markdown
    url="https://github.com/MaiXiaoMeng/qianxun-wechat-sdk",  # 自己项目地址，比如 github 的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
