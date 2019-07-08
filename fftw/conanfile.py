from conans import ConanFile, CMake, tools
import os

class FFTWConan(ConanFile):
    name = "fftw"
    version = "3.3.8"
    description = "C subroutine library for computing the Discrete Fourier Transform (DFT) in one or more dimensions"
    url = "https://github.com/bincrafters/conan-fftw"
    homepage = "http://www.fftw.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0"
    exports = ["COPYRIGHT"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "precision": ["double", "single", "longdouble"],
               "openmp": [True, False], "threads": [True, False], "combinedthreads": [True, False]}
    default_options = 'shared=True', 'fPIC=True', 'precision=single', 'openmp=False', 'threads=False', 'combinedthreads=False'
    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]
     #_source_subfolder = "source_subfolder"
    #_build_subfolder = "build_subfolder"

    def configure(self):
        self.settings.compiler.libcxx = 'libstdc++11'
        # del self.settings.compiler.libcxx

    # def config_options(self):
    #     if self.settings.os == 'Windows':
    #         del self.options.fPIC

    def source(self):
        source_url = "http://www.fftw.org"
        tools.get("{0}/fftw-{1}.tar.gz".format(source_url, self.version))
        # self.source_dir = self.name + "-" + self.version
        #os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self, generator="Ninja")
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["ENABLE_OPENMP"] = self.options.openmp
        cmake.definitions["ENABLE_THREADS"] = self.options.threads
        cmake.definitions["WITH_COMBINED_THREADS"] = self.options.combinedthreads
        cmake.definitions["ENABLE_FLOAT"] = self.options.precision == "single"
        cmake.definitions["ENABLE_LONG_DOUBLE"] = self.options.precision == "longdouble"
        source_dir = self.name + "-" + self.version
        cmake.configure(build_dir='build', source_dir='../{}'.format(source_dir))
        cmake.build()
        cmake.install()

    def package(self):
        # Most of the package got copied by cmake.install()
        pass

    def package_info(self):
        self.cpp_info.libs = ['fftw3f']
        self.cpp_info.libdirs = ['lib']
        # allow access to FFTW3*.cmake files for find_package(FFTW3 CONFIG) when using cmake_paths generator
        self.cpp_info.builddirs = ["", "lib/cmake/fftw3"]

    def deploy(self):
        self.copy('*', dst='lib', src='lib')
