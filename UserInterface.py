from CommunicationNode import CommunicationNode
from Resource import Resource
import tkinter as tk
import tkinter.filedialog as fd
import os
import sys

from utils import save_file, load_file


class UserInterface(tk.Tk):
    """
    """
    local_node: CommunicationNode = None

    def __init__(
            self,
            local_node: CommunicationNode = None,
            title: str = None,
            background: str = None,
            download_folder_name: str = None
    ):
        super().__init__()
        self.local_node = local_node
        self.remoteResources = []
        self.title(title)
        self.download_folder_name = download_folder_name
        self.geometry("240x240")
        self.config(bg=background)
        self.configure(background='#FFCC99')
        bg = 'Orange'
        tk.Button(self, text='Status', width=20, bg=bg, command=self.status).place(x=20, y=20)
        tk.Button(self, text='List', width=20, bg=bg, command=self.list_local_resources).place(x=20, y=50)
        tk.Button(self, text='Download file', width=20, bg=bg, command=self.download_file).place(x=20, y=80)
        tk.Button(self, text='Transfer', width=20, bg=bg, command=self.transfer).place(x=20, y=110)
        tk.Button(self, text='Add file', width=20, bg=bg, command=self.add_file).place(x=20, y=140)
        tk.Button(self, text='Remove file', width=20, bg=bg, command=self.remove_file).place(x=20, y=170)
        tk.Button(self, text='Turn off', width=20, bg=bg, command=self.turn_off).place(x=20, y=200)

    def status(self):
        list_window = tk.Toplevel(self)
        list_window.title("Nodes")
        listbox = tk.Listbox(list_window)
        listbox.pack()
        for client in self.local_node.clients:
            listbox.insert(tk.END, client)

    def populate_resources_listbox(self, listbox):
        for client in self.local_node.clients:
            resources = self.local_node.nodes_and_files[client]
            if resources[0] == '':
                pass
            else:
                for i in range(0, len(resources)):
                    listbox.insert(tk.END, f"{resources[i]} | {client}")
        return listbox

    def list_local_resources(self):
        list_window = tk.Toplevel(self)
        list_window.title("Resources")
        list_window.geometry("300x300")
        listbox = tk.Listbox(list_window, width=50)
        listbox.pack()
        for resource in self.local_node.resources:
            listbox.insert(tk.END, resource.name)
        listbox = self.populate_resources_listbox(listbox)
        return list_window, listbox

    def transfer(self):
        list_window = tk.Toplevel(self)
        list_window.title("Remote resources")
        list_window.geometry("300x300")
        listbox = tk.Listbox(list_window, width=50)
        listbox.pack()
        listbox = self.populate_resources_listbox(listbox)

        def run_transfer():
            selected_index = listbox.curselection()
            if selected_index:
                selected_resource_with_address = listbox.get(selected_index[0])
                resource_name, resource_address = selected_resource_with_address.replace(" ", "").split("|")
                ip, port = resource_address.split(":")
                list_window.destroy()
                self.local_node.ask_for_resource_thread(resource_name, ip, int(port))

        transfer = tk.Button(list_window, text="transfer", command=run_transfer)
        transfer.pack(pady=10)

    def add_file(self):
        file = fd.askopenfilename(title='Choose a file of any type', filetypes=[("All files", "*.*")])
        if file:
            file_data = load_file(os.path.abspath(file))
            if file_data:
                resource = Resource(os.path.basename(file), file_data)
                is_duplicate = False

                for existing_resource in self.local_node.resources:
                    if existing_resource.name == resource.name and existing_resource.data != resource.data:
                        is_duplicate = True
                        base_name, extension = os.path.splitext(resource.name)
                        new_name = resource.name
                        i = 1
                        while any(existing.name == new_name for existing in self.local_node.resources):
                            new_name = f"{base_name}({i}){extension}"
                            i += 1
                        resource.name = new_name
                        self.local_node.add_resource(resource)
                        break
                    elif existing_resource.name == resource.name and existing_resource.data == resource.data:
                        print(f"Resource {resource.name} already exists on this node")
                        is_duplicate = True
                        break

                if not is_duplicate:
                    self.local_node.add_resource(resource)

    def remove_file(self):
        list_window = tk.Toplevel(self)
        list_window.title("Resources")
        listbox = tk.Listbox(list_window)
        listbox.pack()
        for resource in self.local_node.resources:
            listbox.insert(tk.END, resource.name)

        def remove_selected_obj():
            selected_index = listbox.curselection()
            if selected_index:
                selected_value = listbox.get(selected_index[0])
                list_window.destroy()
                self.local_node.remove_resource(selected_value)

        remove_button = tk.Button(list_window, text="Remove", command=remove_selected_obj)
        remove_button.pack(pady=10)

    def download_file(self):
        list_window = tk.Toplevel(self)
        list_window.title("Resources")
        listbox = tk.Listbox(list_window)
        listbox.pack()
        for resource in self.local_node.resources:
            listbox.insert(tk.END, resource.name)

        def download_selected_obj():
            selected_index = listbox.curselection()
            if selected_index:
                selected_resource_name = listbox.get(selected_index[0])
                for listed_resource in self.local_node.resources:
                    if listed_resource.name == selected_resource_name:
                        save_file(f'{self.download_folder_name}/{selected_resource_name}', listed_resource.data)
                list_window.destroy()

        save_button = tk.Button(list_window, text="Download", command=download_selected_obj)
        save_button.pack(pady=10)

    def turn_off(self):
        self.destroy()
        sys.exit()
