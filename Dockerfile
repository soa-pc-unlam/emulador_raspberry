# Usa una imagen base oficial de Ubuntu
FROM ubuntu:latest

# Instala los paquetes necesarios
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Cambia la contraseña del root (opcional, puedes cambiarla)
RUN echo 'root:root' | chpasswd

# Permite la autenticación por clave pública para el root (opcional)
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# No permita que Docker mate procesos que usen el PID 1
RUN sed -i 's/#UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Abre el puerto 22 para SSH
EXPOSE 22 5000

# Inicia el servidor SSH cuando el contenedor se ejecute
CMD ["/usr/sbin/sshd", "-D"]
