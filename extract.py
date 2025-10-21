import os
import sys
import shutil
if len(sys.argv) == 3:
    match = open("match.txt", "w")
    match.write(f"Elo >= \"{sys.argv[2]}\"\n")
    match.write(f"WhiteTitle <> \"BOT\"\n")
    match.write(f"BlackTitle <> \"BOT\"")
    match.close()
elif len(sys.argv) > 3:
    match = open("match.txt", "w")
    match.write(f"Elo >= \"{sys.argv[2]}\"\n")
    match.write(f"Elo <= \"{sys.argv[3]}\"\n")
    match.write(f"WhiteTitle <> \"BOT\"\n")
    match.write(f"BlackTitle <> \"BOT\"")
    match.close()
elif len(sys.argv) < 3:
    print("Usage: python3 extract.py input min-elo max-elo")
    sys.exit()
date = sys.argv[1].replace("lichess_db_standard_rated_", "").replace(".pgn.zst", "")
if len(sys.argv) == 3:
    file_name = f"{sys.argv[2]}+ ({date}).pgn"
elif len(sys.argv) > 3:
    file_name = f"{sys.argv[2]}-{sys.argv[3]} ({date}).pgn"
if os.path.isfile(file_name) == False:
    os.system(f"pzstd -dc {sys.argv[1]} | pgn-extract -t match.txt -7 -C -s -o '{file_name}'")
if os.path.getsize(file_name) == 0:
    sys.exit()
if os.path.isdir("supervised-0"):
    shutil.rmtree("supervised-0")
if os.path.isdir("kb1-64x6"):
    shutil.rmtree("kb1-64x6")
os.system(f"trainingdata-tool -chunks-per-file 1 -files-per-dir {sys.maxsize} '{file_name}'")
os.chdir("lczero-training/tf")
os.system(f"python3 train.py --cfg configs/example.yaml --output /Users/me/Downloads/chess-engine/{file_name.split()[0]}.txt")