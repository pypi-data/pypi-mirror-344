from setuptools import setup  

setup(  
    name="mcp_usee_user",  
    version="0.1.4",  
    packages=["mcp_usee_user"],  
    install_requires=["mcp>=1.5.0"],  
    entry_points={  
        "console_scripts": ["mcp-server=mcp_usee_user.main:main"]  
    },  
    description="测试mcp服务哈哈哈",  
    long_description=open("README.md").read(),  
    license="MIT"  
)  
