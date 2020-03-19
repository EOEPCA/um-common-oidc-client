import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'eoepca-oidc',
  version = '0.0.1',
  author = 'EOEPCA',
  author_email = 'angel.lozano@deimos-space.com',
  description = 'Open ID Connect python library developed by the EOEPCA team',
  long_description = long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/EOEPCA/um-common-oidc-client',
  packages=setuptools.find_packages(),
  license='apache-2.0',
  keywords = ['OIDC', 'EOEPCA', 'client'],
  classifiers=[
    'Development Status :: 3 - Alpha',                      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
  ],
  python_requires='>=3.6',
)
