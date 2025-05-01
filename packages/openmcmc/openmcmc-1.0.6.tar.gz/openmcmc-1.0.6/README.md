<!--
SPDX-FileCopyrightText: 2024 Shell Global Solutions International B.V. All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
-->

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/openmcmc.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/openmcmc/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/openmcmc.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/openmcmc/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/sede-open/openMCMC/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/sede-open/openMCMC/actions/workflows/main.yml)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=coverage)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=bugs)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=pyelq_openmcmc&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=pyelq_openmcmc)
</div>

# openMCMC
openMCMC is a package for constructing Bayesian models from distributional components, and then doing parameter 
estimation using Markov Chain Monte Carlo (MCMC) methods. The package supports a number of standard distributions used 
in Bayesian modelling (e.g. Normal, gamma, uniform), and a number of simple functional forms for the parameters of 
these distributions. For a model constructed in the toolbox, a number of different MCMC algorithms are available, 
including simple random walk Metropolis-Hastings, manifold MALA, exact samplers for conjugate distribution choices, 
and reversible-jump MCMC for parameters with an unknown dimensionality.
***

# Installing openMCMC as a package
Suppose you want to use this openMCMC package in a different project.
You can install it from [PyPi](https://pypi.org/project/openmcmc/) through pip 
`pip install openmcmc`.
Or you could clone the repository and install it from the source code. After activating the environment you want to 
install openMCMC in, open a terminal, move to the main openMCMC folder
where pyproject.toml is located and run `pip install .`, optionally you can pass the `-e` flag is for editable mode.
All the main options, info and settings for the package are found in the pyproject.toml file which sits in this repo
as well.

***

# Examples
For some examples on how to use this package please check out these [Examples](https://github.com/sede-open/openMCMC/blob/main/examples)

***
# Contribution
This project welcomes contributions and suggestions. If you have a suggestion that would make this better you can 
simply open an issue with a relevant title. Don't forget to give the project a star! Thanks again!

For more details on contributing to this repository, see the [Contributing guide](https://github.com/sede-open/openMCMC/blob/main/CONTRIBUTING.md).

***
# Licensing

Distributed under the Apache License Version 2.0. See the [license file](https://github.com/sede-open/openMCMC/blob/main/LICENSE.md) for more information.
