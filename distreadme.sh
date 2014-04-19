#ª/bin/bash
cat README.md | grep -v '^!' |  pandoc  -f markdown -t rst -o README.txt
