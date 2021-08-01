import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import configparser
import os
import time

VEHICLE_DIRECTORY = "C:/Users/Carsmaniac/Documents/GitHub/paintjob-packer/library/vehicles"

IMAGE_PAINTJOBS_INCLUDED = "https://i.imgur.com/evSjSpv.png"
IMAGE_TRUCKS_SUPPORTED = "https://i.imgur.com/EjcBoVh.png"
IMAGE_TRAILERS_SUPPORTED = "https://i.imgur.com/MzOsazO.png"
IMAGE_BUSES_SUPPORTED = "https://i.imgur.com/lbD4wqg.png"
IMAGE_RELATED_MODS = "https://i.imgur.com/a7RJfN6.png"
IMAGE_ENJOY = "https://i.imgur.com/Q1RxPRv.png"
IMAGE_DOWNLOAD = "https://i.imgur.com/Bn5nY69.png"

BUS_RESOURCES_FORUMS = "bus.stuff/forums"
BUS_RESOURCES_WORKSHOP = "bus.stuff/workshop"
BUS_RESOURCES_TRUCKY = "bus.stuff/trucky"
BUS_RESOURCES_MODLAND = "bus.stuff/modland"

MOD_LINK_PAGE = "https://github.com/Carsmaniac/paintjob-packer/blob/master/library/mod%20links.md"
BUY_ME_A_COFFEE = "https://www.buymeacoffee.com/carsmaniac"

class DescVars:
    def __init__(self, game_short, mod_name, link_formatting="none"):
        selected_ini = configparser.ConfigParser(allow_no_value = True)
        selected_ini.optionxform = str
        selected_ini.read("{}/{}.ini".format(game_short, mod_name), encoding = "utf-8")

        self.mod_name = mod_name

        self.trucks = []
        for truck in selected_ini["pack info"]["trucks"].split(";"):
            if truck != "":
                self.trucks.append(Vehicle(VEHICLE_DIRECTORY, game_short, truck))
        self.truck_mods = []
        for truck_mod in selected_ini["pack info"]["truck mods"].split(";"):
            if truck_mod != "":
                self.truck_mods.append(Vehicle(VEHICLE_DIRECTORY, game_short, truck_mod))
        self.trailers = []
        for trailer in selected_ini["pack info"]["trailers"].split(";"):
            if trailer != "":
                self.trailers.append(Vehicle(VEHICLE_DIRECTORY, game_short, trailer))
        self.trailer_mods = []
        for trailer_mod in selected_ini["pack info"]["trailer mods"].split(";"):
            if trailer_mod != "":
                self.trailer_mods.append(Vehicle(VEHICLE_DIRECTORY, game_short, trailer_mod))
        self.bus_pack = selected_ini["pack info"].getboolean("bus pack")
        self.paintjobs = []
        if selected_ini["pack info"]["paintjobs"] != "":
            self.paintjobs = selected_ini["pack info"]["paintjobs"].split(";")
        self.checklist_stage = int(selected_ini["pack info"]["checklist stage"])

        self.short_description = selected_ini["description"]["short description"].replace("\\n","\n") # configparser escapes \n, so we need to un-escape it
        self.short_description = format_links(self, self.short_description, link_formatting) # converts markdown links to html or bbcode, or removes them
        self.more_info = selected_ini["description"]["more info"].replace("\\n","\n")
        self.more_info = format_links(self, self.more_info, link_formatting)
        self.changelog = selected_ini["description"]["changelog"].replace("\\n","\n")

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
            self.other_pack_modland_link = other_ini["links"]["modland"]
        else:
            self.other_pack = False
            self.other_pack_workshop_link = ""
            self.other_pack_trucky_link = ""
            self.other_pack_forums_link = ""
            self.other_pack_modland_link = ""

class Vehicle:
    def __init__(self, VEHICLE_DIRECTORY, game_short, file_name):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read("{}/{}/{}.ini".format(VEHICLE_DIRECTORY, game_short, file_name))
        self.name = config["vehicle info"]["name"]
        self.file_name = file_name
        self.trailer = config["vehicle info"].getboolean("trailer")
        self.mod = config["vehicle info"].getboolean("mod")
        self.mod_author = config["vehicle info"]["mod author"]
        self.mod_link_workshop = config["vehicle info"]["mod link workshop"]
        self.mod_link_forums = config["vehicle info"]["mod link forums"]
        self.mod_link_author_site = config["vehicle info"]["mod link author site"]
        self.mod_link_trucky = config["vehicle info"]["mod link trucky"]

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

        self.variable_game = tk.StringVar(None, "American Truck Simulator")
        self.variable_game.trace("w", self.update_selectable_mods)
        self.variable_selected_mod = tk.StringVar(None, "")
        self.variable_selected_mod.trace("w", self.load_pack)

        self.panel_mod = ttk.LabelFrame(self.container, text = "Mod Selection")
        self.panel_mod.grid(row = 0, column = 0, sticky = "new", padx = 5, pady = (5, 0))
        self.panel_selector = ttk.Notebook(self.container)
        self.panel_selector.grid(row = 1, column = 0, sticky = "sew", padx = 5, pady = (0, 5))
        self.panel_editor = ttk.Frame(self.container)
        self.panel_selector.add(self.panel_editor, text = " Edit Paintjob Pack ")
        self.panel_description = ttk.Frame(self.container)
        self.panel_selector.add(self.panel_description, text = " Generate Description ")
        self.panel_checklist = ttk.LabelFrame(self.container, text = "Pack Checklist")
        self.panel_checklist.grid(row = 0, rowspan = 2, column = 1, padx = (0, 5), pady = 5, sticky = "nw")

        self.game_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_game, values = ["Euro Truck Simulator 2", "American Truck Simulator"])
        self.game_select.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "news")
        self.mod_select = ttk.Combobox(self.panel_mod, state = "readonly", textvariable = self.variable_selected_mod, values = [])
        self.mod_select.grid(row = 0, column = 1, sticky = "ew", padx = (0,5))
        self.panel_mod.columnconfigure(0, weight = 1)
        self.panel_mod.columnconfigure(1, weight = 6)

        self.editor_paintjobs_label = ttk.Label(self.panel_editor, text = "Paintjobs")
        self.editor_paintjobs_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nw")
        self.editor_paintjobs_text = tk.Text(self.panel_editor, height = 2.5, width = 35)
        self.editor_paintjobs_text.grid(row = 0, rowspan = 2, column = 1, padx = 5, pady = 5)
        self.editor_short_description_label = ttk.Label(self.panel_editor, text = "Short description")
        self.editor_short_description_label.grid(row = 2, column = 0, padx = 5, sticky = "nw")
        self.editor_short_description_text = tk.Text(self.panel_editor, height = 2.5, width = 35)
        self.editor_short_description_text.grid(row = 2, rowspan = 2, column = 1, padx = 5, pady = (0, 5))
        self.editor_more_info_label = ttk.Label(self.panel_editor, text = "More info")
        self.editor_more_info_label.grid(row = 4, column = 0, padx = 5, sticky = "nw")
        self.editor_more_info_text = tk.Text(self.panel_editor, height = 2.5, width = 35)
        self.editor_more_info_text.grid(row = 4, rowspan = 2, column = 1, padx = 5, pady = (0, 5))
        self.editor_related_mods_label = ttk.Label(self.panel_editor, text = "Related mods")
        self.editor_related_mods_label.grid(row = 6, column = 0, padx = 5, sticky = "nw")
        self.editor_related_mods_hint = ttk.Label(self.panel_editor, text = "Pack/Reason", foreground = "gray")
        self.editor_related_mods_hint.grid(row = 7, column = 0, padx = 5, sticky = "nw")
        self.editor_related_mods_text = tk.Text(self.panel_editor, height = 2.5, width = 35)
        self.editor_related_mods_text.grid(row = 6, rowspan = 2, column = 1, padx = 5, pady = (0, 5))
        self.editor_changelog_label = ttk.Label(self.panel_editor, text = "Changelog")
        self.editor_changelog_label.grid(row = 8, column = 0, padx = 5, sticky = "nw")
        self.editor_changelog_text = tk.Text(self.panel_editor, height = 2.5, width = 35)
        self.editor_changelog_text.grid(row = 8, rowspan = 2, column = 1, padx = 5, pady = (0, 5))
        self.editor_bus_pack_variable = tk.BooleanVar(None, False)
        self.editor_bus_pack_checkbox = ttk.Checkbutton(self.panel_editor, text = "Bus pack", variable = self.editor_bus_pack_variable)
        self.editor_bus_pack_checkbox.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "w")
        self.editor_sort_vehicles = ttk.Button(self.panel_editor, text = "Sort vehicles", width = 20, command = lambda : self.sort_vehicles())
        self.editor_sort_vehicles.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = "w")
        self.editor_header_label = ttk.Label(self.panel_editor, text = "Header image")
        self.editor_header_label.grid(row = 1, column = 2, padx = 5, sticky = "nw")
        self.editor_header_variable = tk.StringVar()
        self.editor_header_text = ttk.Entry(self.panel_editor, textvariable = self.editor_header_variable, width = 40)
        self.editor_header_text.grid(row = 1, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_showcase_label = ttk.Label(self.panel_editor, text = "Showcase image")
        self.editor_showcase_label.grid(row = 2, column = 2, padx = 5, sticky = "nw")
        self.editor_showcase_variable = tk.StringVar()
        self.editor_showcase_text = ttk.Entry(self.panel_editor, textvariable = self.editor_showcase_variable, width = 40)
        self.editor_showcase_text.grid(row = 2, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_workshop_label = ttk.Label(self.panel_editor, text = "Steam Workshop")
        self.editor_workshop_label.grid(row = 3, column = 2, padx = 5, sticky = "nw")
        self.editor_workshop_variable = tk.StringVar()
        self.editor_workshop_text = ttk.Entry(self.panel_editor, textvariable = self.editor_workshop_variable, width = 40)
        self.editor_workshop_text.grid(row = 3, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_trucky_label = ttk.Label(self.panel_editor, text = "TruckyMods")
        self.editor_trucky_label.grid(row = 4, column = 2, padx = 5, sticky = "nw")
        self.editor_trucky_variable = tk.StringVar()
        self.editor_trucky_text = ttk.Entry(self.panel_editor, textvariable = self.editor_trucky_variable, width = 40)
        self.editor_trucky_text.grid(row = 4, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_forums_label = ttk.Label(self.panel_editor, text = "SCS Forums")
        self.editor_forums_label.grid(row = 5, column = 2, padx = 5, sticky = "nw")
        self.editor_forums_variable = tk.StringVar()
        self.editor_forums_text = ttk.Entry(self.panel_editor, textvariable = self.editor_forums_variable, width = 40)
        self.editor_forums_text.grid(row = 5, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_modland_label = ttk.Label(self.panel_editor, text = "Modland")
        self.editor_modland_label.grid(row = 6, column = 2, padx = 5, sticky = "nw")
        self.editor_modland_variable = tk.StringVar()
        self.editor_modland_text = ttk.Entry(self.panel_editor, textvariable = self.editor_modland_variable, width = 40)
        self.editor_modland_text.grid(row = 6, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_sharemods_label = ttk.Label(self.panel_editor, text = "ShareMods")
        self.editor_sharemods_label.grid(row = 7, column = 2, padx = 5, sticky = "nw")
        self.editor_sharemods_variable = tk.StringVar()
        self.editor_sharemods_text = ttk.Entry(self.panel_editor, textvariable = self.editor_sharemods_variable, width = 40)
        self.editor_sharemods_text.grid(row = 7, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_modsbase_label = ttk.Label(self.panel_editor, text = "modsBase")
        self.editor_modsbase_label.grid(row = 8, column = 2, padx = 5, sticky = "nw")
        self.editor_modsbase_variable = tk.StringVar()
        self.editor_modsbase_text = ttk.Entry(self.panel_editor, textvariable = self.editor_modsbase_variable, width = 40)
        self.editor_modsbase_text.grid(row = 8, column = 3, padx = 5, pady = (0, 5), sticky = "nw")
        self.editor_save_pack = ttk.Button(self.panel_editor, text = "Save pack", width = 30, command = lambda : self.save_pack())
        self.editor_save_pack.grid(row = 9, column = 3, padx = 5, pady = (0, 5), sticky = "w")

        self.desc_mod_manager = ttk.Button(self.panel_description, text = "Mod manager", command = lambda : self.mod_manager_description())
        self.desc_mod_manager.grid(row = 0, column = 0, sticky = "news", padx = 5, pady = 5)
        self.desc_workshop = ttk.Button(self.panel_description, text = "Steam Workshop", command = lambda : self.workshop_description())
        self.desc_workshop.grid(row = 1, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_forums = ttk.Button(self.panel_description, text = "SCS Forums", command = lambda : self.forums_description())
        self.desc_forums.grid(row = 2, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_short = ttk.Button(self.panel_description, text = "Short Forums", command = lambda : self.short_forums_description())
        self.desc_short.grid(row = 3, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_trucky = ttk.Button(self.panel_description, text = "TruckyMods", command = lambda : self.trucky_description())
        self.desc_trucky.grid(row = 4, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_short = ttk.Button(self.panel_description, text = "Short Trucky", command = lambda : self.short_trucky_description())
        self.desc_short.grid(row = 5, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_modland = ttk.Button(self.panel_description, text = "Modland", command = lambda : self.modland_description())
        self.desc_modland.grid(row = 6, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.desc_ets2_lt = ttk.Button(self.panel_description, text = "ets2.lt", command = lambda : self.ets2_lt_description())
        self.desc_ets2_lt.grid(row = 7, column = 0, sticky = "news", padx = 5, pady = (0, 5))
        self.description_output = tk.Text(self.panel_description, height = 17.4)
        self.description_output.grid(row = 0, rowspan = 8, column = 1, sticky = "news", padx = (0,5), pady = 5)
        self.panel_description.columnconfigure(0, weight = 1)
        self.panel_description.columnconfigure(1, weight = 4)

        self.editor_bus_pack_variable = tk.BooleanVar(None, False)
        self.editor_bus_pack_checkbox = ttk.Checkbutton(self.panel_editor, text = "Bus pack", variable = self.editor_bus_pack_variable)
        self.checklist_packer_variable = tk.BooleanVar(None, False)
        self.checklist_packer_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Generate files with Paintjob Packer", variable = self.checklist_packer_variable)
        self.checklist_packer_checkbox.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nw")
        self.checklist_paintjob_variable = tk.BooleanVar(None, False)
        self.checklist_paintjob_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Make paintjob textures", variable = self.checklist_paintjob_variable)
        self.checklist_paintjob_checkbox.grid(row = 1, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_icon_variable = tk.BooleanVar(None, False)
        self.checklist_icon_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Make in-game icon", variable = self.checklist_icon_variable)
        self.checklist_icon_checkbox.grid(row = 2, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_screenshots_variable = tk.BooleanVar(None, False)
        self.checklist_screenshots_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Take screenshots x5", variable = self.checklist_screenshots_variable)
        self.checklist_screenshots_checkbox.grid(row = 3, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_templated_images_variable = tk.BooleanVar(None, False)
        self.checklist_templated_images_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Make templated images and crop screenshots", variable = self.checklist_templated_images_variable)
        self.checklist_templated_images_checkbox.grid(row = 4, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_upload_images_variable = tk.BooleanVar(None, False)
        self.checklist_upload_images_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Upload header and showcase, add links", variable = self.checklist_upload_images_variable)
        self.checklist_upload_images_checkbox.grid(row = 5, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_mod_manager_variable = tk.BooleanVar(None, False)
        self.checklist_mod_manager_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Generate mod manager description", variable = self.checklist_mod_manager_variable)
        self.checklist_mod_manager_checkbox.grid(row = 6, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_workshop_variable = tk.BooleanVar(None, False)
        self.checklist_workshop_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Package, upload to Steam Workshop, add link", variable = self.checklist_workshop_variable)
        self.checklist_workshop_checkbox.grid(row = 7, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_trucky_variable = tk.BooleanVar(None, False)
        self.checklist_trucky_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Re-package, upload to Trucky Mod Hub, add link", variable = self.checklist_trucky_variable)
        self.checklist_trucky_checkbox.grid(row = 8, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_sharemods_variable = tk.BooleanVar(None, False)
        self.checklist_sharemods_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Upload to ShareMods and modsBase, add links", variable = self.checklist_sharemods_variable)
        self.checklist_sharemods_checkbox.grid(row = 9, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_forums_variable = tk.BooleanVar(None, False)
        self.checklist_forums_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Upload to SCS Forums, add link", variable = self.checklist_forums_variable)
        self.checklist_forums_checkbox.grid(row = 10, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_forums_link_variable = tk.BooleanVar(None, False)
        self.checklist_forums_link_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Add forums link to main post", variable = self.checklist_forums_link_variable)
        self.checklist_forums_link_checkbox.grid(row = 12, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_forums_trucky_variable = tk.BooleanVar(None, False)
        self.checklist_forums_trucky_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Add forums link to Trucky page", variable = self.checklist_forums_trucky_variable)
        self.checklist_forums_trucky_checkbox.grid(row = 13, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_modland_variable = tk.BooleanVar(None, False)
        self.checklist_modland_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Upload to Modland", variable = self.checklist_modland_variable)
        self.checklist_modland_checkbox.grid(row = 14, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_ets2_lt_variable = tk.BooleanVar(None, False)
        self.checklist_ets2_lt_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Upload to ets2.lt/atsmods.lt", variable = self.checklist_ets2_lt_variable)
        self.checklist_ets2_lt_checkbox.grid(row = 15, column = 0, padx = 5, pady = (0, 5), sticky = "nw")
        self.checklist_modland_link_variable = tk.BooleanVar(None, False)
        self.checklist_modland_link_checkbox = ttk.Checkbutton(self.panel_checklist, text = "Add Modland link", variable = self.checklist_modland_link_variable)
        self.checklist_modland_link_checkbox.grid(row = 16, column = 0, padx = 5, pady = (0, 5), sticky = "nw")

        self.game_short = ""
        self.update_selectable_mods(self)

    def update_selectable_mods(self, *args):
        game_short_dict = {"Euro Truck Simulator 2":"ets", "American Truck Simulator":"ats"}
        self.game_short = game_short_dict[self.variable_game.get()]
        mod_list_incomplete = []
        mod_list_complete = []
        for file_name in os.listdir(self.game_short):
            each_mod = configparser.ConfigParser(allow_no_value = True)
            each_mod.optionxform = str
            each_mod.read("{}/{}".format(self.game_short, file_name), encoding = "utf-8")
            each_mod_stage = int(each_mod["pack info"]["checklist stage"])
            if each_mod_stage < 15:
                mod_list_incomplete.append(file_name[:-4])
            else:
                mod_list_complete.append(file_name[:-4])
        mod_list = mod_list_incomplete + mod_list_complete
        self.mod_select.configure(values = mod_list)
        self.variable_selected_mod.set(mod_list[0])

    def sort_vehicles(self, *args):
        selected_ini = configparser.ConfigParser(allow_no_value = True)
        selected_ini.optionxform = str
        selected_ini.read("{}/{}.ini".format(self.game_short, self.variable_selected_mod.get()), encoding = "utf-8")

        trucks = []
        for truck in selected_ini["pack info"]["trucks"].split(";"):
            if truck != "":
                trucks.append(Vehicle(VEHICLE_DIRECTORY, self.game_short, truck))
        trucks.sort(key = lambda veh: veh.name)
        truck_mods = []
        for truck_mod in selected_ini["pack info"]["truck mods"].split(";"):
            if truck_mod != "":
                truck_mods.append(Vehicle(VEHICLE_DIRECTORY, self.game_short, truck_mod))
        truck_mods.sort(key = lambda veh: veh.name)
        trailers = []
        for trailer in selected_ini["pack info"]["trailers"].split(";"):
            if trailer != "":
                trailers.append(Vehicle(VEHICLE_DIRECTORY, self.game_short, trailer))
        trailers.sort(key = lambda veh: veh.name)
        trailer_mods = []
        for trailer_mod in selected_ini["pack info"]["trailer mods"].split(";"):
            if trailer_mod != "":
                trailer_mods.append(Vehicle(VEHICLE_DIRECTORY, self.game_short, trailer_mod))
        trailer_mods.sort(key = lambda veh: veh.name)

        truck_names = []
        for veh in trucks:
            truck_names.append(veh.file_name)
        truck_names = ";".join(truck_names)
        trailer_names = []
        for veh in trailers:
            trailer_names.append(veh.file_name)
        trailer_names = ";".join(trailer_names)
        truck_mod_names = []
        for veh in truck_mods:
            truck_mod_names.append(veh.file_name)
        truck_mod_names = ";".join(truck_mod_names)
        trailer_mod_names = []
        for veh in trailer_mods:
            trailer_mod_names.append(veh.file_name)
        trailer_mod_names = ";".join(trailer_mod_names)

        selected_ini["pack info"]["trucks"] = truck_names
        selected_ini["pack info"]["trailers"] = trailer_names
        selected_ini["pack info"]["truck mods"] = truck_mod_names
        selected_ini["pack info"]["trailer mods"] = trailer_mod_names

        with open("{}/{}.ini".format(self.game_short, self.variable_selected_mod.get()), "w") as configfile:
            selected_ini.write(configfile)

        print("\a") # audio confirmation
        print("\a")

    def save_pack(self, *args):
        selected_ini = configparser.ConfigParser(allow_no_value = True)
        selected_ini.optionxform = str
        selected_ini.read("{}/{}.ini".format(self.game_short, self.variable_selected_mod.get()), encoding = "utf-8")

        selected_ini["pack info"]["bus pack"] = str(self.editor_bus_pack_variable.get())
        selected_ini["pack info"]["paintjobs"] = self.editor_paintjobs_text.get("1.0", "end").rstrip().replace("\n", ";")

        checklist_variables = [self.checklist_packer_variable, self.checklist_paintjob_variable, self.checklist_icon_variable,
                               self.checklist_screenshots_variable, self.checklist_templated_images_variable, self.checklist_upload_images_variable,
                               self.checklist_mod_manager_variable, self.checklist_workshop_variable, self.checklist_trucky_variable,
                               self.checklist_sharemods_variable, self.checklist_forums_variable, self.checklist_forums_link_variable,
                               self.checklist_forums_trucky_variable, self.checklist_modland_variable, self.checklist_ets2_lt_variable,
                               self.checklist_modland_link_variable]
        checklist_stage = 0
        for i in range(len(checklist_variables)):
            if checklist_variables[i].get() and i > checklist_stage:
                checklist_stage = i
        selected_ini["pack info"]["checklist stage"] = str(checklist_stage)

        selected_ini["description"]["short description"] = self.editor_short_description_text.get("1.0", "end").rstrip().replace("\n", "\\n")
        selected_ini["description"]["more info"] = self.editor_more_info_text.get("1.0", "end").rstrip().replace("\n", "\\n")
        selected_ini["description"]["related mods"] = self.editor_related_mods_text.get("1.0", "end").rstrip().replace("\n", ";")
        selected_ini["description"]["changelog"] = self.editor_changelog_text.get("1.0", "end").rstrip().replace("\n", "\\n")

        selected_ini["images"]["header"] = self.editor_header_variable.get()
        selected_ini["images"]["showcase"] = self.editor_showcase_variable.get()

        selected_ini["links"]["steam workshop"] = self.editor_workshop_variable.get()
        selected_ini["links"]["forums"] = self.editor_forums_variable.get()
        selected_ini["links"]["trucky"] = self.editor_trucky_variable.get()
        selected_ini["links"]["modland"] = self.editor_modland_variable.get()
        selected_ini["links"]["sharemods"] = self.editor_sharemods_variable.get()
        selected_ini["links"]["modsbase"] = self.editor_modsbase_variable.get()

        with open("{}/{}.ini".format(self.game_short, self.variable_selected_mod.get()), "w", encoding="utf-8") as configfile:
            selected_ini.write(configfile)

        print("\a") # audio confirmation
        print("\a")

    def load_pack(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        self.editor_paintjobs_text.delete("1.0", "end")
        self.editor_paintjobs_text.insert("1.0", "\n".join(desc_vars.paintjobs))
        self.editor_short_description_text.delete("1.0", "end")
        self.editor_short_description_text.insert("1.0", desc_vars.short_description)
        self.editor_more_info_text.delete("1.0", "end")
        self.editor_more_info_text.insert("1.0", desc_vars.more_info)
        related_mods = []
        for rel in desc_vars.related_mods:
            related_mods.append(rel[0] + "/" + rel[1])
        self.editor_related_mods_text.delete("1.0", "end")
        self.editor_related_mods_text.insert("1.0", "\n".join(related_mods))
        self.editor_changelog_text.delete("1.0", "end")
        self.editor_changelog_text.insert("1.0", desc_vars.changelog)
        self.editor_bus_pack_variable.set(desc_vars.bus_pack)
        self.editor_header_variable.set(desc_vars.image_header)
        self.editor_showcase_variable.set(desc_vars.image_showcase)
        self.editor_workshop_variable.set(desc_vars.workshop_link)
        self.editor_forums_variable.set(desc_vars.forums_link)
        self.editor_trucky_variable.set(desc_vars.trucky_link)
        self.editor_modland_variable.set(desc_vars.modland_link)
        self.editor_sharemods_variable.set(desc_vars.sharemods_link)
        self.editor_modsbase_variable.set(desc_vars.modsbase_link)
        checklist_variables = [self.checklist_packer_variable, self.checklist_paintjob_variable, self.checklist_icon_variable,
                               self.checklist_screenshots_variable, self.checklist_templated_images_variable, self.checklist_upload_images_variable,
                               self.checklist_mod_manager_variable, self.checklist_workshop_variable, self.checklist_trucky_variable,
                               self.checklist_sharemods_variable, self.checklist_forums_variable, self.checklist_forums_link_variable,
                               self.checklist_forums_trucky_variable, self.checklist_modland_variable, self.checklist_ets2_lt_variable,
                               self.checklist_modland_link_variable]
        for i in range(len(checklist_variables)):
            if i <= desc_vars.checklist_stage:
                checklist_variables[i].set(True)
            else:
                checklist_variables[i].set(False)

    def change_directory(self, *args):
        new_directory = filedialog.askdirectory(title = "Package output", initialdir = self.variable_directory.get())
        if new_directory != "":
            self.variable_directory.set(new_directory)

    def workshop_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "bbcode")
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
                desc += "- " + pj + "\n"
            desc += "\n"
        if desc_vars.bus_pack:
            desc += "[img]{}[/img]\n".format(IMAGE_BUSES_SUPPORTED)
            for veh in desc_vars.truck_mods:
                desc += "- {}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
            desc += "\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRUCKS_SUPPORTED)
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "- " + veh.name + "\n"
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "- {}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
                desc += "\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "[img]{}[/img]\n".format(IMAGE_TRAILERS_SUPPORTED)
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "- " + veh.name + "\n"
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "- {}'s [url={}]{}[/url]\n".format(veh.mod_author, veh.mod_link("wtfa"), veh.name)
                desc += "\n"
        if self.game_short == "ets":
            desc += "Let me know in the comments if you'd like to see any other vehicles supported, including any of [url={}#euro-truck-simulator-2]these mods![/url]\n\n".format(MOD_LINK_PAGE)
        else:
            desc += "Let me know in the comments if you'd like to see any other vehicles supported, including any of [url={}#american-truck-simulator]these mods![/url]\n\n".format(MOD_LINK_PAGE)
        if desc_vars.more_info != "":
            desc += desc_vars.more_info + "\n\n"
        if len(desc_vars.related_mods) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_RELATED_MODS)
            for rel in desc_vars.related_mods:
                desc += "[url={}]{}[/url] - {}\n".format(rel[2], rel[0], rel[1])
            desc += "\n"
        desc += "[img]{}[/img]\n".format(IMAGE_ENJOY)
        desc += "Please don't reupload my mods to other sites. They're already available elsewhere, if you'd like to download them directly. Thanks :)\n\n"
        desc += "Everything I make is (and always will be) free, but if you'd like to support the creation of my mods you can [url={}]buy me a coffee.[/url]\nSupport isn't expected, but it is appreciated!\n\n".format(BUY_ME_A_COFFEE)
        desc += "You can [url=https://steamcommunity.com/id/carsmaniac/myworkshopfiles/]follow me on the Workshop[/url] to see more!"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def forums_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "bbcode")
        desc = ""
        desc += "[img]{}[/img]\n\n".format(desc_vars.image_showcase)
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += "[b]This mod requires my [url={}]bus resource pack[/url] to work![/b]\n\n".format(BUS_RESOURCES_FORUMS)
        if desc_vars.other_pack:
            desc += "{} pack available [url={}]here[/url].\n\n".format(desc_vars.other_game, desc_vars.other_pack_forums_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "[img]{}[/img]\n".format(IMAGE_PAINTJOBS_INCLUDED)
            desc += "[list]\n"
            for pj in desc_vars.paintjobs:
                desc += "[*]{}\n".format(pj)
            desc += "[/list]\n\n"
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
        desc += "[list]\n"
        desc += "[*][url={}][size=150][b][color=#e7e7e7]Share[/color][color=#32d98c]Mods[/color][/b][/size] (direct download)[/url]\n".format(desc_vars.sharemods_link)
        desc += "[*][url={}][size=150][b][color=#200a5d]mods[/color][color=#eb5d0f]Base[/color][/b][/size] (mirror download)[/url]\n".format(desc_vars.modsbase_link)
        desc += "[*][url={}][size=150][b][color=#c81f55]TruckyMods[/color][/b][/size] (instant install and older versions)[/url]\n".format(desc_vars.trucky_link)
        desc += "[*][url={}][size=150][b][color=#7d9ac4]Steam Workshop[/color][/b][/size] (instant install and auto-updates)[/url]\n".format(desc_vars.workshop_link)
        desc += "[/list]\n"
        desc += "[size=85]Please don't reupload my mods. Thanks :)[/size]"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def trucky_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "html")
        desc = ""
        desc += "<div> <!-- Cars was here ;) -->\n"
        desc += "    <p>{}</p>\n".format(desc_vars.short_description.replace("\n\n", "</p>\n    <p>"))
        if desc_vars.bus_pack:
            desc += "    <p style=\"font-weight: 700\">This mod requires my <a style=\"color: white; text-decoration: underline\" href=\"{}\">bus resource pack</a>to work!</p>\n".format(BUS_RESOURCES_TRUCKY)
        if desc_vars.other_pack:
            desc += "    <p>{} pack available <a style=\"color: white; text-decoration: underline\" href=\"{}\">here</a>.</p>\n".format(desc_vars.other_game, desc_vars.other_pack_trucky_link)
        if len(desc_vars.paintjobs) >= 1:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Paintjobs included</p>\n"
            desc += "    <ul style=\"list-style: none; padding-left: 15px\">\n"
            for pj in desc_vars.paintjobs:
                desc += "        <li>- {}</li>\n".format(pj)
            desc += "    </ul>\n"
        if desc_vars.bus_pack:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Buses supported</p>\n"
            desc += "    <ul style=\"list-style: none; padding-left: 15px\">\n"
            for veh in desc_vars.truck_mods:
                desc += "        <li>- {}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
            desc += "    </ul>\n"
        else:
            if len(desc_vars.trucks) + len(desc_vars.truck_mods) >= 1:
                desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Trucks supported</p>\n"
                desc += "    <ul style=\"list-style: none; padding-left: 15px\">\n"
                if len(desc_vars.trucks) >= 1:
                    for veh in desc_vars.trucks:
                        desc += "        <li>- {}</li>\n".format(veh.name)
                if len(desc_vars.truck_mods) >= 1:
                    for veh in desc_vars.truck_mods:
                        desc += "        <li>- {}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
                desc += "    </ul>\n"
            if len(desc_vars.trailers) + len(desc_vars.trailer_mods) >= 1:
                desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Trailers supported</p>\n"
                desc += "    <ul style=\"list-style: none; padding-left: 15px\">\n"
                if len(desc_vars.trailers) >= 1:
                    for veh in desc_vars.trailers:
                        desc += "        <li>- {}</li>\n".format(veh.name)
                if len(desc_vars.trailer_mods) >= 1:
                    for veh in desc_vars.trailer_mods:
                        desc += "        <li>- {}'s <a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a></li>\n".format(veh.mod_author, veh.mod_link("tfaw"), veh.name)
                desc += "    </ul>\n"
        if self.game_short == "ets":
            desc += "    <p>Let me know in the comments if you'd like to see any other vehicles supported, including any of <a style=\"color: white; text-decoration: underline\" href=\"{}#euro-truck-simulator-2\">these mods!</a></p>\n".format(MOD_LINK_PAGE)
        else:
            desc += "    <p>Let me know in the comments if you'd like to see any other vehicles supported, including any of <a style=\"color: white; text-decoration: underline\" href=\"{}#american-truck-simulator\">these mods!</a></p>\n".format(MOD_LINK_PAGE)
        if desc_vars.more_info != "":
            desc += "    <p>{}</p>".format(desc_vars.more_info.replace("\n\n", "</p>\n    <p>"))
        if len(desc_vars.related_mods) >= 1:
            desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Related mods</p>\n"
            desc += "    <ul>\n"
            for rel in desc_vars.related_mods:
                desc += "        <li><a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a> - {}</li>\n".format(rel[3], rel[0], rel[1])
            desc += "    </ul>\n"
        desc += "    <p style=\"color: white; font-family: Montserrat, sans-serif; font-size: 24px; font-weight: 700\">Enjoy! :)</p>\n"
        desc += "    <p>Everything I make is (and always will be) free, but if you'd like to support the creation of my mods you can <a style=\"color: white; text-decoration: underline\" href=\"{}\">buy me a coffee</a>. Support isn't expected, but it is appreciated!\n".format(BUY_ME_A_COFFEE)
        desc += "</div>"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def modland_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "txt")
        desc = ""
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += ">> This mod requires my bus resource pack to work! <<\n"
            desc += "Download it here: {}\n\n".format(BUS_RESOURCES_MODLAND)
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
            desc += "I've also made a pack for {}:\n{}\n\n".format(desc_vars.other_game, desc_vars.other_pack_modland_link)
        desc += "Please don't reupload my mods to other sites. Thanks, and enjoy! :)"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def ets2_lt_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "txt")
        desc = ""
        desc += desc_vars.short_description + "\n\n"
        if desc_vars.bus_pack:
            desc += ">> This mod requires my bus resource pack to work! <<\n"
            desc += "Download it here: {}\n\n".format(BUS_RESOURCES_FORUMS)
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
        desc += "Changelog for " + desc_vars.changelog.replace("Version", "version").replace("\n", ":\n", 1) + "\n\n"
        desc += "Please don't reupload my mods to other sites. Thanks, and enjoy! :)"
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def short_trucky_description(self, *args):
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

    def short_forums_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get())
        desc = ""
        desc += "[url={}][b][size=150]{}[/size][/b][/url] - ".format(desc_vars.forums_link[25:], desc_vars.mod_name)
        if desc_vars.bus_pack:
            desc += "{} buses".format(len(desc_vars.truck_mods))
        else:
            total_trucks = len(desc_vars.trucks) + len(desc_vars.truck_mods)
            total_trailers = len(desc_vars.trailers) + len(desc_vars.trailer_mods)
            if total_trucks >= 1 and total_trailers >= 1:
                desc += "{} trucks, {} trailers".format(total_trucks, total_trailers)
            elif total_trucks >= 1:
                desc += "{} trucks".format(total_trucks)
            elif total_trailers >= 1:
                desc += "{} trailers".format(total_trailers)
        if len(desc_vars.paintjobs) >= 1:
            desc += ", {} different paintjobs".format(len(desc_vars.paintjobs))
        self.description_output.delete("1.0", "end")
        self.description_output.insert("1.0", desc)

    def mod_manager_description(self, *args):
        desc_vars = DescVars(self.game_short, self.variable_selected_mod.get(), "txt")
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

def format_links(self, desc_text, format):
    if format == "none":
        return desc_text
    else:
        if "](" in desc_text:
            link_index = desc_text.index("](") # assuming there is only ever one link in a description
            link_start = []
            for i in range(link_index):
                if desc_text[link_index - i] == "[":
                    link_start.append(link_index - i) # only the first value is used, so only the bracket that actually marks the link is counted
            link_end = []
            for i in range(len(desc_text) - link_index):
                if desc_text[link_index + i] == ")":
                    link_end.append(link_index + i + 1)
            md_link = desc_text[link_start[0]:link_end[0]] # link in markdown (md) format
            link = md_link[1:-1].split("](")
            if format == "bbcode":
                output_link = "[url={}]{}[/url]".format(link[1], link[0])
            elif format == "html":
                output_link = "<a style=\"color: white; text-decoration: underline\" href=\"{}\">{}</a>".format(link[1], link[0])
            elif format == "txt":
                output_link = link[0]
            return desc_text[:link_start[0]] + output_link + desc_text[link_end[0]:]
        else:
            return desc_text

def main():
    root = tk.Tk()
    root.title("Paintjob Tracker")
    root.resizable(False, False)
    tracker = TrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
