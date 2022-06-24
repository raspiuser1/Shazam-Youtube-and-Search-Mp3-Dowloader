#mp3 download bot
import os
import youtube_dl
import telepotpro
import shutil
from random import randint
from multiprocessing import Process
from youtubesearchpython import VideosSearch
from youtubesearchpython import Search
from dotenv import load_dotenv
from os.path import join, dirname
from youtube_dl import YoutubeDL
import time
import subprocess
from pathlib import Path
import re
import json
from shazam import *
# from bs4 import BeautifulSoup
# import requests
# from requests_html import HTMLSession

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN")
bot = telepotpro.Bot(TOKEN)

class Music:
    def __init__(self, user_input, msg):
        self.chat = Chat
        self.user_input = user_input[2:]

    def search_music(self, user_input):
        return VideosSearch(user_input, limit = 1).result()

    def get_link(self, result):
        return result['result'][0]['link']

    def get_title(self, result):
        return result['result'][0]['title']

    def get_duration(self, result):
        result = result['result'][0]['duration'].split(':')
        min_duration = int(result[0])
        split_count = len(result)
        
        return min_duration, split_count

    def download_music(self, file_name, link):
        ydl_opts = {
            'outtmpl': './'+file_name,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
            'prefer_ffmpeg': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)

        pass

class Chat:  
    def __init__(self, msg):
        self.chat_id = msg['chat']['id']
        self.user_input = msg['text']
        self.user_input = self.user_input.replace('@TLMusicDownloader_bot', '')
        self.user_name = msg['from']['first_name']
        self.message_id = msg['message_id']
        self.messages = {
            'start':'🤖>====== Download Options ======<🤖\n'
                    '1) Paste youtube links\n'
                    '2) Paste Shazam links\n'
                    '3) Paste spotify link\n'
                    '4) /m [Song name] or [Artist - Song name]\nReturns 1 song\n\n'
                    '🤖>====== Search & Download =====<🤖\n'
                    '/s [-nr] - Search song/artist\n10 results will be displayed if [-nr] not specified\n\n'
                    '/d [nr] - Download Number from searchlist, see /s\n\n'
                    '/list - Show downloaded mp3 songs\n\n'
                    '🤖>========== Settings ==========<🤖\n'
                    '/t - Send mp3 file through telegram (Standard)\n\n'
                    '/c - Save mp3 file to Shared folder\n\n'
                    '/stat - Show status of settings\n\n'
                    '/restart - Restart the bot'
                    ,
            'too_long':'‼️ *Audiofile is longer then 30mins, try again*\n'
        }

        self.check_input(self.user_input, msg)
        pass


    def send_message(self, content):
        return bot.sendMessage(self.chat_id, content, reply_to_message_id=self.message_id, parse_mode='Markdown')

    def delete_message(self, message):
        chat_id = message['chat']['id']
        message_id = message['message_id']
        bot.deleteMessage((chat_id, message_id))

        pass

    def send_audio(self, file_name):
        bot.sendAudio(self.chat_id,audio=open(file_name,'rb'), reply_to_message_id=self.message_id)
        pass

    def escapechar1(self,yturl):
            yturl = yturl.replace("_", " ")
            yturl = yturl.replace("*", "")  
            yturl = yturl.replace("[", "")
            yturl = yturl.replace("|", "")
            yturl = yturl.replace("\\", "")
            yturl = yturl.replace("/", "")
            yturl = yturl.replace(":", "")
            yturl = yturl.replace("#", " ")
            yturl = yturl.replace("'", " ")
            yturl = yturl.replace('"', "")
            yturl = yturl.replace("`", "")
            yturl = yturl.replace("{", "")
            yturl = yturl.replace("}", "")
            yturl = yturl.replace("?", " ")
            yturl = yturl.replace("é", "e")
            yturl = yturl.replace("%", "")
            return yturl    
    
    def escapechar(self,yturl):
            yturl = yturl.replace("_", "\\_")
            yturl = yturl.replace("*", "\\*")  
            yturl = yturl.replace("[", "\\[")
            yturl = yturl.replace("|", "")
            yturl = yturl.replace("`", "\\`")
            return yturl
        
    def process_request(self, user_input):
        if user_input.startswith('/stat'):
            global clubshare,telshare
            with open("clubmount") as f:
                clubmount = f.readline().rstrip()
                if clubmount == "1":
                    clubshare = "on"
                else:
                    clubshare = "off"
            with open("telmount") as f:
                telmount = f.readline().rstrip()
                if telmount == "1":
                    telshare = "on"
                else:
                    telshare = "off"                
            self.send_message(f'Telegram Share = {telshare}\n'
                              f'Sharedfolder = {clubshare}\n')    
            return
        
        
        sh1 = "share"
        mountclub = os.getcwd() + "/" + sh1 + "/"
        
        if user_input.startswith('/list'):
            msg =""
            tel = 1
            # Iterate directory
            for path in os.listdir(mountclub):
                # check if current path is a file
                if os.path.isfile(os.path.join(mountclub, path)):
                    msg += str(tel) + ") " + str(path) + "\n"
                    tel += 1
            self.send_message('=====Downloaded MP3 files=====\n' + msg)
            return
        
        if user_input.startswith('/restart'):
            self.send_message(f"restarting the Bot")
            cmd = subprocess.Popen(f'restart.sh',
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = cmd.communicate()
            
            return
        
        if user_input.startswith('/c'):
            cmd = subprocess.Popen(f'sudo curlftpfs club46:club46@192.168.1.6/sda1/downloads {mountclub}',
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = cmd.communicate()   
            if cmd.returncode == 0 :
                self.send_message('Set downloads to Shared folder')
                with open('clubmount', 'w') as f:
                    f.write('1')
                with open('telmount', 'w') as f:
                    f.write('0')
                return    
            else:
                self.send_message('Unable To mount local folder')
                with open('clubmount', 'w') as f:
                    f.write('0')
                with open('telmount', 'w') as f:
                    f.write('1')                      
                return
        if user_input.startswith('/t'):
            cmd = subprocess.Popen(f'sudo umount {mountclub}',
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = cmd.communicate()   
            if cmd.returncode == 0 :
                self.send_message('Set downloads via Telegram')
                with open('clubmount', 'w') as f:
                    f.write('0')
                with open('telmount', 'w') as f:
                    f.write('1')
                return    
            else:
                self.send_message('Unable To unmount local folder')
                return            
        #check if telegram send or shared send
        with open("clubmount") as f:
            clubmount = f.readline().rstrip()
        with open("telmount") as f:
            telmount = f.readline().rstrip()
            
        if "youtu.be" in user_input or "youtube.com" in user_input:
            httplink = str(re.search("(?P<url>https?://[^\s]+)", user_input).group("url"))
            youtube_dl_opts = {}
            with YoutubeDL(youtube_dl_opts) as ydl:
                  info_dict = ydl.extract_info(httplink, download=False)
                  video_url = info_dict.get("url", None)
                  video_id = info_dict.get("id", None)
                  video_title = info_dict.get('title', None)
                  #print(video_title)
            getlink = httplink
            file_name = video_title + '.mp3'
            
        elif "open.spotify.com" in user_input:
            yturl = ""
            httplink = str(re.search("(?P<url>https?://[^\s]+)", user_input).group("url"))
            print(httplink)
            fol = "/usr/bin/python3 " + os.getcwd() + "/spotify.py " +httplink
            cmd2 = subprocess.Popen(fol,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out1, err = cmd2.communicate()            
            for line in out1.decode().splitlines():
                        print(line)
                        line = line.replace("'", "")
                        #line = line.replace(" ", "")
                        line = line.replace("(", "")
                        line = line.replace(")", "")
                        line1 = line.split(",")
                        name = line1[1]
                        print(name)
                        artist = line1[0]
                        print(artist)
            comp = artist + " - " + name
            self.send_message(str(comp))
            file_name = comp + '.mp3'
            file_name = file_name.replace('"', '')
            result = Music.search_music(self, comp)               
            self.send_message(f"🎵 {Music.get_title(self, result)}\n🔗 {Music.get_link(self, result)}")
            downloading_message = self.send_message('⬇️ Downloading... \n_(this may take a while.)_')
            getlink = Music.get_link(self, result)
            
        elif "shazam.com" in user_input:
            yturl = ""
            httplink = str(re.search("(?P<url>https?://[^\s]+)", user_input).group("url"))
            fol = "/usr/bin/python3 " + os.getcwd() + "/shazam.py " +httplink
            cmd2 = subprocess.Popen(fol,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out1, err = cmd2.communicate()
            for line in out1.decode().splitlines():
                    #print(line)
                    if "youtu" in line:
                        line = line.replace("'", "")
                        #line = line.replace(" ", "")
                        line = line.replace("(", "")
                        line = line.replace(")", "")
                        line1 = line.split(",")
                        yturl = str(line1[0].rstrip("\n"))
                        name = line1[1]
                        print(name)
                        artist = line1[2]
                        print(artist)
                        #escape chars voor telegram
                        yturl2 =yturl
                        yturl = self.escapechar(yturl)
                        break
            if "youtu" in yturl:
                self.send_message(f"Downloading {yturl}")
                getlink = yturl2
                file_name = artist + " - " + name + '.mp3'
                
            else:
                self.send_message('No valid youtube link from Shazam')
                return
            
        #seach multiple sesults
        elif user_input.startswith('/d'):
            if user_input[3:].isnumeric():
                line7 = int(user_input[3:])
                i = 1
                with open("list.txt") as f:
                    for line in f:
                        if i == line7:
                            print("=====Selection=====\n " + line)
                            self.send_message('=====Selection=====\n ' + line)
                            break
                        i+=1
                res4 = line.split("| ID: ")
                getlink = "https://www.youtube.com/watch?v=" + res4[1].rstrip()
                self.send_message(f"Downloading {getlink}")
                tit = res4[0]
                naam3 = self.escapechar1(tit[3:])
                file_name = naam3 + '.mp3'
            else:
                self.send_message(f'No valid number, try again')
                return

                
        elif user_input.startswith('/s'):
            if user_input[-2:].isnumeric() and str(user_input[-3]) == "-" and str(user_input[-4]) == " ":
               max1 = int(user_input[-2:])
            else:
               max1 = 10   
            self.send_message(f'Max {max1} Results will be Displayed')   
            allSearch = Search(user_input[2:-4], limit = max1)
            r = allSearch.result()
            res = json.dumps(r)
            res = json.loads(res)
            res1 = res['result']
            tel = 0
            msg2 = ""
            msg2a = ""
            for item in res1:
                tel += 1
                msg = str(tel) + ") " + item["title"] + " | ID: " + item["id"]
                msg = self.escapechar(msg) + "\n"
                msg2a += msg
                msg2 += msg + "\n"            
            self.send_message(f'🤖>========== Results ==========<🤖\n\n {msg2}')
            with open('list.txt', 'w') as f:
                    f.write(msg2a)
            return
        
        
        
        elif user_input.startswith('/m'):
            #als geen shazam of youtube:
            #installeren als proxie error:
            #pip3 install youtube-search-python
            #
            result = Music.search_music(self, user_input[2:])
            min_duration, split_count = Music.get_duration(self, result)

            if int(min_duration) < 30 and split_count < 3:
                #" - " + str(randint(0,999999))+
                file_name = Music.get_title(self, result) + '.mp3'
                file_name = file_name.replace('"', '')
                self.send_message(f"🎵 {Music.get_title(self, result)}\n🔗 {Music.get_link(self, result)}")
                downloading_message = self.send_message('⬇️ Downloading... \n_(this may take a while.)_')
                getlink = Music.get_link(self, result)
            else:
                self.send_message('Exit: Audio is longer than 30 mins, try again')
                return
        try:
           file_name = file_name.replace('"', "")
        except Exception:
            pass    
        
        if file_name[0] == " ":
            file_name = file_name[1:]
            
        if telmount == "1":
            try:
                downloading_message = self.send_message('⬇️ Downloading to Telegram \n_(this may take a while.)_')
                Music.download_music(self, file_name, getlink)
                self.send_audio(file_name)
                self.delete_message(downloading_message)   
                self.send_message('✅✅✅ Sucessfully downloaded\n' +file_name)
                print ("\nSucces\n")
                time.sleep(2)
                os.remove(file_name)
            except:
                print ("\nError!\n")
                self.send_message('Error')
                
        if clubmount == "1":               
                try:
                    downloading_message = self.send_message('⬇️ Downloading to Shared Folder \n_(this may take a while.)_')
                    Music.download_music(self, sh1 + "/" + file_name, getlink)
                    #print(os.getcwd() + "/" + file_name)
                    print("File copied successfully.")
                    self.delete_message(downloading_message) 
                    self.send_message('✅✅✅ Sucessfully downloaded\n' +file_name)
                 
                # If source and destination are same
                except shutil.SameFileError:
                    print("Source and destination represents the same file.")
                    self.delete_message(downloading_message)
                    self.send_message("Source and destination represents the same file.")
                # If destination is a directory.
                except IsADirectoryError:
                    print("Destination is a directory.")
                    self.delete_message(downloading_message)
                    self.send_message("Destination is a directory.")
                # If there is any permission issue
                except PermissionError:
                    print("Permission denied.")
                    self.delete_message(downloading_message)
                    self.send_message("Permission denied.")
                # For other errors
                except:
                    file4 = mountclub + file_name
                    self.delete_message(downloading_message)
                    if self.checkfileexist(file4):                 
                        print("WARNING: unable to obtain file audio codec with ffprobe, File is copied to folder")
                        self.send_message("WARNING: unable to obtain file audio codec with ffprobe, File is copied to folder")
                    else:
                        print("Error occurred while copying file.")
                        self.send_message("Error occurred while copying file.")        

    def checkfileexist(self,file4):
        if Path(file4).is_file():
            return True
        else:
            return False
        
        
    def check_input(self, user_input, msg):
        #global sendtelegram,sendclub

            
        if user_input.startswith('/start') or user_input.startswith('/help'):
            self.send_message(self.messages['start'])

        elif (user_input.startswith('/') or
              "youtu.be" in user_input or "youtube.com" in user_input
              or "open.spotify.com" in user_input
              or "shazam.com" in user_input):             
            self.process_request(user_input)
 

        # else:
        #     #Invalid command
        #     self.send_message(self.messages['invalid_command'])

        pass 

def start_new_chat(msg):
    Process(target=Chat, args=(msg,)).start()
    

bot.message_loop(start_new_chat, run_forever=True)
