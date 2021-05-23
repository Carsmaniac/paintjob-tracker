import tkinter as tk
from tkinter import ttk

class TrackerApp:

    def __init__(self, master):
        self.container = ttk.Frame(master)
        self.container.pack(fill = "both")

        self.variable_game = tk.StringVar(None, "Euro Truck Simulator 2")
        self.variable_game.trace("w", self.update_selectable_mods)
        self.variable_selected_mod = tk.StringVar(None, "")
        self.variable_directory = tk.StringVar(None, "D:\\Documents\\Trucksim\\Uploading")

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
        self.description_copier = ttk.Button(self.panel_description, text = "Copy to clipboard", command = lambda : self.copy_description())
        self.description_copier.grid(row = 5, column = 0, sticky = "news", padx = 5, pady = (0,5))
        self.description_output = tk.Text(self.panel_description)
        self.description_output.grid(row = 0, rowspan = 6, column = 1, sticky = "news", padx = (0,5), pady = 5)
        self.panel_description.columnconfigure(0, weight = 1)
        self.panel_description.columnconfigure(1, weight = 4)

        self.update_selectable_mods(self)

    def update_selectable_mods(self, *args):
        if self.variable_game.get() == "Euro Truck Simulator 2":
            mod_list = ["Very Long Company Name Inc Paintjob Pack", "ets2"]
            self.mod_select.configure(values = mod_list)
            self.variable_selected_mod.set(mod_list[0])
        else:
            mod_list = ["ats1", "ats2"]
            self.mod_select.configure(values = mod_list)
            self.variable_selected_mod.set(mod_list[0])

    def change_directory(self, *args):
        pass

    def generate_workshop(self, *args):
        pass
        # self.description_output.delete("1.0", "end")
        # self.description_output.insert("1.0", "some\ntext\nhere")
        # text = self.description_output.get("1.0", "end")

    def generate_standalone(self, *args):
        pass

    def workshop_description(self, *args):
        pass

    def forums_description(self, *args):
        pass

    def trucky_description(self, *args):
        pass

    def plaint_text_description(self, *args):
        pass

    def short_description(self, *args):
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
