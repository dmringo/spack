# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColormath(PythonPackage):
    """Color math and conversion library."""

    homepage = "https://pypi.python.org/pypi/colormath/2.1.1"
    url      = "https://pypi.io/packages/source/c/colormath/colormath-2.1.1.tar.gz"

    version('3.0.0', '3d4605af344527da0e4f9f504fad7ddbebda35322c566a6c72e28edb1ff31217')
    version('2.1.1', '10a0fb17e3c24363d0e1a3f2dccaa33b')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-networkx', type=('build', 'run'))
    depends_on('py-networkx@2.0:', type=('build', 'run'), when='@3.0.0:')
