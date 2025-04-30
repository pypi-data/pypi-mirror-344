from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A vectorized approach to Genetic Programming - PyTorch version'

setup(
    name='tensorgp',
    version=VERSION,
    author='Francisco Baeta',
    author_email='<fjrbaeta@dei.uc.pt>',
    description=DESCRIPTION,
    url='https://github.com/AwardOfSky/TensorGP/tree/pytorch',
    keywords=['Genetic Programming', 'Vectorization', 'GPU', 'Python', 'PyTorch'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    project_urls = {
        "Source": "https://github.com/AwardOfSky/TensorGP/tree/pytorch",
    },
    install_requires=[
        'scikit-image',
        'matplotlib',
    ],
    packages=find_packages(),
    include_package_data=True,
)
