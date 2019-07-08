from conans import ConanFile, CMake, tools
import os

class MettleConan(ConanFile):
    name = 'mettle'
    version = 'git'
    description = 'C++14 unit test framework'
    license = "BSD 3-clause"
    url = "https://jimporter.github.io/mettle"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    requires = 'Boost/1.67.0@aibs/stable'
    build_requires = "CMake/3.12.1@aibs/stable"
    generators = 'cmake'
    source_dir = 'mettle'

    def source(self):
        self.run('git clone https://github.com/JohnGalbraith/mettle.git')
        self.run('git submodule update --init', True, self.source_dir)
        tools.replace_in_file('{}/CMakeLists.txt'.format(self.source_dir),
                              'project(Mettle LANGUAGES CXX)',
                              'project(Mettle LANGUAGES CXX)\n' \
                              'include(../conanbuildinfo.cmake)\n' \
                              'conan_basic_setup()')

    def build(self):
        cmake = CMake(self, generator="Ninja")
        cmake.configure(build_dir='build', source_dir='../mettle')
        cmake.build()

    def package(self):
        self.copy("build/bin/mettle", dst="bin", keep_path=False)
        self.copy("mettle/scripts/mettle_junit.py", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy('*.hpp', dst="include", src="mettle/include")
        self.copy('bencode.hpp', dst="include", src="mettle/bencode.hpp/include")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libs = ['mettle']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']

