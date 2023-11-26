#Se usa como base a la imagen de desktopcontainers/raspberrypi
FROM fredblgr/ubuntu-novnc:20.04

# se descargan las dependencias
RUN apt-get -q -y update && \
    apt-get -q -y install qemu-system \
			      unzip \	

#se crean los directorios de descarga
RUN mkdir /root/raspberry &&\
	mkdir /root/raspberry/images &&\
	mkdir /root/raspberry/git
	
#se descarga nuestra imagen de Raspbian ya configurada que se encuentra en google drive
RUN cd /root/raspberry/images &&\
	wget https://drive.google.com/file/d/101SAgE86_e7ws9l-63drSPTruEsCIosF/view?usp=sharing

#se descarga el kernel y el archivo versatile de la imagen de Raspbian	
RUN cd /root/raspberry/git &&\
	git clone https://github.com/soaunlam2021/emulador_raspberry.git &&\
	cp imagen_so_raspbian/kernel-qemu-4.19.50-buster /root/raspberry/images &&\
	cp imagen_so_raspbian/versatile-pb-buster.dtb /root/raspberry/images 


#se establece el password root
RUN echo 'root:1234' | chpasswd

# restablezco parametros del emulador
RUN echo "/etc/init.d/dbus start" >> /root/.bashrc &&\
	echo "rm /tmp/.X1-lock" >> /root/.bashrc &&\
	echo "rm .X11-unix/X1" >> /root/.bashrc &&\
	echo "iniciando Qemu Raspberry.." >> /root/.bashrc 

EXPOSE 2222
VOLUME ["/images"]

#se inicia el emulador el entorno GUI de raspbian ejecutandose en qemu-4
RUN cd /root/raspberry/images &&\
    qemu-system-arm -kernel kernel-qemu-4.19.50-buster -drive \
	                "file=raspbian-buster.qcow,index=0,media=disk,format=qcow2" \
					-append "root=/dev/sda2 panic=1 filesystem=ext4 rw" -cpu arm1176 \
					-m 256 -M versatilepb -dtb versatile-pb-buster.dtb -no-reboot