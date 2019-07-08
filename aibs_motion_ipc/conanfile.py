from conans import ConanFile, CMake
import io
import os

class AIBSMotionIPCConan(ConanFile):
    name = 'aibs.motion.ipc'
    description = '2P Motion Correction'
    license = 'Allen Institute Software License'
    url = 'http://johng@stash.corp.alleninstitute.org/scm/om/aibs.motion.ipc.git'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = ['cmake', "virtualenv"]
    build_requires = [
        "CMake/3.12.1@aibs/stable", 
        "Ninja/1.7.2@aibs/stable", 
        "GCC/7.2.0@aibs/stable",
        'mettle/git@aibs/stable',
    ]
    requires = 'blaze/3.5@aibs/stable', 'histogram/3.2@aibs/stable', 'fftw/3.3.8@aibs/stable'

    options = {'aibsio_branch': 'ANY'}
    default_options = { 'aibsio_branch': 'dev' }

    def config_options(self):
        if self.version == 'master':
            self.options.aibsio_branch = 'master'

    def requirements(self):
        self.requires('aibsio/{}@aibs/stable'.format(self.options.aibsio_branch))

    def source(self):
        self.run("git clone http://nileg@stash.corp.alleninstitute.org/scm/om/aibs.motion.ipc.git -b recipeless")
        if self.version != 'dev':
            self.run('cd aibs.motion.ipc; git pull')
        self.run('cd aibs.motion.ipc; git submodule init; git submodule update')

    def build(self):
        cmake = CMake(self, generator="Ninja",  build_type="Debug")
        cmake.configure(build_dir='build', source_dir='../aibs.motion.ipc')
        cmake.build()

    def package(self):
        self.copy("build/bin/aibs.motion.ipc", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.bindirs = ['bin']

    def deploy(self):
        branch = io.StringIO()
        self.run('bin/aibs.motion.ipc --logging.level warn --branch', cwd=self.package_folder, output=branch)
        branch = branch.getvalue().strip()
        aibsio_branch = io.StringIO()
        self.run('bin/aibs.motion.ipc --aibsio_branch', cwd=self.package_folder, output=aibsio_branch)
        aibsio_branch = aibsio_branch.getvalue().strip()
        if not branch or not aibsio_branch:
            self.output.error('Cannot stage without a branch')
        if branch == 'master':
            dst = '/allen/aibs/pipeline/open_modules'
            rpath = '/allen/aibs/pipeline/open_modules/lib64:/usr/lib'
        else:
            dst = os.path.join('/allen/aibs/pipeline/open_modules/stage/aibs.motion.ipc', branch)
            rpath = (
                    '/allen/aibs/pipeline/open_modules/stage/aibsio/{}/lib64:'
                    '/allen/aibs/pipeline/open_modules/lib64:'
                    '/usr/lib'
                    ).format(aibsio_branch)
        self.output.info('deploy executable to {}'.format(dst))
        self.copy('bin/aibs.*', dst=dst)
        self.run('patchelf --force-rpath --set-rpath "{}" {}/bin/aibs.motion.ipc'.format(rpath, dst))

