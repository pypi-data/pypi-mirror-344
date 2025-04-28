from setuptools import setup, find_packages

setup(
    name='NetHyTech-STT-Smruti_Nayak',
    version='0.1',
    author='Smruti_Nayak',
    author_email='nayaksmrutiranjan38@gmail.com',
    description='This is a speech-to-text package created by Smruti Nayak',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ],
)
