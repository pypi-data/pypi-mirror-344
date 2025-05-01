import glob
import os
from setuptools import setup

import textract

# get all of the scripts
scripts = glob.glob("bin/*")

# read in the description from README
with open("README.md") as stream:
    long_description = stream.read()

github_url = 'https://github.com/supercog-ai/textract'


def parse_requirements(requirements_filename):
    """read in the dependencies from the requirements files
    """
    dependencies, dependency_links = [], []
    requirements_dir = os.path.dirname(requirements_filename)
    with open(requirements_filename, 'r') as stream:
        for line in stream:
            line = line.strip()
            if line.startswith("-r"):
                filename = os.path.join(requirements_dir, line[2:].strip())
                _dependencies, _dependency_links = parse_requirements(filename)
                dependencies.extend(_dependencies)
                dependency_links.extend(_dependency_links)
            elif line.startswith("http"):
                dependency_links.append(line)
            else:
                package = line.split('#')[0]
                if package:
                    dependencies.append(package)
    return dependencies, dependency_links


requirements_filename = os.path.join("requirements", "python")
dependencies, dependency_links = parse_requirements(requirements_filename)


setup(
    name="textract-supercog",
    # Updated version number
    version="1.6.5.post1",
    description="extract text from any document. no muss. no fuss.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=github_url,
    download_url="%s/archives/master" % github_url,
    # Added your info while preserving original attribution
    author='SuperCog AI (fork), Original author: Dean Malmgren',
    author_email='your.email@example.com',  # Replace with your email
    license='MIT',
    scripts=scripts,
    packages=[
        'textract',
        'textract.parsers',
    ],
    install_requires=dependencies,
    extras_require={
        "pocketsphinx": ["pocketsphinx==0.1.15"]
    },
    dependency_links=dependency_links,
    zip_safe=False,
    # Added classifiers for better PyPI categorization
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
