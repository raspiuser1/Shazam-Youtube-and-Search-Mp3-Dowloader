# Shazam, Youtube and search mp3 downloader Telegram bot<br />

Youtube link: https://www.youtube.com/watch?v <br />
[![IMAGE VIDEO](https://img.youtube.com/vi/aOHubhP2/0.jpg)](https://www.youtube.com/watch?v=aOHubh)<br />

Clone this repo and rename the env file to .env and put yout bot token in it<br />
you can get a bot token by talking to the @botfather on telegram <br />

start your bot with  `python3 bot.py` . 
Type `/help` for the menu, you can paste youtube links or share your found shazam with the bot. 
It will search the song on youtube, download it and convert it to an mp3. 
You can also search like `/m michael jackson - beat it`. 

Currently the shared folder `share` is mounted from a networkdrive with an ftpserver running, I used an Usb stick which is in my TP-Link router to do this.
it will store the data onto the USB drive.

If you want a local drive you have to adapt the script.

Check the youtube video for more details. 

