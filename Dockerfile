FROM archlinux:latest

RUN pacman -Syu --noconfirm base-devel
RUN useradd -ms /bin/bash user
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
COPY --chown=user:user . /informant/src/informant-0.6.0
COPY --chown=user:user ./test /informant
WORKDIR /informant
USER user
ENV SRCDEST=src
#CMD ["makepkg", "-rsi", "--noconfirm"]

