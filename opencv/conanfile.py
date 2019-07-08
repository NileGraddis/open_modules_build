from conans import ConanFile, CMake

class OpenCVConan(ConanFile):
    name = 'OpenCV'
    description = 'Open Source Computer Vision Library'
    version = '4.0.0'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'http://opencv/license.html'
    url = 'http://stash.corp.alleninstitute.org/projects/OM/repos/conan.opencv'

    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]
    requires = 'OpenBLAS/[>=0.3.0]@aibs/stable'
    generators = 'cmake'

    def source(self):
        self.run('git clone https://github.com/opencv/opencv.git')
        self.run('cd opencv && git checkout tags/4.0.0')

    def build(self):
        cmake = CMake(self, generator='Ninja')
        cmake_options = {
            'WITH_QT': False,
            'WITH_GTK': False,
            'WITH_CUDA': False, # darn, CUDA requires gcc < 5.0.
            'WITH_IPP': False,
            'WITH_TBB': False,
            'WITH_OPENMP': False,
            'WITH_PTHREADS_PF': False,
            'WITH_EIGEN': True,
            'WITH_FFMPEG': False,
            'BUILD_PERF_TESTS': False,
            'BUILD_TESTS': False,
            'BUILD_DOCS': False,
            'BUILD_EXAMPLES': False,
            'BUILD_opencv_apps': False,
            'BUILD_opencv_python2': False, # Avoid build error that is not my problem to fix
            'BUILD_opencv_python3': False, # Avoid build error that is not my problem to fix
            'BUILD_opencv_python_bindings_generator': False, # Avoid build error that is not my problem to fix
            'BUILD_opencv_java_bindings': False,
            'BUILD_opencv_java_bindings_generator': False,
        }
        cmake.configure(defs=cmake_options, build_dir='build', source_dir='../opencv')
        cmake.build()

    opencv_libs = ['core', 'imgproc']

    def package(self):
        self.copy(pattern="*.h*", dst="include", src="opencv/include")
        self.copy(pattern="*.h*", dst="include/opencv2", src="build/opencv2")
        for lib in self.opencv_libs:
            self.copy(pattern="*.h*", dst="include", src="opencv/modules/%s/include" % lib)
        self.copy(pattern="*.so*", dst="lib", src="build/lib", keep_path=False)

    def package_info(self):
        libs_opencv = [
            'opencv_imgproc',
            'opencv_core' # GCC wants this last
        ]
        libs_linux = [
        ]
        libs = libs_opencv + libs_linux
        self.cpp_info.libs.extend(libs)

    def deploy(self):
        self.copy('*', dst='lib', src='lib')
