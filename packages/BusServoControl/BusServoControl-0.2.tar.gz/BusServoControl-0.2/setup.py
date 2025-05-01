from setuptools import setup, find_packages

setup(
    name='BusServoControl',  # 包名
    version='0.2',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 依赖项
        "pyserial"
    ],
    author='Ma Fukang',  # 作者
    author_email='956787367@qq.com',  # 作者邮箱
    description='A module for controlling servo motors',  # 描述
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 长描述格式
    url='https://github.com/LeurDeLis/BusServoControl',  # 项目地址
    license='MIT',  # 许可证
)
