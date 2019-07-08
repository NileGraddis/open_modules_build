from conans import ConanFile, CMake, tools

# Warning: as of version 0.3.1, the OpenBLAS either shared or static has a
# static initialization bug.  Do not move past version 0.3.0 until this is
# fixed upstream.

class OpenBLAS(ConanFile):
    name = "OpenBLAS"
    version = "0.3.5"
    url = "https://github.com/xianyi/OpenBLAS"
    homepage = "http://www.openblas.net/"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."
    license = "BSD 3-Clause"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "USE_MASS": [True, False],
               "USE_OPENMP": [True, False],
               "USE_THREAD": [True, False],
               "NO_LAPACKE": [True, False]
              }
    default_options = "shared=True", "USE_MASS=False", "USE_OPENMP=False", "USE_THREAD=False", "NO_LAPACKE=False"
    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]

    def get_make_arch(self):
        return "32" if self.settings.arch == "x86" else "64"

    def get_make_build_type_debug(self):
        return "0" if self.settings.build_type == "Release" else "1"

    def get_make_option_value(self, option):
        return "1" if option else "0"

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            if not self.options.shared:
                raise Exception("Static build not supported in Visual Studio: "
                                "https://github.com/xianyi/OpenBLAS/blob/v0.2.20/CMakeLists.txt#L177")

    def source(self):
        self.run('git clone https://github.com/xianyi/OpenBLAS.git sources')
        self.run('cd sources && git checkout tags/v{}'.format(self.version))

    def build(self):
        # if self.settings.compiler != "Visual Studio":
        #     make_options = "DEBUG={0} NO_SHARED={1} BINARY={2} NO_LAPACKE={3} USE_MASS={4} USE_OPENMP={5}".format(
        #         self.get_make_build_type_debug(),
        #         False, #self.get_make_option_value(not self.options.shared),
        #         self.get_make_arch(),
        #         self.get_make_option_value(self.options.NO_LAPACKE),
        #         self.get_make_option_value(self.options.USE_MASS),
        #         self.get_make_option_value(self.options.USE_OPENMP))
        #     self.run("cd sources && make %s" % make_options, cwd=self.source_folder)
        # else:
        #    self.output.warn("Building with CMake: Some options won't make any effect")
        cmake = CMake(self)
        cmake.definitions["USE_MASS"] = self.options.USE_MASS
        cmake.definitions["USE_OPENMP"] = self.options.USE_OPENMP
        cmake.definitions["USE_THREAD"] = self.options.USE_THREAD
        cmake.definitions["NO_LAPACKE"] = self.options.NO_LAPACKE
        cmake.definitions["USE_SIMPLE_THREADED_LEVEL3"] = 1
        cmake.definitions["OMP_NUM_THREADS"] = 1
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE", dst="licenses", src="sources",
                      ignore_case=True, keep_path=False)

            if self.settings.compiler == "Visual Studio":
                self.copy(pattern="*.h", dst="include", src=".")
            else:
                self.copy(pattern="*.h", dst="include", src="sources")

            self.copy(pattern="*.dll", dst="bin", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

    def deploy(self):
        self.copy('*', src='lib', dst='lib')
