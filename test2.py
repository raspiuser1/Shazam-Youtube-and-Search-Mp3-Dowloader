
# Drive letter: M
# Shared drive path: \\shared\folder
# Username: user123
# Password: password
import subprocess
#apt install samba-common-bin
# Disconnect anything on M
#subprocess.call(r'net use m: /del', shell=True)

# Connect to shared drive, use drive letter M
#subprocess.call(r'net use m: \\DESKTOP-48R8ISU\music\downloads', shell=True)
#subprocess.call(r'sudo mount -t cifs \\\\DESKTOP-48R8ISU\\music /telegram-music-downloader-bot/club46/', shell=True)
subprocess.call(r'curlftpfs club46:club46@192.168.1.6/sda1/downloads/ /telegram-music-downloader-bot/club46/', shell=True)
#subprocess.call(r'sudo umount /telegram-music-downloader-bot/club46/', shell=True)



# sudo apt install curlftpfs