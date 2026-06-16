from setuptools import setup, find_packages

setup(
    name="mac-perf-monitor",
    version="0.1.0",
    description="macOS Behavioral Causality Intelligence Engine",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "rumps>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "causalcore=mac_monitor.cli.main:main",
        ],
    },
    python_requires=">=3.8",
)
