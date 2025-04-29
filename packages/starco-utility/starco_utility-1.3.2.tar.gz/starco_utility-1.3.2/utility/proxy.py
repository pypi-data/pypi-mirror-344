import requests
from concurrent.futures import ThreadPoolExecutor
import ssl
import certifi
import python_socks
from concurrent.futures import as_completed
import urllib.parse


class PROXY:
    def __init__(self, proxy_type: str, ip: str, port: int, username: str = None, password: str = None, timeout=5) -> None:
        '''
            proxy_type:str
            http , socks4 ,socks5
        '''
        if proxy_type not in ['http', 'socks4', 'socks5']:
            raise Exception('wrong proxy_type')
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def make_proxy(self):
        out = {}
        if self.proxy_type == 'http':
            proxy_type = python_socks.ProxyType.HTTP
        elif self.proxy_type == 'socks4':
            proxy_type = python_socks.ProxyType.SOCKS4
        elif self.proxy_type == 'socks5':
            proxy_type = python_socks.ProxyType.SOCKS5
        out['proxy_type'] = proxy_type
        out['addr'] = self.ip
        out['port'] = int(str(self.port))
        if self.username:
            out['username'] = self.username
        if self.password:
            out['password'] = self.password
        return out

    def str_proxy(self):
        out = f"{self.proxy_type}://"
        if self.username and self.password:
            out += f"{self.username}:{self.password}@"
        out += f"{self.ip}:{self.port}"
        return out

    def check(self):
        str_proxy = self.str_proxy()
        print(f"checking {str_proxy}...")
        try:
            p = python_socks.proxy.from_url(str_proxy)

            # `connect` returns standard Python socket in blocking mode
            sock = p.connect(dest_host='check-host.net',
                             dest_port=443, timeout=self.timeout)
            sock = ssl.create_default_context(cafile=certifi.where()).wrap_socket(
                sock=sock,
                server_hostname='check-host.net'
            )

            request = (
                b'GET /ip HTTP/1.1\r\n'
                b'Host: check-host.net\r\n'
                b'Connection: close\r\n\r\n'
            )
            sock.sendall(request)
            response = sock.recv(4096)
            return True
        except Exception as e:
            print(e)
            return False


class ProxyMaker:
    ip: str
    port: int
    username: str = None
    password: str = None
    proxy_type: str = 'socks5'


class ProxyChecker:
    def __init__(self, proxy_list: list[ProxyMaker],  timeout=10, max_threads=10):
        self.proxy_list = proxy_list
        self.timeout = timeout
        self.max_threads = max_threads

    def build_proxy_url(self, proxy: ProxyMaker):
        user = proxy.username
        password = proxy.password
        ip = proxy.ip
        port = proxy.port
        proxy_type = proxy.proxy_type.lower()

        # URL encode username and password if they exist
        if user and password:
            user_encoded = urllib.parse.quote(user)
            password_encoded = urllib.parse.quote(password)
            auth = f"{user_encoded}:{password_encoded}@"
        else:
            auth = ""

        return f"{proxy_type}://{auth}{ip}:{port}"

    def check_proxy(self, proxy: ProxyMaker):
        try:
            print(f"checking {proxy.ip}:{proxy.port}...")
            proxy_url = self.build_proxy_url(proxy)

            proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
            status = False
            proxy_dict = {
                'ip': proxy.ip,
                'port': proxy.port,
                'proxy_type': proxy.proxy_type,
                'username': proxy.username,
                'password': proxy.password
            }
            print(f"proxy_url: {proxy_url}")
            response = requests.get(
                "https://ifconfig.me", proxies=proxies, timeout=self.timeout)
            message = f"[✅] {proxy.ip}:{proxy.port} ➜ IP: {response.text.strip()}"
            status = True
        except Exception as e:
            message = f"[❌] {proxy.ip}:{proxy.port} ➜ {e}"
        out = {
            'status': status,
            'message': message,
            'proxy_str': proxy_url,
            'proxy_dict': proxy_dict

        }
        return out

    def run(self):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            print(f"checking {len(self.proxy_list)} proxies...")
            # Submit all tasks and get future objects
            future_to_proxy = {executor.submit(
                self.check_proxy, proxy): proxy for proxy in self.proxy_list}

            # Collect results as they complete
            for future in as_completed(future_to_proxy):
                result = future.result()
                results.append(result)

        return results
