<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/cp_logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/cp_logo.png">
  <img alt="concreteproperties logo" src="docs/_static/cp_logo.png">
</picture>

[![PyPI](https://img.shields.io/pypi/v/concreteproperties.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/concreteproperties.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/concreteproperties)][python version]
[![License](https://img.shields.io/pypi/l/concreteproperties)][license]
[![Read the documentation at https://concrete-properties.readthedocs.io/](https://img.shields.io/readthedocs/concrete-properties/stable.svg?label=Read%20the%20Docs)][read the docs]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)][ruff]
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Tests](https://github.com/robbievanleeuwen/concrete-properties/actions/workflows/ci.yml/badge.svg?branch=master)][tests]
[![Codecov](https://codecov.io/gh/robbievanleeuwen/concrete-properties/branch/master/graph/badge.svg)][codecov]


[pypi_]: https://pypi.org/project/concreteproperties/
[status]: https://pypi.org/project/concreteproperties/
[python version]: https://pypi.org/project/concreteproperties
[read the docs]: https://concrete-properties.readthedocs.io/
[uv]: https://github.com/astral-sh/uv
[ruff]: https://github.com/astral-sh/ruff
[pre-commit]: https://github.com/pre-commit/pre-commit
[tests]: https://github.com/robbievanleeuwen/concrete-properties/actions/workflows/ci.yml
[codecov]: https://app.codecov.io/gh/robbievanleeuwen/concrete-properties

`concreteproperties` is a python package that can be used to calculate the section
properties of arbitrary reinforced concrete sections. `concreteproperties` can calculate
gross, cracked and ultimate properties. It can perform moment curvature analyses
and generate moment interaction and biaxial bending diagrams. On top of this,
`concreteproperties` can also generate pretty stress plots!

Here's an example of some of the non-linear output `concreteproperties` can generate:

<p align="center">
  <img src="docs/_static/anim/anim_compress.gif" width="500"/>
</p>

## Installation

You can install `concreteproperties` via [pip] from [PyPI]:

```shell
pip install concreteproperties
```

## Documentation

`concreteproperties` is fully documented including a user walkthrough, examples,
background theory and an API guide. The documentation can found at
[https://concrete-properties.readthedocs.io/](https://concrete-properties.readthedocs.io/).

## Features

See the complete list of `concreteproperties` features
[here](https://concrete-properties.readthedocs.io/en/stable/user_guide.html).

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license], `concreteproperties` is free
and open source software.

## Support

Found a bug 🐛, or have a feature request ✨, raise an issue on the
GitHub [issue tracker](https://github.com/robbievanleeuwen/concrete-properties/issues)
Alternatively you can get support on the
[discussions](https://github.com/robbievanleeuwen/concrete-properties/discussions) page.

## Disclaimer

`concreteproperties` is an open source engineering tool that continues to benefit from
the collaboration of many contributors. Although efforts have been made to ensure the
that relevant engineering theories have been correctly implemented, it remains the
user's responsibility to confirm and accept the output. Refer to the
[license](LICENSE.md) for clarification of the conditions of use.

[pypi]: https://pypi.org/
[pip]: https://pip.pypa.io/
[license]: https://github.com/robbievanleeuwen/concrete-properties/blob/master/LICENSE
[contributor guide]: https://github.com/robbievanleeuwen/concrete-properties/blob/master/CONTRIBUTING.md
