import unittest
import socket  # 新增导入
from unittest.mock import MagicMock, patch
from port_checker import is_port_available

class TestPortChecker(unittest.TestCase):
    @patch('socket.socket')
    def test_tcp_port_available(self, mock_socket):
        """测试可用TCP端口"""
        mock_socket.return_value.connect_ex.return_value = 1
        result, msg = is_port_available(5000)
        self.assertTrue(result)
        self.assertIn("TCP端口可用", msg)

    @patch('socket.socket')
    def test_udp_port_in_use(self, mock_socket):
        """测试被占用的UDP端口"""
        mock_socket_instance = mock_socket.return_value
        # 简化超时设置验证
        mock_socket_instance.settimeout.side_effect = None  # 允许settimeout正常调用
        
        # 模拟端口被占用异常
        mock_socket_instance.bind.side_effect = OSError(10048, 'Address already in use')
        
        result, msg = is_port_available(
            5000, 
            protocol='udp',
            timeout=2.0,
            max_retries=1
        )
        
        self.assertFalse(result)
        # 修改断言匹配方式
        self.assertIn("可能被占用", msg)
        
        # 验证套接字参数（使用ANY处理地址族）
        mock_socket.assert_called_once_with(
            family=unittest.mock.ANY,
            type=socket.SOCK_DGRAM
        )
        # 验证超时设置
        mock_socket_instance.settimeout.assert_called_once_with(2.0)

    @patch('socket.socket')
    def test_retry_mechanism(self, mock_socket):
        """测试混合错误场景的重试机制"""
        mock_instances = [MagicMock() for _ in range(3)]
        # 交替模拟超时错误和连接错误
        for i, m in enumerate(mock_instances):
            if i % 2 == 0:
                m.connect_ex.side_effect = socket.timeout("模拟超时")
            else:
                m.connect_ex.return_value = 111  # 连接拒绝错误码
        mock_socket.side_effect = mock_instances

        result, msg = is_port_available(5000, max_retries=3)
        self.assertFalse(result)
        self.assertEqual(mock_socket.call_count, 3)

    @patch('socket.socket')
    def test_tcp_port_in_use(self, mock_socket):
        """测试TCP端口占用场景（单次检测）"""
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 0
        
        result, msg = is_port_available(3306, protocol='tcp')
        self.assertFalse(result)
        self.assertIn("已被占用", msg)

    @patch('socket.socket')
    def test_ipv6_tcp_port(self, mock_socket):
        """测试IPv6 TCP端口检测"""
        mock_socket.return_value.connect_ex.return_value = 1
        result, msg = is_port_available(5000, host='::1', address_family=socket.AF_INET6)
        self.assertTrue(result)
        self.assertIn("TCP端口可用", msg)

    def test_invalid_port_string(self):
        """测试字符串类型的非法端口"""
        result, msg = is_port_available("5000")  # type: ignore
        self.assertFalse(result)
        self.assertIn("整数类型", msg)

if __name__ == '__main__':
    unittest.main()