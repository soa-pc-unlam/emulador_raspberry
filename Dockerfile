#Se usa como base a la imagen de desktopcontainers/raspberrypi
FROM desktopcontainers/raspberrypi

# se descargan las dependencias
RUN apt-get -q -y update && \
	apt-get remove qemu-system-arm &&\
    apt-get -q -y install libpixman-1-dev \
                          libglib2.0-dev  \
						  python3 \
						  gcc \
						  python3-tk && \ 
    apt-get -q -y clean 
    

#se instala la ultima version de qemu-system-arm
RUN  wget https://download.qemu.org/qemu-7.1.0.tar.xz &&\
	 tar xvJf qemu-7.1.0.tar.xz &&\
	 cd qemu-7.1.0 &&\
	 ./configure --target-list=arm-softmmu,arm-linux-user --disable-vnc  --enable-gtk &&\
	 Make -j 2 &&\
	 Make install

#se descarga nuestra imagen de Raspbian ya configurada que se encuentra en google drive
RUN cd /images &&\
	rm * &&\
	wget https://drive.google.com/u/0/uc?id=11zHhyjt9Jul9EQBXMCNm0DitNiAvd0lK&export=download&confirm=t&uuid=572f3b37-0848-49a9-a2c5-f921ed6af75 

#se descarga el kernel de la imagen de Raspbian	
RUN cd /home/app &&\
	git clone https://github.com/soaunlam2021/emulador_raspberry.git &&\
	cp imagen_so_raspbian/kernel /

#se establece el password root
RUN echo 'root:1234' | chpasswd

EXPOSE 2222
VOLUME ["/images"]
