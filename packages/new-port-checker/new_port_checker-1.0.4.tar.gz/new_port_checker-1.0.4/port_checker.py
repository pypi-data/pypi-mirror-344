import socket
import logging
import time
from functools import lru_cache
from typing import Tuple
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import configparser

# 导出公共接口
__all__ = ["is_port_available", "AF_INET", "AF_INET6"]

# 定义地址族常量
AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6

# 全局日志配置，修改为动态设置
logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def is_port_available(
    port: int,
    host: str = "127.0.0.1",
    timeout: float = 2.0,
    max_retries: int = 3,
    protocol: str = "tcp",
    address_family: int = AF_INET,
    total_timeout: float = None,
) -> Tuple[bool, str]:
    start_time = time.time()
    logger = logging.getLogger(__name__)

    # 添加host格式检查
    try:
        socket.getaddrinfo(host, None)
    except socket.gaierror:
        logger.warning("主机地址格式异常: %s", host)

    # 增强型端口验证（包含类型和范围检查）
    if not isinstance(port, int):
        logger.error("端口类型错误: %s (期望int)", type(port).__name__)
        return False, f"端口必须为整数类型，当前类型：{type(port).__name__}"

    if not 1 <= port <= 65535:
        logger.error("端口超出范围: %d (允许范围1-65535)", port)
        return False, f"端口号 {port} 超出有效范围(1-65535)"

    # 协议类型验证
    protocol = protocol.lower()
    if protocol not in ("tcp", "udp"):
        logger.error("不支持的协议类型: %s", protocol)
        return False, f"不支持的协议类型: {protocol}"

    socket_type = socket.SOCK_DGRAM if protocol == "udp" else socket.SOCK_STREAM

    # 分离UDP检测逻辑
    if protocol == "udp":
        for attempt in range(1, max_retries + 1):
            if total_timeout is not None and (time.time() - start_time) > total_timeout:
                return False, "检测超时，已达到总超时时间限制"
            try:
                s = socket.socket(family=address_family, type=socket.SOCK_DGRAM)
                s.settimeout(timeout)
                s.bind((host, port))
                s.close()  # 立即关闭可用端口
                logger.info(f"尝试 {attempt}/{max_retries}: UDP端口 {port} 可用")
                return True, "UDP端口可用"
            except OSError as e:
                # 确保套接字资源释放
                if "s" in locals():
                    s.close()
                logger.warning(
                    f"尝试 {attempt}/{max_retries}: UDP端口 {port} 绑定失败 - {str(e)}"
                )
                if attempt == max_retries:
                    return False, f"UDP {host}:{port} 可能被占用"
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"UDP检测意外错误: {str(e)}")
                return False, f"检测异常: {str(e)}"
        return False, f"UDP检测失败（最大重试次数 {max_retries}）"
    else:
        # 重构TCP检测逻辑
        for attempt in range(1, max_retries + 1):
            if total_timeout is not None and (time.time() - start_time) > total_timeout:
                return False, "检测超时，已达到总超时时间限制"
            try:
                with socket.socket(family=address_family, type=socket_type) as s:
                    s.settimeout(timeout)
                    result = s.connect_ex((host, port))

                    actual_result = (
                        int(result) if isinstance(result, (int, bytes)) else 1
                    )
                    if actual_result == 0:
                        logger.warning(
                            f"尝试 {attempt}/{max_retries}: TCP端口 {port} 已被占用"
                        )
                        return False, f"TCP {host}:{port} 已被占用"

                    # 添加 10035 到允许的错误码中
                    allowed_errors = (1, 111, 10061, 10035)
                    if actual_result not in allowed_errors:
                        error_msg = f"系统错误码: {actual_result}"
                        logger.warning(f"尝试 {attempt}/{max_retries}: {error_msg}")
                        return False, error_msg
                    else:
                        logger.info(f"尝试 {attempt}/{max_retries}: 端口检测通过")

            except socket.timeout as e:
                error_msg = f"连接超时: {str(e)}"
                logger.error(f"尝试 {attempt}/{max_retries}: 检测超时 - {error_msg}")
                # 遇到超时错误，立即返回 False
                return False, error_msg
            except Exception as e:
                error_msg = f"连接错误: {str(e)}"
                logger.error(f"尝试 {attempt}/{max_retries}: 检测错误 - {error_msg}")
                return False, error_msg

        return True, "TCP端口可用"


def is_port_range_available(
    start_port: int,
    end_port: int,
    host: str = "127.0.0.1",
    timeout: float = 2.0,
    max_retries: int = 3,
    protocol: str = "tcp",
    address_family: int = AF_INET,
    total_timeout: float = None,
) -> dict:
    result = {}
    start_time = time.time()
    total_ports = end_port - start_port + 1

    def check_port(port):
        nonlocal start_time
        if total_timeout is not None and (time.time() - start_time) > total_timeout:
            return
        result[port] = is_port_available(
            port, host, timeout, max_retries, protocol, address_family, total_timeout
        )
        # 显示进度
        completed = len(result)
        print(
            f"\r检测进度: {completed}/{total_ports} ({completed/total_ports*100:.2f}%)",
            end="",
            flush=True,
        )

    with ThreadPoolExecutor() as executor:
        try:
            if total_timeout is not None:
                executor.map(
                    check_port, range(start_port, end_port + 1), timeout=total_timeout
                )
            else:
                executor.map(check_port, range(start_port, end_port + 1))
        except TimeoutError:
            pass
    print()  # 换行
    return result


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    default_config = config["default"] if "default" in config else {}

    parser = argparse.ArgumentParser(description="端口可用性检测工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("port", type=int, nargs="?", help="要检测的端口号")
    group.add_argument(
        "--range", nargs=2, type=int, metavar=("START", "END"), help="要检测的端口范围"
    )
    parser.add_argument(
        "--host", default=default_config.get("host", "127.0.0.1"), help="目标主机地址"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(default_config.get("timeout", 2.0)),
        help="单次检测超时时间（秒）",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=int(default_config.get("max_retries", 3)),
        dest="max_retries",
        help="最大重试次数",
    )
    parser.add_argument(
        "--protocol",
        choices=["tcp", "udp"],
        default=default_config.get("protocol", "tcp"),
        help="检测协议类型",
    )
    # 移除重复的 --loglevel 参数添加语句
    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=default_config.get("loglevel", "INFO"),
        help="日志级别",
    )
    parser.add_argument("--ipv6", action="store_true", help="使用IPv6地址协议簇")
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="输出格式，可选 text 或 json",
    )
    parser.add_argument("--total-timeout", type=float, help="总检测超时时间（秒）")
    parser.add_argument("--exclude", type=int, nargs="+", help="要排除检测的端口号")

    args = parser.parse_args()

    # 配置日志级别
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=getattr(logging, args.loglevel),
    )

    if args.port is not None:
        result, message = is_port_available(
            port=args.port,
            host=args.host,
            timeout=args.timeout,
            max_retries=args.max_retries,
            protocol=args.protocol,
            address_family=AF_INET6 if args.ipv6 else AF_INET,
            total_timeout=args.total_timeout,
        )
        if args.output == "text":
            print(f"\n检测结果: {'可用' if result else '不可用'}")
            print(f"状态详情: {message}")
        elif args.output == "json":
            print(
                json.dumps(
                    {"port": args.port, "available": result, "message": message},
                    ensure_ascii=False,
                )
            )
        exit(0 if result else 1)
    else:
        start_port, end_port = args.range
        ports_to_check = [
            port
            for port in range(start_port, end_port + 1)
            if args.exclude is None or port not in args.exclude
        ]
        results = {}
        for port in ports_to_check:
            result = is_port_available(
                port=port,
                host=args.host,
                timeout=args.timeout,
                max_retries=args.max_retries,
                protocol=args.protocol,
                address_family=AF_INET6 if args.ipv6 else AF_INET,
                total_timeout=args.total_timeout,
            )
            results[port] = result

        if args.output == "text":
            print("\n端口范围检测结果:")
            for port, (available, message) in results.items():
                print(f"端口 {port}: {'可用' if available else '不可用'} - {message}")
        elif args.output == "json":
            formatted_results = {
                port: {"available": available, "message": message}
                for port, (available, message) in results.items()
            }
            print(json.dumps(formatted_results, ensure_ascii=False))
        exit(0 if all([res[0] for res in results.values()]) else 1)


if __name__ == "__main__":
    main()


# 配置日志
logging.basicConfig(filename='port_checker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_port(port, protocol, host, result_dict):
    try:
        if protocol.lower() == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol.lower() == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            logging.error(f"不支持的协议: {protocol}")
            print(f"不支持的协议: {protocol}")
            result_dict[port] = False
            return
        
        result = sock.connect_ex((host, port))
        sock.close()
        result_dict[port] = result == 0
        if result_dict[port]:
            logging.info(f"端口 {port} 是开放的")
        else:
            logging.info(f"端口 {port} 是关闭的")
    except Exception as e:
        logging.error(f"检查端口 {port} 时出错: {e}")
        print(f"检查端口 {port} 时出错: {e}")
        result_dict[port] = False

def main():
    parser = argparse.ArgumentParser(description='检查端口可用性')
    parser.add_argument('port', help='要检查的端口或端口范围，例如 80 或 8000-8010')
    parser.add_argument('--protocol', default='tcp', help='协议类型 (tcp 或 udp)')
    parser.add_argument('--host', default='127.0.0.1', help='主机地址')
    args = parser.parse_args()

    try:
        result_dict = {}
        threads = []
        if '-' in args.port:
            start, end = map(int, args.port.split('-'))
            if start > end:
                print("错误：起始端口不能大于结束端口。")
                return
            for port in range(start, end + 1):
                t = threading.Thread(target=check_port, args=(port, args.protocol, args.host, result_dict))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            for port, is_open in result_dict.items():
                if is_open:
                    print(f"端口 {port} 是开放的")
                else:
                    print(f"端口 {port} 是关闭的")
        else:
            port = int(args.port)
            check_port(port, args.protocol, args.host, result_dict)
            if result_dict[port]:
                print(f"端口 {port} 是开放的")
            else:
                print(f"端口 {port} 是关闭的")
    except ValueError:
        print("错误：请输入有效的端口或端口范围。")

if __name__ == '__main__':
    main()
