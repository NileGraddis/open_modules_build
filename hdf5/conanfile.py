from conans import ConanFile, CMake, tools
import os

# HDF5 has many options and variations, which apparently do not play nice
# together.  Be *very* careful about arbitrarily mixing these features:
# 1) shared libraries (we want)
# 2) thread safety
# 3) C++ bindings (these are useless anyway)
# 4) ZLIB (required at AIBS)
# 5) external vs. local ZLIB
# 6) shared vs. static ZLIB (must be shared to link with shared HDF5)

# Coaxing in ZLib support is particularly dicey.  No dice linking to shared system
# zlib in a portable way, and the local ZLib build feature breaks also without
# a magic combo of features.

class Hdf5Conan(ConanFile):
    name = "HDF5"
    version = "1.10.3"
    description = "HDF5 libraries and utilities"
    license = "https://support.hdfgroup.org/ftp/HDF5/releases/COPYING"
    url = "http://stash.corp.alleninstitute.org/projects/OM/repos/conan.hdf5"
    settings = "os", "compiler", "build_type", "arch"

    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]
    options = {
        "cxx": [True, False],
        "shared": [True, False],
        "parallel": [True, False]
        }

    default_options = (
        "cxx=False",
        "shared=True",
        "parallel=False",
        )
    generators = 'cmake'

    def source(self):
        # Why not just a URL to the file?  This is really horrific when
        # changing HDF5 versions, because the magic string "wpdmdl=11810"
        # changes for each release, and you have to mess around on the website
        # to find the new magic bean.  Ugh.
        tools.download(
            'https://www.hdfgroup.org/package/source-gzip/?wpdmdl=12596',
            'hdf5-{}.tar.gz'.format(self.version)
        )
        tools.unzip("hdf5-{}.tar.gz".format(self.version))
        os.unlink("hdf5-{}.tar.gz".format(self.version))
        # tools.replace_in_file('hdf5-{}/CMakeLists.txt'.format(self.version),
        #         'PROJECT (HDF5 C CXX)',
        #         'PROJECT (HDF5 C CXX)\n' \
        #                 'include(../conanbuildinfo.cmake)\n' \
        #                 'conan_basic_setup(TARGETS)')

        tools.replace_in_file('hdf5-{}/config/cmake/HDFCompilerFlags.cmake'.format(self.version),
                '-Wconversion', '-Wno-conversion')
        tools.replace_in_file('hdf5-{}/config/cmake/HDFCompilerFlags.cmake'.format(self.version),
                '-Wstrict-prototypes', '-Wno-strict-prototypes')

        tools.download('https://www.zlib.net/zlib-1.2.11.tar.gz', 'zlib-1.2.11.tar.gz')

    def build(self):
        cmake = CMake(self, generator="Ninja")
        cmake_options = {
                'HDF5_ALLOW_EXTERNAL_SUPPORT': 'TGZ',
                'HDF5_ENABLE_THREADSAFE': False,
                'ZLIB_TGZ_NAME': 'zlib-1.2.11.tar.gz',
                'TGZPATH': self.build_folder,
                'HDF5_ENABLE_Z_LIB_SUPPORT': True,
                'ZLIB_USE_EXTERNAL': False,
                'HDF5_BUILD_CPP_LIB': False,
                'HDF5_BUILD_EXAMPLES': False,
                'HDF5_BUILD_TOOLS': False,
                'BUILD_TESTING': False,
                'BUILD_SHARED_LIBS': True,
                'H5_ENABLE_STATIC_LIB': False,
                }

        # Silence gcc warnings; this ancient C software is hopeless to patch here
        cmake.definitions["CMAKE_C_FLAGS"] = \
            "-Wno-sign-conversion -Wno-discarded-qualifiers -Wno-incompatible-pointer-types"

        cmake.configure(defs=cmake_options, build_dir='build', source_dir='../hdf5-{}'.format(self.version))
        # cmake.build(target='ZLIB')
        cmake.build()
        cmake.install()

    def package(self):
        # Most of the package got copied by cmake.install()
        self.copy('libz.*', src='build/bin', dst='lib')

    def package_info(self):
        self.cpp_info.libs = ['hdf5', 'z']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = ['include']

    def deploy(self):
        self.copy('*.so*', src='lib', dst='lib')
