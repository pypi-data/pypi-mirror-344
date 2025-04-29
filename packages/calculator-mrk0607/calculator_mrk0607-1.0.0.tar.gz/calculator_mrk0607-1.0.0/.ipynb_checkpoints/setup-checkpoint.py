from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',  # Use your actual Python version
    'Programming Language :: Python :: 3.11'
]

setup(
    name= "calculator-mrk0607",
    version='1.0.0',
    description='A very basic calculator module with simple math operations.',
    long_description = open('Readme.txt', encoding='utf-8').read() + '\n\n' + open('changelog.txt', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    url='https://github.com/pythonophile',  # Update with your actual URL or GitHub repo
    author="Muhammad Rizwan Khan Usafzai",
    author_email='rizviyousafzai123@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator basic math module education',
    packages=find_packages(),  # Will include the calculator package folder
    install_requires=[],  # No dependencies
    include_package_data=True,
)