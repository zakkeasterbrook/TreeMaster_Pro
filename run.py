import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os
import keyword
import re

class TreeNode:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = []
        self.content = ""  # Store file content temporarily

    def add_child(self, child_node):
        """Adds a child node if the current node is not a file."""
        if not self.is_file:
            self.children.append(child_node)

    def find_child(self, name):
        """Finds a child node by name."""
        for child in self.children:
            if child.name == name:
                return child
        return None

class TreeMasterPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TreeMaster Pro - File Structure Manager")
        self.geometry("1000x700")
        self.configure(bg="#1e1e1e")  # Set dark theme background

        # Initialize the root node with default name
        self.root_node_name = "MyProject"
        self.root_node = TreeNode(self.root_node_name)

        # Undo/Redo History
        self.history = []
        self.redo_stack = []

        # Load and resize icons
        self.folder_icon = self.load_and_resize_icon("folder_icon.png", (16, 16))
        self.python_icon = self.load_and_resize_icon("python_icon.png", (16, 16))
        self.html_icon = self.load_and_resize_icon("html_icon.png", (16, 16))
        self.js_icon = self.load_and_resize_icon("js_icon.png", (16, 16))
        self.css_icon = self.load_and_resize_icon("css.png", (16, 16))
        self.default_file_icon = self.load_and_resize_icon("default_file_icon.png", (16, 16))

        # Header Frame
        header_frame = tk.Frame(self, bg="#1e1e1e")
        header_frame.pack(fill=tk.X, padx=10, pady=5)

        # Project Name Entry
        self.project_name_var = tk.StringVar(value=self.root_node_name)
        project_name_entry = tk.Entry(header_frame, textvariable=self.project_name_var, font=("Arial", 14), bg="#2b2b2b", fg="#ffffff", width=20)
        project_name_entry.pack(side=tk.LEFT, padx=10)

        # Rename Button
        rename_btn = tk.Button(header_frame, text="Rename Project", command=self.rename_project, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        rename_btn.pack(side=tk.LEFT, padx=10)

        # Add title and instructions
        self.hidden_signature_revealed = False  # State for revealing the signature
        self.title_label = tk.Label(header_frame, text="TreeMaster Pro", font=("Arial", 20, "bold"), fg="#00d0ff", bg="#1e1e1e")
        self.title_label.pack(side=tk.LEFT, padx=10)
        self.title_label.bind("<Enter>", self.start_hover_timer)
        self.title_label.bind("<Leave>", self.cancel_hover_timer)

        instructions = tk.Label(self, text="Right-click or double-click on a file to edit or use the buttons below to manage the file tree.",
                                font=("Arial", 10), fg="#ffffff", bg="#1e1e1e")
        instructions.pack(pady=5)

        # Timer for revealing hidden text
        self.hover_timer = None

        # Obfuscated Data Structure and Function
        hidden_data = [90, 46, 84, 46, 69] 

        def _decode_signature(data):
            # The function is obfuscated and never called, used only to store the hidden signature
            return "".join(chr(x) for x in data)

        # Encapsulate and hide the signature retrieval
        signature = (lambda d: None)(_decode_signature(hidden_data))  # Encapsulation to prevent use

        # Button Frame
        button_frame = tk.Frame(self, bg="#1e1e1e")
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add Buttons
        add_folder_btn = tk.Button(button_frame, text="Add Folder", command=self.add_folder, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        add_folder_btn.grid(row=0, column=0, padx=5)
        add_file_btn = tk.Button(button_frame, text="Add File", command=self.add_file, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        add_file_btn.grid(row=0, column=1, padx=5)
        delete_btn = tk.Button(button_frame, text="Delete Node", command=self.delete_node, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        delete_btn.grid(row=0, column=2, padx=5)
        rename_node_btn = tk.Button(button_frame, text="Rename Node", command=self.rename_node, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        rename_node_btn.grid(row=0, column=3, padx=5)
        save_btn = tk.Button(button_frame, text="Save Structure", command=self.save_structure, bg="#282828", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        save_btn.grid(row=0, column=4, padx=5)
        undo_btn = tk.Button(button_frame, text="Undo", command=self.undo, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        undo_btn.grid(row=0, column=5, padx=5)
        redo_btn = tk.Button(button_frame, text="Redo", command=self.redo, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        redo_btn.grid(row=0, column=6, padx=5)

        # Preset Structures Frame
        preset_frame = tk.Frame(self, bg="#1e1e1e")
        preset_frame.pack(fill=tk.X, padx=10, pady=10)

        # Preset Structure Buttons
        flask_btn = tk.Button(preset_frame, text="Create Flask Structure", command=self.create_flask_structure, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        flask_btn.grid(row=0, column=0, padx=5)
        django_btn = tk.Button(preset_frame, text="Create Django Structure", command=self.create_django_structure, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        django_btn.grid(row=0, column=1, padx=5)
        web_btn = tk.Button(preset_frame, text="Create Basic Web Project", command=self.create_web_structure, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        web_btn.grid(row=0, column=2, padx=5)
        react_btn = tk.Button(preset_frame, text="Create React Project", command=self.create_react_structure, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        react_btn.grid(row=0, column=3, padx=5)
        node_btn = tk.Button(preset_frame, text="Create Node.js Project", command=self.create_nodejs_structure, bg="#007acc", fg="#ffffff", font=("Arial", 10), padx=10, pady=5)
        node_btn.grid(row=0, column=4, padx=5)

        # Treeview and Editor Frame
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview Widget
        self.tree = ttk.Treeview(main_frame, selectmode="browse", style="Treeview")
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid for resizing
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)

        # Embedded Editor
        self.editor_frame = tk.Frame(main_frame, bg="#1e1e1e")
        self.editor_frame.grid(row=0, column=1, sticky="nsew")
        self.text_area = ScrolledText(self.editor_frame, wrap=tk.WORD, font=("Courier New", 12), bg="#2b2b2b", fg="#ffffff")
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<KeyRelease>", self.syntax_highlight)

        # Treeview Styling
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="#ffffff", 
                        fieldbackground="#2b2b2b", 
                        font=("Arial", 10))
        style.map("Treeview", background=[("selected", "#007acc")], foreground=[("selected", "white")])
        
        # Context Menu
        self.menu = tk.Menu(self, tearoff=0, bg="#2b2b2b", fg="white")
        self.menu.add_command(label="Add Folder", command=self.add_folder)
        self.menu.add_command(label="Add File", command=self.add_file)
        self.menu.add_separator()
        self.menu.add_command(label="Delete", command=self.delete_node)
        self.menu.add_command(label="Rename", command=self.rename_node)
        self.menu.add_separator()
        self.menu.add_command(label="Edit", command=self.edit_file)
        self.menu.add_separator()
        self.menu.add_command(label="Save Structure", command=self.save_structure)
        
        # Bind right-click menu and double-click to the tree
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Populate the initial tree
        self.populate_tree()

    def load_and_resize_icon(self, path, size=(16, 16)):
        """Loads and resizes an icon image."""
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def start_hover_timer(self, event):
        """Starts a timer when the cursor hovers over the label."""
        self.hover_timer = self.after(3000, self.reveal_hidden_signature)

    def cancel_hover_timer(self, event):
        """Cancels the timer if the cursor leaves the label."""
        if self.hover_timer:
            self.after_cancel(self.hover_timer)
            self.hover_timer = None
            if self.hidden_signature_revealed:
                self.title_label.config(text="TreeMaster Pro")  # Hide the hidden text
                self.hidden_signature_revealed = False

    def reveal_hidden_signature(self):
        """Reveals the hidden signature."""
        if not self.hidden_signature_revealed:
            self.title_label.config(text="TreeMaster Pro Z.T.E")  # Reveals the hidden text
            self.hidden_signature_revealed = True

    def syntax_highlight(self, event=None):
        """Applies syntax highlighting to the text editor."""
        content = self.text_area.get("1.0", tk.END)
        self.text_area.mark_set("range_start", "1.0")
        data = content.split("\n")
        for i, line in enumerate(data):
            self.text_area.mark_set("range_start", f"{i + 1}.0")
            self.text_area.mark_set("range_end", f"{i + 1}.end")
            self.text_area.tag_remove("Keyword", f"{i + 1}.0", f"{i + 1}.end")
            self.text_area.tag_remove("Function", f"{i + 1}.0", f"{i + 1}.end")
            self.text_area.tag_remove("Comment", f"{i + 1}.0", f"{i + 1}.end")
            self.text_area.tag_remove("String", f"{i + 1}.0", f"{i + 1}.end")

            # Highlight Keywords
            for kw in keyword.kwlist:
                idx = line.find(kw)
                while idx != -1:
                    self.text_area.tag_add("Keyword", f"{i + 1}.{idx}", f"{i + 1}.{idx + len(kw)}")
                    idx = line.find(kw, idx + 1)

            # Highlight Function Definitions
            function_matches = re.finditer(r"def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(", line)
            for match in function_matches:
                self.text_area.tag_add("Function", f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")

            # Highlight Comments
            comment_start = line.find("#")
            if comment_start != -1:
                self.text_area.tag_add("Comment", f"{i + 1}.{comment_start}", f"{i + 1}.end")

            # Highlight Strings
            string_matches = re.finditer(r"(['\"])(?:(?=(\\?))\2.)*?\1", line)
            for match in string_matches:
                self.text_area.tag_add("String", f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")

        # Configure the colors for different tags
        self.text_area.tag_configure("Keyword", foreground="#ff79c6")
        self.text_area.tag_configure("Function", foreground="#50fa7b")
        self.text_area.tag_configure("Comment", foreground="#6272a4")
        self.text_area.tag_configure("String", foreground="#f1fa8c")

    def populate_tree(self):
        """Populates the treeview widget with the nodes."""
        self.tree.delete(*self.tree.get_children())  # Clear existing tree nodes
        self._add_to_tree("", self.root_node)

    def _add_to_tree(self, parent, node):
        """Adds a node and its children recursively to the treeview."""
        icon = self.get_icon(node.name, node.is_file)
        tree_id = self.tree.insert(parent, "end", text=node.name, image=icon, open=True)
        for child in node.children:
            self._add_to_tree(tree_id, child)

    def get_icon(self, name, is_file):
        """Returns the appropriate icon based on the file type."""
        if not is_file:
            return self.folder_icon
        if name.endswith('.py'):
            return self.python_icon
        elif name.endswith('.html'):
            return self.html_icon
        elif name.endswith('.js'):
            return self.js_icon
        elif name.endswith('.css'):
            return self.css_icon
        else:
            return self.default_file_icon

    def add_folder(self):
        """Adds a new folder node."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a node to add a folder to.")
            return
        parent_node = self.get_node_by_id(selected_item[0])
        if parent_node.is_file:
            messagebox.showwarning("Invalid Operation", "Cannot add a folder under a file.")
            return
        folder_name = simpledialog.askstring("Folder Name", "Enter the folder name:")
        if folder_name:
            self.save_state()  # Save current state for undo
            new_node = TreeNode(folder_name)
            parent_node.add_child(new_node)
            self.populate_tree()

    def add_file(self):
        """Adds a new file node."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a node to add a file to.")
            return
        parent_node = self.get_node_by_id(selected_item[0])
        if parent_node.is_file:
            messagebox.showwarning("Invalid Operation", "Cannot add a file under another file.")
            return
        file_name = simpledialog.askstring("File Name", "Enter the file name (e.g., main.py):")
        if file_name:
            if '.' not in file_name:
                messagebox.showwarning("Warning", "Please provide a valid file extension (e.g., .py, .html).")
                return
            self.save_state()  # Save current state for undo
            new_node = TreeNode(file_name, is_file=True)
            parent_node.add_child(new_node)
            self.populate_tree()

    def delete_node(self):
        """Deletes a selected node."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a node to delete.")
            return
        node = self.get_node_by_id(selected_item[0])
        if node:
            self.save_state()  # Save current state for undo
            parent_node = self.find_parent_node(self.root_node, node)
            if parent_node:
                parent_node.children.remove(node)
            self.populate_tree()

    def rename_node(self):
        """Renames a selected node."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a node to rename.")
            return
        node = self.get_node_by_id(selected_item[0])
        if node:
            new_name = simpledialog.askstring("Rename Node", f"Enter a new name for '{node.name}':")
            if new_name:
                self.save_state()  # Save current state for undo
                node.name = new_name
                self.populate_tree()

    def rename_project(self):
        """Renames the root project folder."""
        new_name = self.project_name_var.get().strip()
        if new_name:
            self.save_state()  # Save current state for undo
            self.root_node.name = new_name
            self.populate_tree()

    def show_context_menu(self, event):
        """Shows the context menu on right-click."""
        try:
            self.tree.selection_set(self.tree.identify_row(event.y))
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def on_double_click(self, event):
        """Handles double-click events on the treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        node = self.get_node_by_id(selected_item[0])
        if node and node.is_file:
            self.edit_file()

    def get_node_by_id(self, tree_id, node=None):
        """Finds a node by its tree ID."""
        if node is None:
            node = self.root_node
        if self.tree.item(tree_id)["text"] == node.name:
            return node
        for child in node.children:
            found_node = self.get_node_by_id(tree_id, child)
            if found_node:
                return found_node
        return None

    def find_parent_node(self, parent, target):
        """Finds the parent node of a given target node."""
        for child in parent.children:
            if child == target:
                return parent
            result = self.find_parent_node(child, target)
            if result:
                return result
        return None

    def save_structure(self):
        """Saves the file structure to disk."""
        directory = filedialog.askdirectory(title="Select Directory to Save Structure")
        if directory:
            try:
                self._save_to_disk(directory, self.root_node)
                messagebox.showinfo("Success", "File structure saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def _save_to_disk(self, path, node):
        """Recursively saves nodes to disk."""
        current_path = os.path.join(path, node.name)
        if node.is_file:
            with open(current_path, 'w') as file:
                file.write(node.content)  # Save the temporary content
        else:
            os.makedirs(current_path, exist_ok=True)
            for child in node.children:
                self._save_to_disk(current_path, child)

    def create_flask_structure(self):
        """Creates a basic Flask project structure."""
        flask_structure = {
            'app': ['__init__.py', 'routes.py', 'models.py'],
            'static': [],
            'templates': [],
            'requirements.txt': True,
            'run.py': True
        }
        self.build_structure(flask_structure, self.root_node)
        self.populate_tree()

    def create_django_structure(self):
        """Creates a basic Django project structure."""
        django_structure = {
            'project_name': ['__init__.py', 'settings.py', 'urls.py', 'wsgi.py', 'asgi.py'],
            'app_name': ['__init__.py', 'admin.py', 'apps.py', 'models.py', 'tests.py', 'views.py'],
            'manage.py': True,
        }
        self.build_structure(django_structure, self.root_node)
        self.populate_tree()

    def create_web_structure(self):
        """Creates a basic web project structure."""
        web_structure = {
            'css': ['styles.css'],
            'js': ['scripts.js'],
            'index.html': True,
            'README.md': True,
        }
        self.build_structure(web_structure, self.root_node)
        self.populate_tree()

    def create_react_structure(self):
        """Creates a basic React project structure."""
        react_structure = {
            'public': ['index.html', 'favicon.ico'],
            'src': ['index.js', 'App.js', 'App.css'],
            'package.json': True,
            'README.md': True
        }
        self.build_structure(react_structure, self.root_node)
        self.populate_tree()

    def create_nodejs_structure(self):
        """Creates a basic Node.js project structure."""
        nodejs_structure = {
            'src': ['index.js', 'app.js'],
            'routes': ['index.js'],
            'controllers': ['mainController.js'],
            'package.json': True,
            'README.md': True
        }
        self.build_structure(nodejs_structure, self.root_node)
        self.populate_tree()

    def build_structure(self, structure, parent_node):
        """Builds a predefined file structure."""
        self.save_state()  # Save current state for undo
        for key, value in structure.items():
            if isinstance(value, list):
                folder_node = TreeNode(key)
                parent_node.add_child(folder_node)
                for file in value:
                    folder_node.add_child(TreeNode(file, is_file=True))
            else:
                parent_node.add_child(TreeNode(key, is_file=True))

    def save_state(self):
        """Saves the current state of the tree for undo functionality."""
        self.history.append(self._clone_tree(self.root_node))
        self.redo_stack.clear()  # Clear redo stack on new action

    def undo(self):
        """Undo the last action."""
        if self.history:
            self.redo_stack.append(self._clone_tree(self.root_node))
            self.root_node = self.history.pop()
            self.populate_tree()

    def redo(self):
        """Redo the last undone action."""
        if self.redo_stack:
            self.history.append(self._clone_tree(self.root_node))
            self.root_node = self.redo_stack.pop()
            self.populate_tree()

    def _clone_tree(self, node):
        """Deep clones a tree for undo/redo purposes."""
        cloned_node = TreeNode(node.name, node.is_file)
        cloned_node.content = node.content
        for child in node.children:
            cloned_node.add_child(self._clone_tree(child))
        return cloned_node

    def edit_file(self):
        """Opens a mini code editor to edit the selected file."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a file to edit.")
            return
        node = self.get_node_by_id(selected_item[0])
        if node and node.is_file:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, node.content)
            self.text_area.bind("<KeyRelease>", lambda e: self.update_file_content(node))

    def update_file_content(self, node):
        """Updates the file content temporarily."""
        node.content = self.text_area.get(1.0, tk.END)

    def save_file_content(self, event=None):
        """Temporarily saves the file content within the application."""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        node = self.get_node_by_id(selected_item[0])
        if node and node.is_file:
            node.content = self.text_area.get(1.0, tk.END)
            messagebox.showinfo("Temporary Save", "Changes have been temporarily saved within the app.")

if __name__ == "__main__":
    app = TreeMasterPro()
    app.mainloop()
