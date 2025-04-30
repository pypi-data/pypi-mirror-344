import unittest
from unittest.mock import patch
import sys
import os

# 将项目目录添加到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from port_checker import check_port, main

class TestPortChecker(unittest.TestCase):
    @patch('socket.socket')
    def test_tcp_port_open(self, mock_socket):
        mock_connect = mock_socket.return_value.connect_ex
        mock_connect.return_value = 0
        result = check_port(80, 'tcp', '127.0.0.1')
        self.assertEqual(result, True)

    @patch('socket.socket')
    def test_tcp_port_closed(self, mock_socket):
        mock_connect = mock_socket.return_value.connect_ex
        mock_connect.return_value = 1
        result = check_port(80, 'tcp', '127.0.0.1')
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()