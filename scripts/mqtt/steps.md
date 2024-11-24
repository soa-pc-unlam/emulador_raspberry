## Configuración para windows con WSL

1- Desde Power Shell

- New-NetFirewallRule -DisplayName "Mosquitto 1883" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
- netsh interface portproxy add v4tov4 listenaddress=192.168.1.44 listenport=1883 connectaddress=127.0.0.1 connectport=1883
- netsh interface portproxy show v4tov4 (Opcional para validar el proxy creado)

2- Crear o editar archivo C/Users/myuser/.wslconfig
Con el siguiente contenido:
```sh
[wsl2]
localhostForwarding=true
```

3- wsl --shutdown y luego wsl

4- Ir al mismo directorio que el docker-compose-yml y ejecutar: 

```sh
docker-compose up -d
```

5- Definir Password

```sh
docker exec -it mosquitto mosquitto_passwd -c mosquitto/passwd_file/password.txt admin
```

6- Test

```sh
mosquitto_sub -h <broker> -p 1883 -t /test/message -v -u "admin" -P "soa2024"
mosquitto_pub -h <broker> -p 1883 -t /test/message -m "hello world" -u "admin" -P "soa2024"
```
<broker>: 
    - localhost si ejecuta dentro de wsl
    - IP de PC local si ejecuta dentro de la LAN