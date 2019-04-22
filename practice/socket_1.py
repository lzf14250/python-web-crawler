import socket

s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s1.connect(('data.pr4e.org',80))
cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
s1.send(cmd)

outstr = ''

while True:
    data = s1.recv(512)
    if(not len(data)):
        break
    outstr += data.decode()

print(outstr)

s1.close()
