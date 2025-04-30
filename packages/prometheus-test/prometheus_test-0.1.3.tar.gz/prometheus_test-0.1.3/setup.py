from setuptools import setup, find_packages

setup(
    name="prometheus-test",
    version="0.1.3",
    description="Test framework for Prometheus tasks",
    author="Laura Abro",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "pymongo>=4.0.0",
        "PyYAML>=6.0.0",
        "typing-extensions>=4.0.0",
    ],
    python_requires=">=3.8",
)
