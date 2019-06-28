import socket
import time
import os
import signal
import errno

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def signal_handler(signum, frame):
  pid, status = os.wait()
  print(f'Child {pid} terminated with status {status}')


def handle_request(client_connection):
  request = client_connection.recv(1024)
  print(f"Child PID: {os.getpid()}. Parent PID: {os.getppid()}")
  print(request.decode())
  http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
  client_connection.sendall(http_response)
  time.sleep(3)


def serve_forever():
  listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  listen_socket.bind(SERVER_ADDRESS)
  listen_socket.listen(REQUEST_QUEUE_SIZE)
  print(f'Serving HTTP on port {PORT} ...')
  print(f'Parent PID: {os.getpid()}')

  signal.signal(signal.SIGCHLD, signal_handler)

  while True:
    try:
      client_connection, client_address = listen_socket.accept()
    except IOError as e:
      code, msg = e.args
      if code == errno.EINTR:
        continue
      else:
        raise


    pid = os.fork()
    
    if pid == 0:
      listen_socket.close()
      handle_request(client_connection)
      client_connection.close()
      os._exit(0)
    else:
      client_connection.close()

if __name__ == '__main__':
  serve_forever()
