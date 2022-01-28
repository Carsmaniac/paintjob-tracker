import os, configparser, tracker, sys

game = input("Which game? (A/E): ")
if game.lower() == "a":
    game = "ats"
elif game.lower() == "e":
    game = "ets"
else:
    sys.exit()

print("\n"*20)

vehicle_list = os.listdir(tracker.VEHICLE_DIRECTORY+"/"+game)
for i in range(len(vehicle_list)):
    print("{} {}".format(str(i).zfill(3), vehicle_list[i][:-4]))

selection = input("Which vehicle?: ")
# ini = configparser.ConfigParser(allow_no_value = True)
# ini.read("{}/{}/{}".format(tracker.VEHICLE_DIRECTORY, game, vehicle_list[int(selection)]), encoding = "utf-8")

print("\n"*20)

for pack_file in os.listdir(game):
    pack = configparser.ConfigParser(allow_no_value = True)
    pack.read("{}/{}".format(game, pack_file), encoding = "utf-8")
    veh_list = pack["pack info"]["trucks"].split(";") + pack["pack info"]["trailers"].split(";") + pack["pack info"]["truck mods"].split(";") + pack["pack info"]["trailer mods"].split(";")
    if vehicle_list[int(selection)][:-4] in veh_list:
        print(pack_file[:-4])
