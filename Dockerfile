from ubuntu:18.04

# Blackhole/1.9.0@aibs/stable:9d2b5ee3d2fe0f27bad1042d6b44bc44b7af3cf1 - Missing
# Boost/1.70.0@aibs/stable:24d50bc0f0027f4fee6bfedcf473c52716255602 - Missing
# FFmpeg/3.4.2@aibs/stable:d6d75afde7c4b8bad5669666176d3f76f70e2a76 - Missing
# HDF5/1.10.4@aibs/stable:c315fa4cdecf2499320fcabbd4fdfda4282d90d9 - Missing
# OpenBLAS/0.3.6@aibs/stable:c315fa4cdecf2499320fcabbd4fdfda4282d90d9 - Missing
# aibsio/dev@aibs/stable:5e84c4c3e86bd047aef53eda5ba9b5c50187a1c1 - Missing
# blaze/3.5@aibs/stable:5aac8d601cde31c07ca94f6c371a85441885bf56 - Missing
# fftw/3.3.8@aibs/stable:4969c884ba8ecb7270fe8cfc01994e54d8fc10e9 - Missing
# fmt/4.0.0@aibs/stable:c315fa4cdecf2499320fcabbd4fdfda4282d90d9 - Missing
# histogram/3.2@aibs/stable:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Missing
# jsonformoderncpp/3.4.0@vthiery/stable:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Download
# libcurl/7.61.0@aibs/stable:e801f43e27415e3a4e75088b12fb8f03fe1e7fdf - Missing
# libpng/1.6.34@aibs/stable:4db1be536558d833e52e862fd84d64d75c2b3656 - Missing
# libtiff/4.0.8@aibs/stable:97172bab7554b947975f35cab343b2a755de9955 - Missing
# libunwind/1.2.1@aibs/stable:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Missing
# openh264/1.7.0@aibs/stable:c315fa4cdecf2499320fcabbd4fdfda4282d90d9 - Missing
# pybind11/2.2.2@conan/stable:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Download


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
    cd aibs_motion_ipc &&\
    conan create . aibs.motion.ipc/master@aibs/stable -b missing --profile gcc9