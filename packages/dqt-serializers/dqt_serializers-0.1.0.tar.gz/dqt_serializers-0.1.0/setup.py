from setuptools import setup, find_packages

setup(
    name="dqt-serializers",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas>=1.3.0", "pyarrow>=5.0.0"],
    entry_points={
        "dqt.serializers": [
            "csv = dqt_serializers.csv_serializer:CsvSerializer",
            "json = dqt_serializers.json_serializer:JsonSerializer"
        ]
    }
)