from setuptools import setup, find_packages 
# setuptools is the most common tool used for packaging Python projects.
# find_packages() automatically detects all sub-packages in your project by looking for __init__.py files.

setup(
    name="insurance_claims_fraud_detection",
    version="0.0.0",
    author="Mahesh",
    author_email="pachpandemahesh300@gmail.com",
    packages=find_packages()
)