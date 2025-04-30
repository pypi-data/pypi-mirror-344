from setuptools import setup, find_packages

setup(
    name="JunoMalacards",            # 包名（pip install时的名称）
    version="0.1.2",               # 版本号
    author="Juno of China",            # 作者
    description="crawler the Malacards from Juno",  # 简短描述
    packages=find_packages(),      # 自动发现所有包
    install_requires=[             # 依赖项
        "DrissionPage>=3.0",
        "lxml>=4.9.0",
        "requests>=2.28.0"
    ],
    python_requires=">=3.7",       # Python版本要求
    entry_points={                 # 命令行工具（可选）
        "console_scripts": [
            "JunoMalacards=JunoMalacards.core:main"
        ]
    },
)