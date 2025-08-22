import subprocess
import json
from colorama import Fore, Style, init
from tabulate import tabulate
from pyfiglet import Figlet

init(autoreset=True)

# قراءة ملف الأدوات
with open("tools.json", "r") as f:
    categories = json.load(f)

def welcome():
    f = Figlet(font='slant')
    logo = f.renderText('DAN')
    print(Fore.CYAN + logo)
    print(Fore.GREEN + Style.BRIGHT + "WELCOME TO DAN TOOLS - Cyber Toolkit\n")

def show_categories():
    print(Fore.CYAN + "\n=== Cybersecurity Toolkit ===")
    for idx, category in enumerate(categories.keys(), 1):
        print(Fore.YELLOW + f"{idx}. {category}")

def show_tools(category):
    tools = categories[category]
    table = [[i+1, tool['name']] for i, tool in enumerate(tools)]
    print(Fore.GREEN + f"\n--- {category} ---")
    print(tabulate(table, headers=[Fore.CYAN + "No.", Fore.CYAN + "Tool"], tablefmt="fancy_grid"))

def tool_info(category, number):
    tools = categories[category]
    if 1 <= number <= len(tools):
        tool = tools[number-1]
        print(Fore.MAGENTA + f"\nName: {tool['name']}\nDescription: {tool['description']}\n")

        command = tool['command']
        try:
            # محاولة تشغيل الأداة مباشرة
            subprocess.call(f"sudo {command}", shell=True)
        except FileNotFoundError:
            print(Fore.RED + f"Error: {tool['name']} is not installed or not in PATH.")
            install = input(Fore.YELLOW + f"Do you want to install {tool['name']} now? (y/n): ").lower()
            if install == 'y':
                try:
                    print(Fore.CYAN + f"Installing {tool['name']}...")
                    subprocess.call(f"sudo apt install -y {command}", shell=True)
                    print(Fore.GREEN + f"{tool['name']} installed successfully! Running it now...")
                    subprocess.call(f"sudo {command}", shell=True)
                except Exception as e:
                    print(Fore.RED + f"Error installing/running the tool: {e}")
            else:
                print(Fore.CYAN + f"Skipping installation of {tool['name']}.")
        except Exception as e:
            print(Fore.RED + f"Error running the tool: {e}")
    else:
        print(Fore.RED + "Tool not found. Please enter a valid number.")

def main():
    welcome()
    while True:
        show_categories()
        choice = input(Fore.CYAN + "Select a category by number (or 'q' to quit): ")
        if choice.lower() == 'q':
            print(Fore.CYAN + "Exiting DAN Tools. Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = list(categories.keys())[int(choice)-1]
            show_tools(category)
            tool_choice = input(Fore.CYAN + "Select a tool by number (or 'b' to go back): ")
            if tool_choice.lower() == 'b':
                continue
            if tool_choice.isdigit():
                tool_info(category, int(tool_choice))
            else:
                print(Fore.RED + "Invalid input.")
        else:
            print(Fore.RED + "Please enter a valid number.")

if __name__ == "__main__":
    main()
