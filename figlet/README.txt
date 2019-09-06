( for f in $(cd figlet-fonts; ls *.flf); do echo ${f%.flf}; echo sanseb | figlet -f $f -d figlet-fonts/ -w999 ;  done ) > sanseb.ascii

echo 'sanseb' | figlet -f fraktur -d figlet-fonts/

