#!/bin/bash

export _GROUP=$1               # specify source group ID (without @googlegroups.com)
export DESTINATION_GROUP=$2    # specify destination group email address

#export _RSS_NUM=50            # (optional. See Tips & Tricks.)
#export _WGET_OPTIONS="--load-cookies cookie.txt --keep-session-cookies"
#export _HOOK_FILE=/path/to.sh # (optional. See The Hook.)

#./crawler.sh -sh              # first run for testing
#./crawler.sh -rss > update.sh # using rss feed for updating

download/crawler.sh -sh > download/wget.sh    # save your script
bash download/wget.sh          # downloading mbox files

python upload/upload.py $_GROUP $DESTINATION_GROUP