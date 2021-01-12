#!/bin/bash

BRANCH="main"

start_moniting()
{
    echo "start morniting folder......"
    fswatch -0 -l 5 ./ -e "(.git|.git/*|/.DS_Store)" | while read -d "" event; do sync_files $event ; done
}

sync_files()
{
    echo "start sync_files ${1}"
   	git add . | git commit -m "auto commit : "${1}"" | git fetch origin ${BRANCH} | git rebase origin/${BRANCH} | git push origin ${BRANCH}
}

doOnMac(){
	echo "mac"
	if hash fswatch >/dev/null 2>&1
	then 
		echo "command exist"
	else
		brew install fswatch	
	fi
	start_moniting
}

doOnLinux(){
	echo "linux"
	if hash fswatch >/dev/null 2>&1
	then 
		echo "command exist"
	else
		apt-get install fswatch	
	fi
	start_moniting
}


if [ "$(uname)" == "Darwin" ]
then
	# Mac OS X 操作系统
	doOnMac
elif [ "$(expr substr $(uname -s) 1 5)"=="Linux" ]
then
    # GNU/Linux操作系统
	doOnLinux
elif [ "$(expr substr $(uname -s) 1 10)"=="MINGW32_NT" ]
then
    # Windows NT操作系统
	echo "windows"
fi