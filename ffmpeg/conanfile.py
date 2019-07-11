from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class FFMpegConan(ConanFile):
    name = "FFmpeg"
    version = "3.4.2"
    url = "https://github.com/bincrafters/conan-ffmpeg"
    description = "Video Codecs"
    license = "https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md"
    settings = "os", "arch", "compiler", "build_type"

    generators = 'pkg_config', 'virtualenv'
    build_requires = 'yasm_installer/1.3.0@aibs/stable'
    requires = 'openh264/1.7.0@aibs/stable'

    def source(self):
        self.run('git clone https://github.com/FFmpeg/FFmpeg.git')
        self.run('cd FFmpeg && git checkout tags/n3.4.2')

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.flags.append('-Wno-deprecated-declarations')
        env_build.flags.append('-Wno-format-truncation')
        env_build.flags.append('-Wno-discarded-qualifiers')

        cmdline_args = [
            "--enable-shared", 
            "--disable-static", 
            "--enable-rpath", 
            "--disable-doc", 
            "--disable-filters", 
            "--disable-hwaccels", 
            "--enable-autodetect", 
            "--disable-jack", 
            "--disable-alsa", 
            "--enable-gpl", 
            "--enable-libopenh264", 
            "--disable-vaapi", 
            "--disable-vdpau", 
            "--disable-bzlib", 
            "--enable-pthreads",
            "--prefix={}".format(self.package_folder)
        ]
        cmdline_args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug']) # debug, courtesy of bincrafters

        with tools.environment_append(env_build.vars), \
             tools.environment_append({'PKG_CONFIG_PATH': self.build_folder}):
            self.run("FFmpeg/configure {}".format(" ".join(cmdline_args)))
            self.run('make -j')
            self.run('make install')

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs.extend(['avcodec', 'avformat'])
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))

    def deploy(self):
        self.copy('*', dst='lib', src='lib')
        self.copy('*', dst='bin', src='bin')
