from setuptools import setup, find_packages

setup(
    name='autoview',
    version='0.1.0',
    description='One-line Python EDA assistant: auto-summary, insights, and visual report generation',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Avinash Betha',
    author_email='avinashb1581@gmail.com',
    url='https://github.com/avinash-betha/autoview',
    project_urls={
        'Documentation': 'https://github.com/avinash-betha/autoview',
        'Source': 'https://github.com/avinash-betha/autoview',
        'Tracker': 'https://github.com/avinash-betha/autoview/issues',
    },
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],
    packages=find_packages(exclude=["tests*", "examples*"]),
    include_package_data=True,
    install_requires=[
        'pandas>=1.0',
        'seaborn>=0.11',
        'matplotlib>=3.3',
        'tabulate>=0.8',
        'missingno>=0.5',
        'scikit-learn>=0.24'
    ],
    python_requires='>=3.6',
)
