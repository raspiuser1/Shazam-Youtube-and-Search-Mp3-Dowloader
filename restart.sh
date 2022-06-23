ps -ef | grep "python bot.py" | awk '{print $2}' | xargs sudo kill
kill $(pgrep -f 'python3 bot.py')
/usr/bin/python3 bot.py