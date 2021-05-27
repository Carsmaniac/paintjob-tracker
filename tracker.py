import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import configparser
import os

vehicle_directory = "D:/Documents/GitHub/paintjob-packer/library/vehicles"

IMAGE_PAINTJOBS_INCLUDED = "web.site/paintjobs"
IMAGE_TRUCKS_SUPPORTED = "web.site/trucks"
IMAGE_TRAILERS_SUPPORTED = "web.site/trailers"
IMAGE_BUSES_SUPPORTED = "web.site/buses"
IMAGE_RELATED_MODS = "web.site/related"
IMAGE_ENJOY = "web.site/enjoy"
IMAGE_DOWNLOAD = "web.site/download"
IMAGE_DOWNLOAD_SHAREMODS = "web.site/sharemods"
IMAGE_DOWNLOAD_MODSBASE = "web.site/modsbase"
IMAGE_DOWNLOAD_WORKSHOP = "web.site/workshop"
IMAGE_DOWNLOAD_TRUCKY = "web.site/trucky"
BUS_RESOURCES_FORUMs = "bus.stuff/forums"
BUS_RESOURCES_WORKSHOP = "bus.stuff/workshop"
BUS_RESOURCES_TRUCKY = "bus.stuff/trucky"

# make a modland button, plain text but - remove colons from subheadings (bold them), switch sharemods link for modland link
# change plain text to ets2.lt
# also get schmitz s.ko reconstructed
# and make that editing tab
# and a button that just shows the changelog

class DescVars:
    def __init__(self, game_short, mod_name):
        selected_ini = configparser.ConfigParser(allow_no_value = True)
        selected_ini.optionxform = str
        selected_ini.read("{}/{}.ini".format(game_short, mod_name), encoding = "utf-8")

        self.mod_name = mod_name

        self.trucks = []
        for truck in selected_ini["pack info"]["trucks"].split(";"):
            if truck != "":
                self.trucks.append(Vehicle(vehicle_directory, game_short, truck))
        self.truck_mods = []
        for truck_mod in selected_ini["pack info"]["truck mods"].split(";"):
            if truck_mod != "":
                self.truck_mods.append(Vehicle(vehicle_directory, game_short, truck_mod))
        self.trailers = []
        for trailer in selected_ini["pack info"]["trailers"].split(";"):
            if trailer != "":
                self.trailers.append(Vehicle(vehicle_directory, game_short, trailer))
        self.trailer_mods = []
        for trailer_mod in selected_ini["pack info"]["trailer mods"].split(";"):
            if trailer_mod != "":
                self.trailer_mods.append(Vehicle(vehicle_directory, game_short, trailer_mod))
        self.bus_pack = selected_ini["pack info"].getboolean("bus pack")
        self.paintjobs = []
        if selected_ini["pack info"]["paintjobs"] != "":
            self.paintjobs = selected_ini["pack info"]["paintjobs"].split(";")

        self.short_description = selected_ini["description"]["short description"]
        self.more_info = selected_ini["description"]["more info"]

        self.image_header = selected_ini["images"]["header"]
        self.image_showcase = selected_ini["images"]["showcase"]

        self.related_mods = []
        if selected_ini["description"]["related mods"] != "":
            for related_mod in selected_ini["description"]["related mods"].split(";"):
                related_name = related_mod.split("/")[0]
                related_reason = related_mod.split("/")[1]
                related_ini = configparser.ConfigParser(allow_no_value = True)
                related_ini.read("{}/{}.ini".format(game_short, related_name), encoding = "utf-8")
                related_workshop_link = related_ini["links"]["steam workshop"] # [2]
                related_trucky_link = related_ini["links"]["trucky"] # [3]
                related_forums_link = related_ini["links"]["forums"] # [4]
                self.related_mods.append([related_name, related_reason, related_workshop_link, related_trucky_link, related_forums_link])

        self.workshop_link = selected_ini["links"]["steam workshop"]
        self.forums_link = selected_ini["links"]["forums"]
        self.trucky_link = selected_ini["links"]["trucky"]
        self.modland_link = selected_ini["links"]["modland"]
        self.sharemods_link = selected_ini["links"]["sharemods"]
        self.modsbase_link = selected_ini["links"]["modsbase"]

        self.other_game_dict = {"ats":["ets", "Euro Truck Simulator 2"], "ets":["ats", "American Truck Simulator"]}
        self.other_game_short = self.other_game_dict[game_short][0]
        self.other_game = self.other_game_dict[game_short][1]
        if os.path.exists("{}/{}.ini".format(self.other_game_short, mod_name)):
            other_ini = configparser.ConfigParser(allow_no_value = True)
            other_ini.read("{}/{}.ini".format(self.other_game_short, mod_name), encoding = "utf-8")
            self.other_pack = True
            self.other_pack_workshop_link = other_ini["links"]["steam workshop"]
            self.other_pack_trucky_link = other_ini["links"]["trucky"]
            self.other_pack_forums_link = other_ini["links"]["forums"]
        else:
            self.other_pack = False
            self.other_pack_workshop_link = ""
            self.other_pack_trucky_link = ""
            self.other_pack_forums_link = ""

class Vehicle:
    def __init__(self, vehicle_directory, game_short, file_name):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read("{}/{}/{}.ini".format(vehicle_directory, game_short, file_name))
        self.name = config["vehicle info"]["name"]
        self.trailer = config["vehicle info"].getboolean("trailer")
        self.mod = config["vehicle info"].getboolean("mod")
        self.mod_author = config["vehicle info"]["mod author"]
        self.mod_link_workshop = config["vehicle info"]["mod link workshop"]
        self.mod_link_forums = config["vehicle info"]["mod link forums"]
        self.mod_link_author_site = config["vehicle info"]["mod link author site"]
        # self.mod_link_trucky = config["vehicle info"]["mod link trucky"]
        self.mod_link_trucky = ""

    def mod_link(self, _priority):
        priority = list(_priority)
        for i in range(4):
            if priority[i] == "w":
                priority[i] = self.mod_link_workshop
            elif priority[i] == "f":
                priority[i] = self.mod_link_forums
            elif priority[i] == "a":
                priority[i] = self.mod_link_author_site
            elif priority[i] == "t":
                priority[i] = self.mod_link_trucky
        mod_link = None
        for link in priority:
            if link != "" and mod_link == None:
                mod_link = link # only chooses the first non-blank mod link
        return(mod_link)

class TrackerApp:
    def __init__(self, master):
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.variable_game = tk.StringVar(None, "Euro Truck Simulator 2")
        self.variable_game.trace("w", self.update_selectable_mods)
        self.variable_selected_mod = tk.StringVar(None, "")
        # self.variable_directory = tk.StringVar(None, "D:/Documents/Trucksim/Uploading")

        self.panel_mod = ttk.LabelFrame(self.container, text = "Mod Selection")
        self.panel_mod.grid(row = 0, column = 0, sticky = "new", padx = 5, pady = (5, 0))
        # self.panel_package = ttk.LabelFrame(self.container, text = "Package Generator")
        # self.panel_package.grid(row = 1, column = 0, sticky = "ew", padx = 5)
        self.panel_description = ttk.LabelFrame(self.container, text = "Description Generator")
        self.panel_description.grid(row = 2, column = 0, sticky = "sew", padx = 5, pady = (0, 5))

        self.game_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_game, values = ["Euro Truck Simulator 2", "American Truck Simulator"])
        self.game_select.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
        self.mod_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_selected_mod, values = [])
        self.mod_select.grid(row = 0, column = 1, sticky = "ew", padx = (0,5))
        self.panel_mod.columnconfigure(0, weight = 1)
        self.panel_mod.columnconfigure(1, weight = 6)


        self.desc_mod_manager = ttk.Button(self.panel_description, text = "Mod manager", command = lambda : self.mod_manager_description())
        self.desc_mod_manager.grid(row = 0, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_short = ttk.Button(self.panel_description, text = "Short description", command = lambda : self.short_description())
        self.desc_short.grid(row = 1, column = 0, sticky = "news", padx = 5)
        self.desc_workshop = ttk.Button(self.panel_description, text = "Steam Workshop", command = lambda : self.workshop_description())
        self.desc_workshop.grid(row = 2, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_forums = ttk.Button(self.panel_description, text = "SCS Forums", command = lambda : self.forums_description())
        self.desc_forums.grid(row = 3, column = 0, sticky = "news", padx = 5)
        self.desc_trucky = ttk.Button(self.panel_description, text = "Trucky Mod Hub", command = lambda : self.trucky_description())
        self.desc_trucky.grid(row = 4, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_plain_text = ttk.Button(self.panel_description, text = "Plain text", command = lambda : self.plain_text_description())
        self.desc_plain_text.grid(row = 5, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.description_output = tk.Text(self.panel_description)
        self.description_output.grid(row = 0, rowspan = 6, column = 1, sticky = "news", padx = (0,5), pady = 5)
        self.panel_description.columnconfigure(0, weight = 1)
        self.panel_description.columnconfigure(1, weight = 4)

        self.game_short = ""
        self.update_selectable_mods(self)

    def update_selectable_mods(self, *args):
        game_short_dict = {"Euro Truck Simulator 2":"ets", "American Truck Simulator":"ats"}
        self.game_short = game_short_dict[self.variable_game.get()]
        mod_list = []
        for file_name in os.listdir(self.game_short):
            mod_list.append(file_name[:-4])
        self.mod_select.configure(values = mod_list)
        self.variable_selected_mod.set(mod_list[0])

    def sort_vehicles(self, *args):
        print("sort")
        pass

    def save_pack(self, *args):
        print("save")
        pass

    def change_directory(self, *args):
        new_directory = filedialog.askdirectory(title = "Package output", initialdir = self.variable_directory.get())
        if new_directory != "":
            self.variable_directory.set(new_directory)

    def workshop_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "[img]{}[/img]\n".format(desc_vars.image_header)
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "[b]This mod requires my [url={}]bus resource pack[/url] to work![/b]\n\n".format(BUS_RESOURCES_WORKSHOP)
        if desc_vars.other_pack:
            desc += "{} pack available [url={}]here[/url].\n\n".format(desc_vars.other_game, desc_vars.other_pack_workshop_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_PAINTJOBS_INCLUDED)
            for pj in desc_vars.paintjobs:
                desc += pj + "\n"
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "[img]{}[/img]\n".format(IMAGE_BUSES_SUPPORTED)
            for veh in desc_vars.truck_mods:
                desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
            desc += "\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRUCKS_SUPPORTED)
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += veh.name + "\n"
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
                desc += "\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRAILERS_SUPPORTED)
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += veh.name + "\n"
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
                desc += "\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if len(desc_vars.related_mods) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_RELATED_MODS)
            for rel in desc_vars.related_mods:
                desc += "[url={}]{}[/url] - {}\n".format(rel[2], rel[0], rel[1])
            desc += "\n"
        desc += "[img]{}[/img]\n".format(IMAGE_ENJOY)
        desc += "Please don't reupload my mods to other sites. They're already available elsewhere, if you'd like to download them directly. Thanks :)\n\n"
        desc += "You can [url=https://steamcommunity.com/id/carsmaniac/myworkshopfiles/]follow me on the Workshop[/url] to see more!"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def forums_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "[img]{}[/img]\n\n".format(desc_vars.image_showcase)
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "[b]This mod requires my [url={}]bus resource pack[/url] to work![/b]\n\n".format(BUS_RESOURCES_FORUMs)
        if desc_vars.other_pack:
            desc += "{} pack available [url={}]here[/url].\n\n".format(desc_vars.other_game, desc_vars.other_pack_forums_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_PAINTJOBS_INCLUDED)
            for pj in desc_vars.paintjobs:
                desc += pj + "\n"
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "[img]{}[/img]\n".format(IMAGE_BUSES_SUPPORTED)
            desc += "[list]\n"
            for veh in desc_vars.truck_mods:
                desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("fwta"), veh.name)
            desc += "[/list]\n\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRUCKS_SUPPORTED)
                desc += "[list]\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "[*]{}\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("fwta"), veh.name)
                desc += "[/list]\n\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRAILERS_SUPPORTED)
                desc += "[list]\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "[*]{}\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("fwta"), veh.name)
                desc += "[/list]\n\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if len(desc_vars.related_mods) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_RELATED_MODS)
            desc += "[list]\n"
            for rel in desc_vars.related_mods:
                desc += "[*][url={}]{}[/url] - {}\n".format(rel[4], rel[0], rel[1])
            desc += "[/list]\n\n"
        desc += "[img]{}[/img]\n".format(IMAGE_DOWNLOAD)
        desc += "[url={}][img]{}[/img][/url] [url={}][img]{}[/img][/url] [url={}][img]{}[/img][/url] [url={}][img]{}[/img][/url]\n".format(desc_vars.sharemods_link, IMAGE_DOWNLOAD_SHAREMODS, desc_vars.modsbase_link, IMAGE_DOWNLOAD_MODSBASE, desc_vars.workshop_link, IMAGE_DOWNLOAD_WORKSHOP, desc_vars.trucky_link, IMAGE_DOWNLOAD_TRUCKY)
        desc += "[size=85]Please don't reupload my mods. Thanks :)[/size]"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def trucky_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "<div style=\"max-width: 650px\"> <!-- Cars was here ;) -->\n"
        desc += "    <img src=\"{}\" style=\"padding-bottom: 5px\">\n".format(desc_vars.image_header)
        desc += "    <p>{}</p>\n".format(desc_vars.short_description)
        if desc_vars.bus_pack:
            desc += "    <p style=\"font-weight: 700\">This mod requires my <a style=\"color: white; text-decoration: underline\" href=\"{}\">bus resource pack</a>to work!</p>\n".format(BUS_RESOURCES_TRUCKY)
        if desc_vars.other_pack:
            desc += "    <p>{} pack available <a style=\"color: white; text-decoration: underline\" href=\"{}\">here</a>.</p>\n".format(desc_vars.other_game, desc_vars.other_pack_trucky_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Paintjobs included</p>\n"
            desc += "    <ul style=\"list-style: none; padding-left: 15px\">\n"
            for pj in desc_vars.paintjobs:
                desc += "        <li>{}</li>\n".format(pj)
            desc += "    </ul>\n"
        if desc_vars.bus_pack:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Buses supported</p>\n"
            desc += "    <ul>\n"
            for veh in desc_vars.truck_mods:
                desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
            desc += "    </ul>\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Trucks supported</p>\n"
                desc += "    <ul>\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "        <li>{}</li>\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
                desc += "    </ul>\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Trailers supported</p>\n"
                desc += "    <ul>\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "        <li>{}</li>\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
                desc += "    </ul>\n"
        if desc_vars.more_info != "":
            desc += "    <p>{}</p>".format(desc_vars.more_info)
        if len(desc_vars.related_mods) >= 1:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Related mods</p>\n"
            desc += "    <ul>\n"
            for rel in desc_vars.related_mods:
                desc += "        <li><a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a> - {}</li>\n".format(rel[3], rel[0], rel[1])
            desc += "    </ul>\n"
        desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Enjoy! :)</p>\n"
        desc += "</div>" + desc_vars.forums_link # For copy-pasting into the forum URL field
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def plain_text_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += ">> This mod requires my bus resource pack to work! <<\n"
            desc += "Download it here: {}\n\n".format(BUS_RESOURCES_FORUMs)
        if len(desc_vars.paintjobs) >= 1:
            desc += "Paintjobs included:\n"
            for pj in desc_vars.paintjobs:
                desc += "- {}\n".format(pj)
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "Buses supported:\n"
            for veh in desc_vars.truck_mods:
                desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
            desc += "\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "Trucks supported:\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "- {}\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
                desc += "\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "Trailers supported:\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "- {}\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
                desc += "\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if desc_vars.other_pack:
            desc += "I've also made a pack for {}: {}\n".format(desc_vars.other_game, desc_vars.other_pack_forums_link)
        desc += "Please don't reupload my mods to other sites. Thanks, and enjoy! :)"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def short_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "A pack of {} paintjobs supporting ".format(desc_vars.mod_name.replace(" Paintjob Pack", ""))
        if desc_vars.bus_pack:
            desc += "{} buses".format(len(desc_vars.truck_mods))
        else:
            total_trucks = len(desc_vars.trucks) + len(desc_vars.truck_mods)
            total_trailers = len(desc_vars.trailers) + len(desc_vars.trailer_mods)
            if total_trucks >= 1 and total_trailers >= 1:
                desc += "{} trucks and {} trailers".format(total_trucks, total_trailers)
            elif total_trucks >= 1:
                desc += "{} trucks".format(total_trucks)
            elif total_trailers >= 1:
                desc += "{} trailers".format(total_trailers)
        if len(desc_vars.paintjobs) >= 1:
            desc += ", with {} different paintjobs".format(len(desc_vars.paintjobs))
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def mod_manager_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "This mod requires my bus resource pack to work!\n\n"
        if desc_vars.other_pack:
            desc += "{} pack also available\n\n".format(desc_vars.other_game)
        if len(desc_vars.paintjobs) >= 1:
            desc += "Paintjobs included:\n"
            for pj in desc_vars.paintjobs:
                desc += "- {}\n".format(pj)
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "Buses supported:\n"
            for veh in desc_vars.truck_mods:
                desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
            desc += "\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "Trucks supported:\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "- {}\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
                desc += "\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "Trailers supported:\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "- {}\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "- {}'s {}\n".format(veh.mod_author, veh.name)
                desc += "\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        desc += "Please don't reupload my mods. Thanks, and enjoy! :)\n"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    # def copy_description(self, *args):
    #     pass

def main():
    root = tk.Tk()
    root.title("Paintjob Tracker")
    root.resizable(False, False)
    tracker = TrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
