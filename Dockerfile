from ubuntu:18.04

run apt-get update

run apt-get install wget -y

run wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
run bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
env PATH=/root/miniconda/bin:$PATH
run conda create --name conan python=3.7 -y
run /bin/bash -c "source activate conan"
run pip install conan

run apt-get install git -y
run apt-get install build-essential -y

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

run apt-get install zlib1g-dev  -y

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

run cd open_modules_build &&\
    git pull &&\
    cd libtiff &&\
    conan create . libtiff/4.0.8@aibs/stable -b missing --profile gcc9

run conan install libunwind/1.2.1@aibs/stable -b missing --profile gcc9
run conan install blaze/3.5@aibs/stable -b missing --profile gcc9
run conan install openh264/1.7.0@aibs/stable -b missing --profile gcc9

run apt-get install pkg-config -y
run conan install FFmpeg/3.4.2@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd fftw &&\
    conan create . fftw/3.3.8@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd fmtlib &&\
    conan create . fmt/4.0.0@aibs/stable -b missing --profile gcc9

run conan install Eigen3/3.3.4@aibs/stable -b missing --profile gcc9
run conan install xtensor/0.19.4@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd opencv &&\
    conan create . OpenCV/4.0.0@aibs/stable -b missing --profile gcc9

# aibsio/master@aibs/stable:bb719cb5adce1b32a57f4a92b199de5c9540ef90 - Build

run git clone http://nileg@stash.corp.alleninstitute.org/scm/om/aibsio.git -b om_master_http &&\
    cd aibsio &&\
    conan create . aibsio/om_master_http@aibs/stable -b missing --profile gcc9

run cd open_modules_build &&\
    git pull &&\
    cd aibs_motion_ipc &&\
    conan create . aibs.motion.ipc/master@aibs/stable -b missing --profile gcc9 -o aibsio_branch=om_master_http

# run cd open_modules_build &&\
#     git pull &&\
#     cd aibs_motion_ipc &&\
#     mkdir build &&\
#     cd build &&\
#     conan install .. -b missing --profile gcc9 -o aibsio_branch=master &&\
#     cd .. &&\
#     git clone http://nileg@stash.corp.alleninstitute.org/scm/om/aibs.motion.ipc.git -b master &&\
#     cd aibs.motion.ipc &&\
#     git submodule init &&\
#     git submodule update &&\
#     cd ../build &&\
#     /bin/bash -c "source activate.sh && cmake ../aibs.motion.ipc -G Ninja && ninja"
    
    # conan create . aibs.motion.ipc/master@aibs/stable -b missing --profile gcc9