# Shazam, Spotify, Youtube and mp3 search downloader Telegram bot<br />

Youtube link: https://youtu.be/gY6uuyXsDUs <br />
[![IMAGE VIDEO](https://img.youtube.com/vi/gY6uuyXsDUs/0.jpg)](https://www.youtube.com/watch?v=gY6uuyXsDUs)<br />

Clone this repo and rename the env file to .env and put yout bot token in it<br />
you can get a bot token by talking to the @botfather on telegram <br />

run `pip install -r requirements.txt`

start your bot with  `python3 bot.py` . 
Type `/help` for the menu, you can paste youtube, Spotify links or share your found shazam with the bot. 
It will search the song on youtube, download it and convert it to an mp3. 
You can also search like `/m michael jackson - beat it`. 

Currently the shared folder `share` is mounted from a networkdrive with an ftpserver running, I used an Usb stick which is in my TP-Link router to do this.
it will store the data onto the USB drive.
This line will connecto to the ftp with user & pass = club46:

`cmd = subprocess.Popen(f'sudo curlftpfs club46:club46@192.168.1.6/sda1/downloads {mountclub}',
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)`
                                  
You have to change the login, pass and the local IP if you want to use a shared drive

If you want to use a local drive you will have to change this line: 
`sh1 = "share" ` to whatever you want. like `sh1 = "downloads" ` 
the folder must be in the path of the script. you will have to make it.  

                                 

Check the youtube video for more details. 

