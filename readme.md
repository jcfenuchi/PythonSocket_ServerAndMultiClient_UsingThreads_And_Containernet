
# Introduction:
this code represents an implementation of structured python socket server that uses Threads to handle with more than one client connection both using POO (programing oriented object), and i have deployed this using [Containernet](https://github.com/ramonfontes/containernet) to emulate real communication, containernet is an feature of mininet-wifi to handle with [Docker containers](https://docs.docker.com/); 

# Code Diagram:
![diagram_Imagem](/DOC/diagram_socket_server.png)

# Requeriments
- Docker
- install Mininet_Wifi and Containernet
- requeriments do run makefile
- python

# how run


### Fist run
```bash
make build
make run
```
or 
```bash
make build
sudo python3 main.py
```

### Clear images
```bash
make clear
```

### Helps
```sh
make help
```
