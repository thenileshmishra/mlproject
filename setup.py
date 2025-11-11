from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Read requirements.txt and return a list of valid requirement strings
    for install_requires. This:
      - strips whitespace
      - ignores blank lines and comments starting with '#'
      - ignores editable installs (-e ...), VCS (git+...), file: and http(s) URLs
    """
    requirements: List[str] = []
    with open(file_path, 'r') as f:
        for line in f:
            req = line.strip()
            if not req or req.startswith('#'):
                continue
            # skip editable and URL-like specifiers
            if req.startswith('-e') or req.startswith('git+') or req.startswith('file:') \
               or req.startswith('http:') or req.startswith('https:'):
                continue
            requirements.append(req)
    return requirements

# Meta data information about our project
setup(
    name="mlproject",
    version="0.0.1",
    author="Nilesh",
    author_email="thenileshmishra@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
