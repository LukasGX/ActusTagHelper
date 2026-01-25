from colorama import Fore
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import re

import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def conv(xml_filename):
    script_dir = Path(__file__).parent
    xml_path = script_dir / f"{xml_filename}.xml"
    json_path = script_dir / f"{xml_filename}.json"

    if xml_path.exists() and xml_path.is_file() and xml_path.suffix.lower() == '.xml':
        tree = ET.parse(xml_path)
        root = tree.getroot()
        print(Fore.GREEN + "XML loaded successfully" + Fore.RESET)

        # fetch meta data
        mtd = root.find("norm").find("metadaten")
        book_short = mtd.find("jurabk").text
        book_long = mtd.find("langue").text

        # fetch laws
        norms = root.findall("norm")

        laws = []

        for norm in norms:
            mtd = norm.find("metadaten")
            ttd = norm.find("textdaten")

            enbez = mtd.find("enbez")
            if enbez == None: continue

            # name
            name = enbez.text
            pattern = r'^§(.*)|^\(XXXX\)\s*§§(.*)'
            
            match = re.match(pattern, name.strip())
            if match:
                content = match.group(1) or match.group(2)
                
                if match.group(1): clean_name = f"§{content.strip()}"
                else: clean_name = f"§§{content.strip()}"
            else: continue

            # title
            try:
                title = mtd.find("titel").text
            except:
                continue
            
            # content
            content_el = ttd.find(".//Content")
            if content_el is not None:
                contentlines = content_el.findall("P")
            else:
                content = ""
                continue

            content = ""
            for line in contentlines:
                dl = line.find("DL")
                
                # 1. P-Text IMMER zuerst
                if line.text:
                    content += line.text.strip() + "\n"
                
                # 2. DL-Inhalt NUR bei DL
                if dl is not None:
                    output = ""
                    dl_children = list(dl)
                    i = 0
                    while i < len(dl_children):
                        child = dl_children[i]
                        if child.tag == "DT" and child.text:
                            output += child.text.strip()
                            if i+1 < len(dl_children) and dl_children[i+1].tag == "DD":
                                dd = dl_children[i+1]
                                la = dd.find("LA")
                                if la is not None and la.text:
                                    output += " " + la.text.strip() + "\n"
                        i += 1
                    
                    if output:  # ← NUR output hinzufügen!
                        content += output
                

            laws.append({
                "name": clean_name,
                "title": title,
                "content": content,
                "offenses": [],
                "consequences": []
            })

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "abbr": book_short,
                "name": book_long,
                "laws": laws
            }, indent=4))
    else:
        print(Fore.RED + "Error: File not found or not valid xml" + Fore.RESET)

def fill_offenses(json_filename):
    script_dir = Path(__file__).parent
    json_path = script_dir / f"{json_filename}.json"

    if json_path.exists() and json_path.is_file() and json_path.suffix.lower() == '.json':
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read()
            json_content = json.loads(content)

        for i, law in enumerate(json_content["laws"]):
            if law.get("offenses") == []:
                offenses = []
                print(Fore.YELLOW + f"Choose mode for this law ({law.get("name")}):" + Fore.RESET)
                print(Fore.LIGHTBLUE_EX + "\"" + law.get("content") + "\"" + Fore.RESET)
                print(Fore.YELLOW + "s=Skip, m=Input manually, x=Save and close" + Fore.RESET)
                char = getch()
                if char == "s":
                    continue
                elif char == "m":
                    print(Fore.YELLOW + "Type every offense (QUIT if you're finished)" + Fore.RESET)
                    while True:
                        offense = input(">> ")
                        if offense == "QUIT": break
                        else: offenses.append(offense)

                    json_content["laws"][i]["offenses"] = offenses
                elif char == "x":
                    with open(json_path, "w", encoding="utf-8") as f:
                        f.write(json.dumps(json_content, indent=4))
                    print("Closed")
                    return

def fill_consequences(json_filename):
    script_dir = Path(__file__).parent
    json_path = script_dir / f"{json_filename}.json"

    if json_path.exists() and json_path.is_file() and json_path.suffix.lower() == '.json':
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read()
            json_content = json.loads(content)

        for i, law in enumerate(json_content["laws"]):
            if law.get("consequences") == []:
                consequences = []
                print(Fore.YELLOW + f"Choose mode for this law ({law.get("name")}):" + Fore.RESET)
                print(Fore.LIGHTBLUE_EX + "\"" + law.get("content") + "\"" + Fore.RESET)
                print(Fore.YELLOW + "s=Skip, m=Input manually, x=Save and close" + Fore.RESET)
                char = getch()
                if char == "s":
                    continue
                elif char == "m":
                    print(Fore.YELLOW + "Type every consequence (QUIT if you're finished)" + Fore.RESET)
                    while True:
                        consequence = input(">> ")
                        if consequence == "QUIT": break
                        else: consequences.append(consequence)

                    json_content["laws"][i]["consequences"] = consequences
                elif char == "x":
                    with open(json_path, "w", encoding="utf-8") as f:
                        f.write(json.dumps(json_content, indent=4))
                    print("Closed")
                    return