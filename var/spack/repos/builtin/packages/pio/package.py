# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install pio
#
# You can edit this file again by typing:
#
#     spack edit pio
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Pio(Package):
    """The Parallel IO library (PIO) is a high-level parallel I/O C/Fortran library
for structured grid applications."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url      = "https://github.com/NCAR/ParallelIO/archive/pio2_4_2.tar.gz"

    version('2.4.2', sha256='89bb4d4bac1fda3a656c5eb89db795aa9e102544b299436fd06a844fe8660216')
    version('2.4.1', sha256='c299e3c2b5aec3cc9aca31d210e21b070042174c6d47ff2e75a936da5e248e1f')
    version('2.4.0', sha256='0653515913ee4c6142b1c85bee306367cad524e2b7042db5a3085fb6d393a08c')
    version('2.3.1', sha256='afe46cf97f73b518594e58d55684d5e423306686414b43fcc8c5c12d31a345f5')
    version('2.3.0', sha256='d7d04839b5aff3de66f12e34c02a5fd0cf36a6d8d15de1586e1775da2e6aae55')

    def url_for_version(self, version):
        # important to use archive (from tag) here, not release tarballs
        base = "https://github.com/NCAR/ParallelIO/archive/pio{underscored}.tar.gz"

        # the 2.2.2 Release on GitHub actually points to 2.2.2a
        if version == Version('2.2.2'):
            real_version = Version('2.2.2a')
        else:
            real_version = version

        return base.format(underscored=real_version.underscored)

    variant('pnetcdf',
            default=True,
            description='build with parallel netcdf support'
    )

    variant('hdf5',
            default=True,
            description='build with hdf5 support'
    )

    variant('fortran',
            default=True,
            description='build PIO fortran libraries'
    )

    # FIXME: CMake builds actually begin around 1.8 -- not sure exactly where
    depends_on('cmake@2.8.12:', when='@2.0.0:', type='build')

    # always need MPI
    # FIXME: version(s) ?
    depends_on('mpi')

    depends_on('netcdf@4.6.1:', when='@2.4.2')
    depends_on('netcdf@4.6.0:', when='@2.4.1')
    depends_on('netcdf@4.5.0:', when='@2.4.0')
    depends_on('netcdf@4.4.1:', when='@2.3.0:2.3.1')

    # FIXME: Figure out which netcdf-fortran versions are required.  Simple
    #        solution is to start with the minimimum NetCDF-c version required
    #        by the Fortran lib
    depends_on('netcdf-fortran', when="+fortran")

    # NOTE: I think it's ok to separate the fortran dependency from the version
    #       dependencies here, i.e. the directives will be considered jointly
    #       by the concretizer.
    depends_on('parallel-netcdf+fortran', when='+fortran +pnetcdf')
    depends_on('parallel-netcdf@1.9.0:', when='@2.4.0:2.4.2 +pnetcdf')
    depends_on('parallel-netcdf@1.8.1:', when='@2.3.0:2.3.1 +pnetcdf')

    depends_on('hdf5@1.10.4:+hl',
               # HDF5 versions before 1.10.4 have a bug that PIO is sensitive
               # to.  +hl variant because NetCDF needs the HDF5 high level
               # interfaces unconditionally
               when='@2.4.0:2.4.2 +hdf5')

    # FIXME: CMake builds actually begin around 1.8 -- not sure exactly where
    # FIXME: Early versions of CMake builds may require
    #        - https://github.com/CESM-Development/CMake_Fortran_utils
    #        - https://github.com/PARALLELIO/genf90
    @when('@2.0.0:')
    def install(self, spec, prefix):

        cmake_args = [
            # Use the MPI compiler wrappers
            '-DCMAKE_C_COMPILER={}'.format(spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(spec['mpi'].mpicxx),
            '-DCMAKE_Fortran_COMPILER={}'.format(spec['mpi'].mpifc),
            # '-DMPI_BASE_DIR:PATH={}'.format(spec['mpi'].prefix),

            # requires GPTL, which isn't provided by spack yet
            '-DPIO_ENABLE_TIMING=OFF',

            # Spack's NetCDF is built with autotools, so the CMake config files
            # that FindNetCDF.cmake would look for are not present. Instead the
            # path has to specified manually.
            '-DNetCDF_C_PATH={}'.format(spec['netcdf'].prefix),
            # '-DNetCDF_Fortran_PATH={}'.format(spec['netcdf-fortran'].prefix),
            '-DPnetCDF_PATH={}'.format(spec['parallel-netcdf'].prefix),
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    # FIXME: CMake builds actually begin around 1.8 -- not sure exactly where
    @when('@:1.7.999')
    def install(self, spec, prefix):
        # FIXME: Implement autotools build
        pass
