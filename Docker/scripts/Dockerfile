FROM docker.io/fedora:21
MAINTAINER ggxx120<ggxx120@gmail.com>

RUN yum -y update;\
    yum -y install passwd openssh-server make emacs nano vim git wget gcc gcc-c++ gdb autoconf automake net-tools tar gzip bzip2 qemu tigervnc-server;\
    yum -y install @lxde-desktop;\
    yum -y install firefox;\
    cd /opt && wget https://nodejs.org/dist/v0.10.35/node-v0.10.35-linux-x64.tar.gz;\
    tar xvf node-v0.10.35-linux-x64.tar.gz;\
    ln -s /opt/node-v0.10.35-linux-x64/bin/node /bin/node;\
    ln -s /opt/node-v0.10.35-linux-x64/bin/npm /bin/npm;\
    npm install -g tty.js;\
    yum clean all
RUN cd /opt && git clone git://github.com/kanaka/noVNC
RUN	mkdir /root/.ssh;\
    mkdir /opt/ttyjs;\
    mkdir /root/.vnc

CMD ["/usr/sbin/sshd", "-D"]

ENTRYPOINT ["/usr/bin/bash"]
