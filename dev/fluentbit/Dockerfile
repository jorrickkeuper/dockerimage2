FROM cloudfoundry/cflinuxfs3:latest

RUN apt remove -y --purge cmake &&\
    hash -r &&\
    apt install -y build-essential libssl-dev &&\
    wget https://github.com/Kitware/CMake/releases/download/v3.20.2/cmake-3.20.2.tar.gz &&\
    tar -zxvf cmake-3.20.2.tar.gz &&\
    cd cmake-3.20.2 &&\
    ./bootstrap &&\
    make &&\
    sudo make install &&\
    cd ../
