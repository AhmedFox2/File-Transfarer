import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, Tk
from tkinterdnd2 import TkinterDnD, DND_FILES

# Update the on_drop function to hide the "اسحب وأفلت" label when files are added
def on_drop(event):
    global files,drop_area,start_button, drop_label
    if event.data not in files:
        files.extend(files)  # Add new files to the existing list
    else:
        pass
    files = root.tk.splitlist(event.data)

    if not files:
        label.configure(text="اسحب وأفلت الملفات هنا")
        drop_label.place(relx=0.5, rely=0.5, anchor="center")  # Show the "اسحب وأفلت" label
    else:
        drop_label.place_forget()  # Hide the "اسحب وأفلت" label

    # Display file previews
    for file in files:
        file_name = os.path.basename(file)
        file_label = ctk.CTkLabel(drop_area, text=file_name, anchor="w", font=("Arial", 12), text_color="#FFFFFF")
        file_label.pack(fill="x", padx=10, pady=5)

    if destination:
        start_button.configure(state="normal")

def select_destination():
    global destination, destination_entry,start_button
    destination = filedialog.askdirectory()
    if destination:
        destination_entry.configure(state="normal")
        destination_entry.delete(0, "end")
        destination_entry.insert(0, destination)
        destination_entry.configure(state="readonly")
        if files:
            start_button.configure(state="normal")

def start_transfer():
    global files, destination, progress_bar, label, start_button, action_var
    if not files:
        label.configure(text="اسحب وأفلت الملفات هنا")
        return

    if not destination:
        return

    progress_bar.set(0)
    total_files = len(files)
    action = action_var.get()

    try:
        for i, file in enumerate(files, start=1):
            if action == "نسخ":
                shutil.copy(file, destination)
            elif action == "نقل":
                shutil.move(file, destination)

            progress_bar.set(i / total_files)

        label.configure(text="تمت العملية بنجاح")
    except Exception as e:
        label.configure(text=f"حدث خطأ: {e}")

    files = []
    start_button.configure(state="disabled")

# Initialize the main application
root = TkinterDnD.Tk()
root.title("برنامج نقل الملفات")
root.geometry("900x700")
root.resizable(True, True)
root.configure(bg="black")

# Configure customtkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
# Create main container
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True)

# Create header
header_frame = ctk.CTkFrame(main_frame, corner_radius=10, height=60, fg_color="#3B8ED0")
header_frame.pack(padx=10, pady=10, fill="x")
header_label = ctk.CTkLabel(
    header_frame,
    text="نقل وإدارة الملفات",
    font=("Arial", 24, "bold"),
    text_color="white"
)
header_label.pack(pady=10)

# Create UI elements
progress_bar = ctk.CTkProgressBar(
    main_frame,
    width=400,
    height=15,
    corner_radius=10,
    progress_color="#28A745"
)
progress_bar.pack(pady=20)
progress_bar.set(0)

# Create destination frame
dest_frame = ctk.CTkFrame(main_frame, corner_radius=10)
dest_frame.pack(pady=10, padx=20, fill="x")

destination_entry = ctk.CTkEntry(
    dest_frame,
    width=400,
    state="readonly",
    height=35,
    corner_radius=8,
    placeholder_text="مسار المجلد..."
)
destination_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

destination_button = ctk.CTkButton(
    dest_frame,
    text="تحديد المجلد",
    command=select_destination,
    height=35,
    corner_radius=8,
)
destination_button.pack(side="left", padx=10, pady=10)

# Create action frame
action_frame = ctk.CTkFrame(main_frame, corner_radius=10)
action_frame.pack(pady=10)

action_var = ctk.StringVar(value="نسخ")
copy_radio = ctk.CTkRadioButton(
    action_frame,
    text="نسخ",
    variable=action_var,
    value="نسخ",
)
copy_radio.pack(side="left", padx=20, pady=10)

move_radio = ctk.CTkRadioButton(
    action_frame,
    text="نقل",
    variable=action_var,
    value="نقل",
)
move_radio.pack(side="left", anchor="e")
# Create label for drag and drop

start_button = ctk.CTkButton(
    main_frame,
    text="بدء العملية",
    command=start_transfer,
    state="disabled",
    height=40,
    corner_radius=8,
    fg_color="#28A745"
)
start_button.pack(pady=10)

# Create a custom font
# لتعريف خط خاص بك، قم بتغيير مسار الملف إلى مسار الخط على جهازك
# مثال: custom_font = ("Cairo", 16) # إذا كان لديك خط القاهرة مثبت
# أو: custom_font = ("Tajawal", 16) # إذا كان لديك خط تجوال مثبت
custom_font = ("Arial", 16)  # الخط الافتراضي

# Update the drop area with better styling
drop_area = ctk.CTkFrame(
    main_frame,
    corner_radius=15,
    border_width=2,
    fg_color="#2B2B2B",  # لون خلفية داكن
)
drop_area.pack(pady=20, padx=20, fill="both", expand=True)

drop_label = ctk.CTkLabel(
    drop_area,
    text="اسحب وأفلت الملفات هنا",
    font=custom_font,
    text_color="#FFFFFF"
)
drop_label.place(relx=0.5, rely=0.5, anchor="center")

# Add a subtle hint text
hint_label = ctk.CTkLabel(
    main_frame,
    text="* يمكنك سحب وإفلات عدة ملفات في نفس الوقت",
    font=("Arial", 12),
    text_color="#666666"
)
hint_label.pack(pady=5)

# Drag & Drop functionality
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)

files = []
destination = None

root.mainloop()