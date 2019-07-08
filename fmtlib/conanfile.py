#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
import os

class FmtConan(ConanFile):
    name = "fmt"
    version = "4.0.0"
    license = "MIT"
    url = "https://github.com/bincrafters/conan-fmt"
    description = "A safe and fast alternative to printf and IOStreams."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "header_only": [True, False]}
    default_options = "shared=True", "header_only=False"
    exports_sources = 'CMakeLists.txt'
    generators = 'cmake'

    build_requires = 'Ninja/[>=1.7]@aibs/stable'

    def config_options(self):
        if self.options.header_only:
            self.settings.clear()
            self.options.remove("shared")

    def source(self):
        source_url = "https://github.com/fmtlib/fmt.git"
        self.run('git clone {}'.format(source_url))
        self.run('cd fmt && git checkout tags/{}'.format(self.version))
        #tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        #os.rename("fmt-{0}".format(self.version), "sources")

    def build(self):
        if not self.options.header_only:
            cmake = CMake(self, generator="Ninja")
            cmake.definitions["FMT_TEST"] = False
            cmake.definitions["FMT_INSTALL"] = False
            cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
            cmake.configure(build_dir='build', source_dir='../fmt')
            cmake.build()

    def package(self):
        # Version > 4
        # self.copy("*.h", src='fmt/include/fmt', dst=os.path.join("include", "fmt"))
        # self.copy("*.so*", src='build', dst='lib')

        # Version 4
        self.copy("*.h", src='fmt/fmt', dst=os.path.join("include", "fmt"))
        self.copy("*.so*", src='build/fmt', dst='lib')

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        self.cpp_info.includedirs = ['include']

    def deploy(self):
        self.copy('*.so*', dst='lib', src='lib')

