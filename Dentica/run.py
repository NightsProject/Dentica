import os

# 1. Define folders that need __init__.py
folders_to_check = [
    "Frontend",
    "Frontend/Dialogues",
    "Backend",
    "Backend/config"
]

# 2. Create __init__.py if missing
for folder in folders_to_check:
    init_path = os.path.join(folder, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# Auto-generated to make this a package\n")
        print(f"[+] Created: {init_path}")
    else:
        print(f"[✓] Exists:  {init_path}")

# 3. Fix import in denticagui_main.py
gui_file = "Frontend/denticagui_main.py"
if os.path.exists(gui_file):
    with open(gui_file, "r") as f:
        lines = f.readlines()

    fixed_lines = []
    changed = False
    for line in lines:
        if "from Dialogues." in line:
            fixed_line = line.replace("from Dialogues.", "from .Dialogues.")
            fixed_lines.append(fixed_line)
            changed = True
            print(f"[~] Fixed import in: {gui_file}")
        else:
            fixed_lines.append(line)

    if changed:
        with open(gui_file, "w") as f:
            f.writelines(fixed_lines)
else:
    print(f"[!] File not found: {gui_file}")
