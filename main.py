# ActusTagHelper
# Simple console

from colorama import init, Fore
import conv

init()

def main():
    print(Fore.YELLOW + """
     _        _               _____              _   _      _                 
    / \\   ___| |_ _   _ ___  |_   _|_ _  __ _   | | | | ___| |_ __   ___ _ __ 
   / _ \\ / __| __| | | / __|   | |/ _` |/ _` |  | |_| |/ _ \\ | '_ \\ / _ \\ '__|
  / ___ \\ (__| |_| |_| \\__ \\   | | (_| | (_| |  |  _  |  __/ | |_) |  __/ |   
 /_/   \\_\\___|\\__|\\__,_|___/   |_|\\__,_|\\__, |  |_| |_|\\___|_| .__/ \\___|_|   
                                        |___/                |_|              
""" + Fore.RESET)
    print(f"""
{Fore.YELLOW}Commands:{Fore.RESET}
    - {Fore.YELLOW}conv{Fore.RESET} Convert xml from gesetze-im-internet.de to ActusTag json
    - {Fore.YELLOW}off{Fore.RESET} Fill ActusTag json with offenses (guided)
    - {Fore.YELLOW}exit{Fore.RESET} / {Fore.YELLOW}x{Fore.RESET} Get me out of here
""")
    
    while True:
        command = input("> ").lower()
        if command == "conv":
            print("Name of the xml file to convert")
            filename = input(">> ")
            conv.conv(filename)
        elif command == "off":
            print("Name of the json file to fill with offenses")
            filename = input(">> ")
            conv.fill_offenses(filename)
        elif command == "exit" or command == "x":
            break
        else:
            print(Fore.RED + "Unknown command" + Fore.RESET)

if __name__ == "__main__":
    main()