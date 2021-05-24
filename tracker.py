import tkinter as tk
from tkinter import ttk, filedialog
import configparser, os

vehicle_directory = "D:/Documents/GitHub/paintjob-packer/library/vehicles"

image_paintjobs_included = "web.site/paintjobs"
image_trucks_supported = "web.site/trucks"
image_trailers_supported = "web.site/trailers"
image_buses_supported = "web.site/buses"
image_related_mods = "web.site/related"
image_enjoy = "web.site/enjoy"
image_download_sharemods = "web.site/sharemods"
image_download_workshop = "web.site/workshop"
image_download_trucky = "web.site/trucky"
bus_resources_forums = "bus.stuff/forums"
bus_resources_workshop = "bus.stuff/workshop"
bus_resources_trucky = "bus.stuff/trucky"

class DescVars:
    def __init__(self, game_short, mod_name):
        selected_ini = configparser.ConfigParser(allow_no_value = True)
        selected_ini.read("{}/{}.ini".format(game_short, mod_name), encoding = "utf-8")

        self.mod_name = mod_name

        self.trucks = []
        for truck in selected_ini["Pack Info"]["trucks"].split(";"):
            self.trucks.append(Vehicle(vehicle_directory, game_short, truck))
        self.truck_mods = []
        for truck_mod in selected_ini["Pack Info"]["truck mods"].split(";"):
            self.truck_mods.append(Vehicle(vehicle_directory, game_short, truck_mod.split("~")[0]))
        self.trailers = []
        for trailer in selected_ini["Pack Info"]["trailers"].split(";"):
            self.trailers.append(Vehicle(vehicle_directory, game_short, trailer))
        self.trailer_mods = []
        for trailer_mod in selected_ini["Pack Info"]["trailer mods"].split(";"):
            self.trailer_mods.append(Vehicle(vehicle_directory, game_short, trailer_mod.split("~")[0]))
        self.bus_pack = selected_ini["Pack Info"].getboolean("bus pack")
        self.paintjobs = []
        if selected_ini["Pack Info"]["paintjobs"] != "":
            self.paintjobs = selected_ini["Pack Info"]["paintjobs"].split(";")

        self.short_description = selected_ini["Description"]["short description"]
        self.more_info = selected_ini["Description"]["more info"]
        self.header_image_link = selected_ini["Description"]["header image link"]
        self.forums_screenshot_image_link = selected_ini["Description"]["forums screenshot image link"]

        self.related_mods = []
        if selected_ini["Description"]["related mods"] != "":
            for related_mod in selected_ini["Description"]["related mods"].split(";"):
                related_name = related_mod.split("~")[0]
                related_reason = related_mod.split("~")[1]
                related_ini = configparser.ConfigParser(allow_no_value = True)
                related_ini.read("{}/{}.ini".format(game_short, related_name), encoding = "utf-8")
                related_workshop_link = related_ini["Links"]["steam workshop"] # [2]
                related_trucky_link = related_ini["Links"]["trucky"] # [3]
                related_forums_link = related_ini["Links"]["forums"] # [4]
                self.related_mods.append([related_name, related_reason, related_workshop_link, related_trucky_link, related_forums_link])

        self.workshop_link = selected_ini["Links"]["steam workshop"]
        self.trucky_link = selected_ini["Links"]["trucky"]
        self.sharemods_link = selected_ini["Links"]["sharemods"]

        self.other_game_dict = {"ats":["ets", "Euro Truck Simulator 2"], "ets":["ats", "American Truck Simulator"]}
        self.other_game_short = self.other_game_dict[game_short][0]
        self.other_game = self.other_game_dict[game_short][1]
        if os.path.exists("{}/{}.ini".format(self.other_game_short, mod_name)):
            other_ini = configparser.ConfigParser(allow_no_value = True)
            other_ini.read("{}/{}.ini".format(self.other_game_short, mod_name), encoding = "utf-8")
            self.other_pack = True
            self.other_pack_workshop_link = other_ini["Links"]["steam workshop"]
            self.other_pack_trucky_link = other_ini["Links"]["trucky"]
            self.other_pack_forums_link = other_ini["Links"]["forums"]
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
        self.mod_link = config["vehicle info"]["mod link"]

class TrackerApp:
    def __init__(self, master):
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.variable_game = tk.StringVar(None, "Euro Truck Simulator 2")
        self.variable_game.trace("w", self.update_selectable_mods)
        self.variable_selected_mod = tk.StringVar(None, "")
        self.variable_directory = tk.StringVar(None, "D:/Documents/Trucksim/Uploading")

        self.panel_mod = ttk.LabelFrame(self.container, text = "Mod Selection")
        self.panel_mod.grid(row = 0, column = 0, sticky = "new", padx = 5, pady = (5, 0))
        self.panel_package = ttk.LabelFrame(self.container, text = "Package Generator")
        self.panel_package.grid(row = 1, column = 0, sticky = "ew", padx = 5)
        self.panel_description = ttk.LabelFrame(self.container, text = "Description Generator")
        self.panel_description.grid(row = 2, column = 0, sticky = "sew", padx = 5, pady = (0, 5))

        self.game_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_game, values = ["Euro Truck Simulator 2", "American Truck Simulator"])
        self.game_select.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
        self.mod_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_selected_mod, values = [])
        self.mod_select.grid(row = 0, column = 1, sticky = "ew", padx = (0,5))
        self.panel_mod.columnconfigure(0, weight = 1)
        self.panel_mod.columnconfigure(1, weight = 6)

        self.current_directory = ttk.Label(self.panel_package, textvariable = self.variable_directory)
        self.current_directory.grid(row = 0, column = 0, columnspan = 3, sticky = "new", padx = 5, pady = (5, 0))
        self.directory_changer = ttk.Button(self.panel_package, text = "Change directory", command = lambda : self.change_directory())
        self.directory_changer.grid(row = 1, column = 0, sticky = "we", padx = (5, 0))
        self.workshop_generator = ttk.Button(self.panel_package, text = "Generate Workshop package", command = lambda : self.generate_workshop())
        self.workshop_generator.grid(row = 1, column = 1, sticky = "we", padx = 5)
        self.standalone_generator = ttk.Button(self.panel_package, text = "Generate standalone package", command = lambda : self.generate_standalone())
        self.standalone_generator.grid(row = 1, column = 2, sticky = "we", padx = (0, 5), pady = 5)
        self.panel_package.columnconfigure(0, weight = 1)
        self.panel_package.columnconfigure(1, weight = 1)
        self.panel_package.columnconfigure(2, weight = 1)

        self.desc_workshop = ttk.Button(self.panel_description, text = "Steam Workshop", command = lambda : self.workshop_description())
        self.desc_workshop.grid(row = 0, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_forums = ttk.Button(self.panel_description, text = "SCS Forums", command = lambda : self.forums_description())
        self.desc_forums.grid(row = 1, column = 0, sticky = "news", padx = 5)
        self.desc_trucky = ttk.Button(self.panel_description, text = "Trucky Mods", command = lambda : self.trucky_description())
        self.desc_trucky.grid(row = 2, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_plain_text = ttk.Button(self.panel_description, text = "Plain text", command = lambda : self.plain_text_description())
        self.desc_plain_text.grid(row = 3, column = 0, sticky = "news", padx = 5)
        self.desc_short = ttk.Button(self.panel_description, text = "Short description", command = lambda : self.short_description())
        self.desc_short.grid(row = 4, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_mod_manager = ttk.Button(self.panel_description, text = "Mod manager", command = lambda : self.copy_description())
        self.desc_mod_manager.grid(row = 5, column = 0, sticky = "news", padx = 5)
        self.description_copier = ttk.Button(self.panel_description, text = "Copy to clipboard", command = lambda : self.copy_description())
        self.description_copier.grid(row = 6, column = 0, sticky = "news", padx = 5, pady = 5)
        self.description_output = tk.Text(self.panel_description)
        self.description_output.grid(row = 0, rowspan = 7, column = 1, sticky = "news", padx = (0,5), pady = 5)
        self.panel_description.columnconfigure(0, weight = 1)
        self.panel_description.columnconfigure(1, weight = 4)

        self.game_short = ""
        self.update_selectable_mods(self)

    def update_selectable_mods(self, *args):
        if self.variable_game.get() == "Euro Truck Simulator 2":
            mod_list = ["Very Long Company Name Inc Paintjob Pack", "ets2"]
            self.mod_select.configure(values = mod_list)
            self.variable_selected_mod.set(mod_list[0])
            self.game_short = "ets"
        else:
            mod_list = ["Wowzer Paintjob Pack", "ats2"]
            self.mod_select.configure(values = mod_list)
            self.variable_selected_mod.set(mod_list[0])
            self.game_short = "ats"

    def change_directory(self, *args):
        new_directory = filedialog.askdirectory(title = "Package output", initialdir = self.variable_directory.get())
        if new_directory != "":
            self.variable_directory.set(new_directory)

    def generate_workshop(self, *args):
        pass

    def generate_standalone(self, *args):
        pass

    def workshop_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "[img]{}[/img]\n".format(desc_vars.header_image_link)
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "[b]This mod requires my [url={}]shared bus resources[/url] to work![/b]\n\n".format(bus_resources_workshop)
        if desc_vars.other_pack:
            desc += "{} pack available [url={}]here[/url].\n\n".format(desc_vars.other_game, desc_vars.other_pack_workshop_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "[img]{}[/img]\n".format(image_paintjobs_included)
            for pj in desc_vars.paintjobs:
                desc += pj + "\n"
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "[img]{}[/img]\n".format(image_buses_supported)
            for veh in desc_vars.truck_mods:
                desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
            desc += "\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "[img]{}[/img]\n".format(image_trucks_supported)
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += veh.name + "\n"
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
                desc += "\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "[img]{}[/img]\n".format(image_trailers_supported)
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += veh.name + "\n"
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
                desc += "\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if len(desc_vars.related_mods) >= 1:
            desc += "[img]{}[/img]\n".format(image_related_mods)
            for rel in desc_vars.related_mods:
                desc += "[url={}]{}[/url] - {}\n".format(rel[2], rel[0], rel[1])
            desc += "\n"
        desc += "[img]{}[/img]\n".format(image_enjoy)
        desc += "Please don't reupload my mods to other sites. They're already available elsewhere, if you'd like to download them directly. Thanks :)\n\n"
        desc += "You can [url=https://steamcommunity.com/id/carsmaniac/myworkshopfiles/]follow me on the Workshop[/url] to see more!"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def forums_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "[color=#FFFFFF][size=200]{}[/size][/color]\n\n".format(desc_vars.mod_name)
        desc += "[img]{}[/img]\n\n".format(desc_vars.forums_screenshot_image_link)
        desc += "[img]{}[/img]\n".format(desc_vars.header_image_link)
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "[b]This mod requires my [url={}]shared bus resources[/url] to work![/b]\n\n".format(bus_resources_forums)
        if desc_vars.other_pack:
            desc += "{} pack available [url={}]here[/url].\n\n".format(desc_vars.other_game, desc_vars.other_pack_forums_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "[img]{}[/img]\n".format(image_paintjobs_included)
            for pj in desc_vars.paintjobs:
                desc += pj + "\n"
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "[img]{}[/img]\n".format(image_buses_supported)
            desc += "[list]\n"
            for veh in desc_vars.truck_mods:
                desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
            desc += "[/list]\n\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "[img]{}[/img]\n".format(image_trucks_supported)
                desc += "[list]\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "[*]{}\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
                desc += "[/list]\n\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "[img]{}[/img]\n".format(image_trailers_supported)
                desc += "[list]\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "[*]{}\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "[*]{}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link, veh.name)
                desc += "[/list]\n\n"
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if len(desc_vars.related_mods) >= 1:
            desc += "[img]{}[/img]\n".format(image_related_mods)
            desc += "[list]\n"
            for rel in desc_vars.related_mods:
                desc += "[*][url={}]{}[/url] - {}\n".format(rel[4], rel[0], rel[1])
            desc += "[/list]\n\n"
        desc += "[url={}][img]{}[/img][/url] [url={}][img]{}[/img][/url] [url={}][img]{}[/img][/url]\n".format(desc_vars.sharemods_link, image_download_sharemods, desc_vars.workshop_link, image_download_workshop, desc_vars.trucky_link, image_download_trucky)
        desc += "[size=85]Please don't reupload my mods. Thanks :)[/size]"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def trucky_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "<div style=\"max-width: 650px\">\n"
        desc += "    <img src=\"{}\" style=\"padding-bottom: 5px\">\n".format(desc_vars.header_image_link)
        desc += "    <p>{}</p>\n".format(desc_vars.short_description)
        if desc_vars.bus_pack:
            desc += "    <p style=\"font-weight: 700\">This mod requires my <a style=\"color: white; text-decoration: underline\" href=\"{}\">shared bus resources</a>to work!</p>\n".format(bus_resources_trucky)
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
                desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link, veh.name)
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
                        desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link, veh.name)
                desc += "    </ul>\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Trailers supported</p>\n"
                desc += "    <ul>\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "        <li>{}</li>\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "        <li>{}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link, veh.name)
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
        desc += "</div>"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def plain_text_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += ">> This mod REQUIRES my shared bus resources to work! <<\n"
            desc += "Download it here: {}\n\n".format(bus_resources_forums)
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
            desc += "I've also made a pack for {}: {}".format(desc_vars.other_game, desc_vars.other_pack_sharemods_link)
        desc += "Please don't reupload my mods to other sites. Thanks, and enjoy! :)"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def short_description(self, *args):
        pass

    def mod_manager_description(self, *args):
        pass

    def copy_description(self, *args):
        pass

def main():
    root = tk.Tk()
    root.title("Paintjob Tracker")
    root.resizable(False, False)
    tracker = TrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
