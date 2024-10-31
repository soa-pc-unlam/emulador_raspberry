FROM ubuntu:22.04
  
ARG DEBIAN_FRONTEND='noninteractive'
 
# se descargan las dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
						  apt-utils \
					      python3 \
						  python3-pip \
						  net-tools \
						  iputils-ping \
						  ssh \
						  openssh-client \ 
&& rm -rf /var/lib/apt/lists/* #se borra la cache de apt para liberar espacio

RUN pip3 install pigpio

#se modifica el archivo sshd_config, para poder acceder por sshs al Docker
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config &&\
    sed -i 's/#PasswordAuthentication/PasswordAuthentication/g' /etc/ssh/sshd_config
 
 
#se establece el password root
RUN echo 'root:1234' | chpasswd

# Abre el puerto 22 para SSH
EXPOSE 22 5022 5000

RUN mkdir /home/server-pigpio
WORKDIR /home/server-pigpio

COPY . /home/server-pigpio

CMD ["python3","GPIOServer.py"]
