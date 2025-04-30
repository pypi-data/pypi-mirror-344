from setuptools import setup, find_packages

setup(
    name='ipo_premium_client',
    version='1.0.3',
    author='Dhaval Mehta',
    description='Unofficial ipopremium.in client',
    long_description='Unofficial ipo premium client',
    url='https://github.com/dhaval-mehta/ipo-premium-client',
    keywords='ipo premium',
    python_requires='>=3.13, <4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
    ],
)