import socket
import json

address = 'localhost'
port = 8081


def handleUpdateRequest(message, obj):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.send(message.encode())
    sock.send(json.dumps(obj).encode())
    sock.close()


def handleAddRequest(message, obj):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.send(message.encode() + json.dumps(obj).encode())
    buf = ''
    reply = sock.recv(1024).decode()
    while reply:
        buf += reply
        reply = sock.recv(1024).decode()
    sock.close()
    if buf:
        buf = json.loads(buf)
        return buf


def handleDeleteRequest(message):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.send(message.encode())
    reply = sock.recv(1024).decode() == 'Done'
    sock.close()
    return reply


def handleGetRequest(message):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.send(message.encode())
    buf = ''
    reply = sock.recv(1024).decode()
    while reply:
        buf += reply
        reply = sock.recv(1024).decode()
    sock.close()
    return json.loads(buf)


def handleFindRequest(message):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.send(message.encode())
    buf = ''
    reply = sock.recv(1024).decode()
    while reply:
        buf += reply
        reply = sock.recv(1024).decode()
    sock.close()
    if buf:
        return json.loads(buf)
