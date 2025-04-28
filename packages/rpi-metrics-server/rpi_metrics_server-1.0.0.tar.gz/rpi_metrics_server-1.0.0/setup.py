from setuptools import setup, find_packages

setup(
    name="rpi-metrics-server",
    version="1.0.0",
    author="QinCai-rui",
    author_email="raymontqin_rui@outlook.com",
    description="Monitor and manage Raspberry Pi system metrics via a Flask server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/QinCai-rui/RPi-Metrics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
        "Framework :: Flask",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flask",
        "flask-limiter",
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rpi-metrics-server=rpi_metrics.server.rpi_metrics_server:main',
        ],
    },
)
