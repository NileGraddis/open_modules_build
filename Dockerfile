from ubuntu:18.04

run apt update

run apt install wget -y

run wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
run bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
env PATH=/root/miniconda/bin:$PATH
run conda create --name conan python=3.7 -y
run /bin/bash -c "source activate conan"
run pip install conan

run apt install git -y
run apt install build-essential -y

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/conan.aiconfig.git -b settingsless &&\
    conan config install conan.aiconfig &&\
    conan profile new gcc9 --detect

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/conan.gcc.git &&\
    cd conan.gcc &&\
    conan create . GCC/7.2.0@aibs/stable --profile gcc9

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/conan.ninja.git &&\
    cd conan.ninja &&\
    conan create . Ninja/1.7.2@aibs/stable --profile gcc9

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/conan.cmake.git &&\
    cd conan.cmake &&\
    conan create . CMake/3.12.1@aibs/stable --profile gcc9

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/conan.boost.git -b release/1.67.0 &&\
    cd conan.boost &&\
    conan create . Boost/1.67.0@aibs/stable --profile gcc9

run git clone https://github.com/NileGraddis/open_modules_build

run cd open_modules_build/mettle &&\
    conan create . mettle/git@aibs/stable --profile gcc9

run apt install zlib1g-dev  -y

run cd open_modules_build &&\
    git pull &&\
    cd blackhole &&\
    conan create . Blackhole/1.9.0@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd hdf5 &&\
    conan create . HDF5/1.10.3@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd openblas &&\
    conan create . OpenBLAS/0.3.5@aibs/stable -b missing --profile gcc9


run conan install histogram/3.2@aibs/stable -b missing --profile gcc9
run conan install libcurl/7.61.0@aibs/stable -b missing --profile gcc9
run conan install libpng/1.6.34@aibs/stable -b missing --profile gcc9


run conan install libtiff/4.0.8@aibs/stable -b missing --profile gcc9

    # FFmpeg/3.4.2@aibs/stable:9d7efe5aa51c8e14ef1d260ee2b8e03c8490c568 - Build
    # aibsio/master@aibs/stable:bb719cb5adce1b32a57f4a92b199de5c9540ef90 - Build
    # blaze/3.5@aibs/stable:40f87659cfa99d67368d2224bb20e8707047227c - Build
    # fftw/3.3.8@aibs/stable:ce1e3c2dad4c30d9c16b12dac841836a3f7d8b4a - Build
    # fmt/4.0.0@aibs/stable:27cb7fbffba1a5268eda91c4da54b0254d48c3b1 - Build
    # libunwind/1.2.1@aibs/stable:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Build
    # openh264/1.7.0@aibs/stable:27cb7fbffba1a5268eda91c4da54b0254d48c3b1 - Build


# run cd open_modules_build &&\
#     git pull &&\
#     cd aibs_motion_ipc &&\
#     conan create . aibs.motion.ipc/master@aibs/stable -b missing --profile gcc9