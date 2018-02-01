#!/bin/bash
echo "bot restarting..."
kill -9 `ps aux | grep -v grep | grep "python3 muhe_bot.py" | awk '{print $2}'`
python3 muhe_bot.py >> bot.log 2>&1&
ps aux | grep -v grep | grep "python3 muhe_bot.py" | awk '{print $2}' > bot.pid
echo "... bot restarted. [OK]"