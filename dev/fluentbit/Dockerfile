FROM cloudfoundry/cflinuxfs3:latest AS base_build

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

FROM base_build

RUN wget https://github.com/fluent/fluent-bit/archive/refs/tags/v1.9.2.tar.gz
RUN tar -xvf v1.9.2.tar.gz
RUN cd fluent-bit-1.9.2/build/
WORKDIR fluent-bit-1.9.2/build/
RUN cmake ../
RUN make

CMD ["/bin/sh"]