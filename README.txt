
# SWAAG - SanSeb's Worst Ascii-Art Generator
# SWAAG - Swaag's Wasteful Anti-Art Generator
# SWAAG - So, you Want some Automated Arabic Gibberish?



### How to run a sanity check ###
mkdir renders; cd renders
# ../font2png.py 'LiberationMono' n b 114.75 63x126 -3,99    # We never use this anymore.
../charmap2pngs.py ../charmaps/ascii_ext/ascii_ext.txt ../charmaps/ascii_ext/ascii_ext-xfce4_term-LiberationMono_9.png
# Use INVERT=1 for normal images:
../centerOfInk.py *.png
../png2ascii.py 7x14 7,14 ../charmaps/ascii_ext/ascii_ext-xfce4_term-LiberationMono_9.png ./ 0.5

