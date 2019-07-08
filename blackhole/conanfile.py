from conans import ConanFile, CMake, tools
import os


class BlackholeConan(ConanFile):
    name = 'Blackhole'
    version = '1.9.0'
    description = 'Yet another logging library'
    license = "MIT"
    url = 'http://stash.corp.alleninstitute.org/projects/OM/repos/conan.blackhole'
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    requires = 'Boost/1.67.0@aibs/stable'
    build_requires = ["CMake/3.12.1@aibs/stable", "Ninja/1.7.2@aibs/stable", "GCC/7.2.0@aibs/stable"]
    generators = 'cmake'

    def source(self):
        self.run('git clone https://github.com/3Hren/blackhole.git')
        # self.run('cd blackhole && git checkout tags/v{}'.format(self.version))
        self.run('git submodule update --init', True, 'blackhole')
        tools.replace_in_file('blackhole/CMakeLists.txt',
                              'project(${LIBRARY_NAME})',
                              'project(${LIBRARY_NAME} LANGUAGES CXX)\n' \
                              'include(../conanbuildinfo.cmake)\n' \
                              'conan_basic_setup(TARGETS)')

        tools.replace_in_file('blackhole/CMakeLists.txt',
                              '${Boost_LIBRARIES}',
                              'CONAN_PKG::Boost')

        # # Fix some kind of namespace collison
        # tools.replace_in_file('blackhole/src/format.cpp', 'CHAR_WIDTH', 'CHAR_WIDTH_hack')
        # tools.replace_in_file('blackhole/include/blackhole/sink/file.hpp',
        #         'template<class Rep, std::uintmax_t Denom>\nclass binary_unit<Rep, std::ratio<1, Denom>>;',
        #         '')

        # # Hack out bitrot that breaks against Boost 1.67 and newer
        # tools.replace_in_file('blackhole/CMakeLists.txt', 'src/sink/socket/tcp.cpp', '')
        # tools.replace_in_file('blackhole/CMakeLists.txt', 'src/sink/socket/udp.cpp', '')
        # tools.replace_in_file('blackhole/src/essentials.cpp', 'registry.add<sink::socket::tcp_t>(registry);', '')
        # tools.replace_in_file('blackhole/src/essentials.cpp', 'registry.add<sink::socket::udp_t>(registry);', '')
        # # tools.replace_in_file('blackhole/src/procname.cpp',
        # #         'return stdext::string_view(program_invocation_short_name, ::strlen(program_invocation_short_name));',
        #         'return stdext::string_view("broken", ::strlen("broken"));'
        #         )
        # tools.replace_in_file('blackhole/src/formatter/json.cpp',
        #         'node.AddMember(rapidjson::StringRef(name.data(), name.size()), value, allocator);',
        #         '')

        # tools.replace_in_file('blackhole/src/formatter/json.cpp',
        #     'std::is_same<T, std::int64_t>::value ||',
        #     'std::is_same<T, std::int64_t>::value || std::is_same<T, long long>::value ||')


    def build(self):
        cmake = CMake(self, generator="Ninja")
        cmake.configure(build_dir='build', source_dir='../blackhole')
        cmake.build()

    def package(self):
        self.copy('libblackhole*', dst='lib', src='build/lib')
        self.copy('*.hpp', dst='include', src='blackhole/include')

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']
        self.cpp_info.libs.append('blackhole')

    def deploy(self):
        self.copy('*.so*', dst='lib', src='lib')

