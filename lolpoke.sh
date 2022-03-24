#!/bin/bash

if ! hash catimg 2>/dev/null; then
	echo -e '\033[91mRequired package `catimg` is missing!'
	echo -e '\e[1;37mInstallation instructions:' \
			'\033[4m\u001b[34mhttps://github.com/posva/catimg'
	exit 1
fi

if [ "$1" == '' ]; then
	echo -e '\033[1;31mExample \033[1;37musage\033[1;31m:\n' \
	'  \033[1;37m$ \033[1;31mpokelol \033[1;37mpikachu'
	POKEMON="pikachu"
else
	POKEMON="$1"
fi

CATIMG=$(which catimg)

python -c "from rich.console import Console; Console().rule(f'[#FFCC00]{\"$POKEMON\".upper()}', style='#0075BE')"

paste <(printf %s \
	"$(echo; \
		python /usr/local/bin/lolpoke.py $CATIMG $POKEMON --img)") \
	<(echo; \
		printf %s \
		"$(echo; \
			echo -e "$(python /usr/local/bin/lolpoke.py $CATIMG $POKEMON --print)" \
			| lolcat -f -p 1000)") \
	| tr -d '"'

python -c "from rich.console import Console; Console().rule(f'[#BEBEC1] ◓ ', style='#0075BE')"
