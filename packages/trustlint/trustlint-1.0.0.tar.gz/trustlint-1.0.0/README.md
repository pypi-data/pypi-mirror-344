# TrustLint

A powerful compliance linting tool for your development workflow, brought to you by ComplyEdge.

## Installation

### npm
```bash
npm install trustlint  
```

### pip
```bash
pip install trustlint
```

## Usage

```javascript
const trustLink = require('trustlint');
// The package will output its version and status
```

## Features

- Real-time compliance validation
- Integration with development workflows
- Automatic compliance checks
- Support for major regulatory frameworks

## Publishing to npm

To publish a new version:

1. Update version in `package.json`
2. Run `npm pack` to verify package contents
3. Run `npm publish` to publish to npm registry

## Publishing to PyPI (pip)

To publish a new version to PyPI:

1. Install the required tools:
   ```bash
   pip install twine wheel
   ```

2. Create a `setup.py` file in your project root:
   ```python
   from setuptools import setup, find_packages

   setup(
       name="trustlint",
       version="0.1.0",
       packages=find_packages(),
       install_requires=[
           # List your Python dependencies here
       ],
       author="ComplyEdge",
       author_email="support@complyedge.io",
       description="A powerful compliance linting tool",
       long_description=open("README.md").read(),
       long_description_content_type="text/markdown",
       url="https://github.com/yourusername/trustlint",
       classifiers=[
           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
       ],
       python_requires=">=3.6",
   )
   ```

3. Build the distribution packages:
   ```bash
   python setup.py sdist bdist_wheel
   ```

4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

   Note: You'll need to have a PyPI account and be logged in. You can create an account at https://pypi.org/

## Support

For questions or support, contact us at support@complyedge.io

## License

MIT © ComplyEdge 