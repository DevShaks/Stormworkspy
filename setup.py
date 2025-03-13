from setuptools import setup, find_packages

setup(
    name='Stormworkspy',                   # Package name (should be unique on PyPI)
    version='0.1.0',                     # Initial version
    author='Shark',                  # Replace with your name
    author_email='-',  # Replace with your email
    description='A package providing a Flask API what allows to controll in game Stormworks vehicles',  # Short description
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DevShaks/Stormworkspy',  # Your project’s homepage
    packages=find_packages(),            # Automatically find your package folder(s)
    install_requires=[                   # List any dependencies your package needs
        'Flask'
    ],
    classifiers=[                        # Additional metadata about your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change if using another license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',             # Python version requirement
)
