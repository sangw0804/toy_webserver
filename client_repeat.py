import socket
import os
import argparse

SERVER_ADDRESS = ('localhost', 8888)
REQUEST = b"""
GET / HTTP/1.1

test
"""

def main(max_clients, max_conns):
  socks = []
  for client_nums in range(max_clients):
    pid = os.fork()
    if pid == 0:
      for conn_nums in range(max_conns):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVER_ADDRESS)
        sock.sendall(REQUEST)
        socks.append(sock)
        print(os.getpid())
      os._exit(0)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Test client for web request',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    '--max-clients',
    type=int,
    default=1,
    help='maximum number of clients'
  )

  parser.add_argument(
    '--max-conns',
    type=int,
    default=1024,
    help='maximum number of connections'
  )

  args = parser.parse_args()
  main(args.max_clients, args.max_conns)