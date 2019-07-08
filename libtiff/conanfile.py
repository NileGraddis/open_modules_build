from conans import ConanFile, CMake, tools
import os

class LibtiffConan(ConanFile):
    name = 'libtiff'
    version = '4.0.8'
    description = 'TIFF I/O library'
    license = "http://www.remotesensing.org/libtiff/"
    url = 'http://stash.corp.alleninstitute.org/projects/OM/repos/conan.libtiff'
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = 'cmake'
    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]
    source_dir = 'libtiff'

    def configure(self):
        self.settings.compiler.libcxx = 'libstdc++11'

    def source(self):
        self.run('git clone https://github.com/vadz/libtiff.git')
        tools.replace_in_file('{}/CMakeLists.txt'.format(self.source_dir),
                              'cmake_minimum_required',
                              'project(LibTIFF LANGUAGES C)\n'
                              'cmake_minimum_required')

        tools.replace_in_file('{}/CMakeLists.txt'.format(self.source_dir),
                              '# Read version information from configure.ac.',
                              'include(../conanbuildinfo.cmake)\n'
                              'conan_basic_setup()\n\n'
                              'set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_FULL_LIBDIR}")\n\n'
                              '# Read version information from configure.ac.')

        # Silence gcc warnings; this ancient C software is hopeless
        tools.replace_in_file('{}/CMakeLists.txt'.format(self.source_dir), '-Wall',
            '-Wimplicit-fallthrough=0 -Wformat -Wno-shift-negative-value '
            '-Wno-int-to-pointer-cast -Wno-format-truncation')

    def build(self):
        cmake = CMake(self, generator="Ninja")
        cmake.configure(build_dir='build', source_dir='../{}'.format(self.source_dir))
        cmake.build()

    def package(self):
        self.copy('*', dst='bin', src='build/bin')
        self.copy('*', dst='lib', src='build/lib')
        self.copy('*.h', dst='include', src='libtiff/libtiff')
        self.copy('*.h', dst='include', src='build/libtiff')

    def package_info(self):
        if self.package_folder:
            self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libs = ['tiff']
        self.cpp_info.libdirs = ['lib']

    def deploy(self):
        self.copy('libtiff*.so*', dst='lib', src='lib')
