#!/usr/bin/env python3

from secf import save, load
from colorama import Fore, Style
import os, time
import re


def hashtag_search(content, hashtags, fnc):
    for line in content:
        if fnc(hashtag in line.split() for hashtag in hashtags):
            yield line


def snp_hashtag(header, content, hashtags, fnc):
    for line in hashtag_search(content, hashtags, fnc):
        print(f"[out] {header}) {line}")


path = os.path.join(os.path.expanduser("~"), ".sectionify")
os.makedirs(path, exist_ok=True)
path = path + "/"
file = {}
changed = False
existing_slots = set()
print(
    "Welcome to my CLI tool.\nThis is used to store data in form of sections and it's entries.\nYou can choose to save data into one of the 3 slots(slot 0, slot 1, slot 2) availaible. You can also choose to restore from a slot at anytime by issueing the appropriate command.\nEnter '??' for help. Press Ctrl+C to exit this interface."
)
for i in range(3):
    if os.path.exists(f"{path}slot{i}"):
        existing_slots.add(str(i))
if existing_slots:
    print(
        f"\n[out] There are {len(existing_slots)} saved states in slot {', '.join(existing_slots)}."
    )

while True:
    try:
        query = input("\nEnter your Query >> ").strip()
        if not query:
            continue
    # Quit method:
    except KeyboardInterrupt:
        if changed:
            try:
                dec = input(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + f"\n[Warn] You have performed some operations since your last save. Please save them else you'll lose the data.\n[out] Press Ctrl+C again to quit, press any other key to cancel quit operation.\n>>"
                    + Style.RESET_ALL
                )
                continue
            except KeyboardInterrupt:
                print(Fore.CYAN + Style.BRIGHT + "\nBye :)" + Style.RESET_ALL)
                exit(130)
        print(Fore.CYAN + Style.BRIGHT + "\nBye :)" + Style.RESET_ALL)
        exit(130)

    if query == "?s":
        for section in file:
            print("[out] " + section)

    elif query == "??" or query == "help":
        print(f"[out] Commands availiable:")
        print(f"[out] +s <section name>  - Add a new Section")
        print(f"[out] +e <section name>  - Add an entry to an existing Section")
        print(
            """[out] ?s 		 - List existing sections.\
            \n[out] ?e <section name>  - Print an entry in a section. Use '*' to print all the entries\
            \n[out] -e <section name>  - Delete an entry from an existing section\
            \n[out] -s <section name>  - Delete a Section\
            \n[out] #<string>          - List all the entries along with it's section name where the hashtag was used\
            \n[out] ?s <section name> () #<string>      - List all the entries of the given section where the hashtag was used\
            \n[out] (Note: For below commands you can specify 2 or more hashtags)\
            \n[out] | #<string> #<string>       - List all the entries along with it's section name where either of the hashtags were used\
            \n[out] & #<string> #<string>       - List all the entries along with it's section name where all of the hashtags were used\
            \n[out] ?s <section name> () | #<string> #<string>      - List all the entries of the given section where either of the hashtags were used\
            \n[out] ?s <section name> () & #<string> #<string>      - List all the entries of the given section where all of the hashtags were used\
            \n[out] save <slot_no>     - Save the state of the program to given slot number\
            \n[out] restore <slot_no>  - Restore the previously stored state of the program\
            \n[out] slots              - Print all the available slots, and their status\
            \n[out] ??                 - Print this message.\
            \n[out] help               - Print this message. """
        )

    elif query == "slots":
        for i in range(3):
            if str(i) in existing_slots:
                st = os.stat(f"{path}slot" + str(i))
                print(
                    f"[out] Slot {i} -- {len(load(f'{path}slot'+str(i)))} section(s)  -- {time.asctime(time.localtime(st[9]))}"
                )
            else:
                print(f"[out] Slot {i} -- unused")

    # elif re.search("^(#[^ ]+ )+$", query + " "):
    #     hashtags = query.split()
    #     for header, content in file.items():
    #         snp_hashtag(header, content, hashtags, any)

    # elif re.search(r"^&( #[^ ]+)+$", query):
    #     hashtags = query.split()[1:]
    #     for header, content in file.items():
    #         snp_hashtag(header, content, hashtags, all)

    # elif re.search(r"^\|( #[^ ]+)+$", query):
    #     hashtags = query.split()[1:]
    #     for header, content in file.items():
    #         snp_hashtag(header, content, hashtags, any)

    elif re.search(r"^([|&])?\s*((#[^\s#]+\s+)*(#[^\s#]+))$", query):
        fnc = any
        p = re.search(r"^([|&])?\s*((#[^\s#]+\s+)*(#[^\s#]+))$", query)
        operation = p.group(1)
        hashtags = p.group(2).split()
        if operation == "&":
            fnc = all
        for header, content in file.items():
            snp_hashtag(header, content, hashtags, fnc)

    elif re.match(
        r"^\?e\s+([^()]+)\s*\(\)\s*([&|])?\s*((#[^\s#]+\s+)*(#[^\s#]+))$", query
    ):
        fnc = any
        p = re.match(
            r"^\?e\s+([^()]+)\s*\(\)\s*([&|])?\s*((#[^\s#]+\s+)*(#[^\s#]+))$", query
        )
        section = p.group(1)
        if section not in file:
            print(
                Fore.RED
                + Style.BRIGHT
                + "[Err ] Section doesn't exist."
                + Style.RESET_ALL
            )
            continue
        operation = p.group(2)
        hashtags = p.group(3).split()
        if operation == "":
            fnc = any
        elif operation == "&":
            fnc = all
        elif operation == "|":
            fnc = any
        snp_hashtag(section, file[section], hashtags, fnc)

    # elif re.search(r"^\?e ([^\(\)]+) \(\) ((#[^\s]+ )+)$", query + " "):
    #     p = re.search(r"^\?e ([^\(\)]+) \(\) ((#[^\s]+ )+)$", query + " ")
    #     section = p.group(1)
    #     if section not in file:
    #         print(
    #             Fore.RED
    #             + Style.BRIGHT
    #             + "[Err ] Section doesn't exist."
    #             + Style.RESET_ALL
    #         )
    #         continue
    #     hashtags = p.group(2).split()
    #     snp_hashtag(section, file[section], hashtags, any)

    # elif re.search(r"^\?e ([^\(\)]+) \(\) \|(( #[^\s]+)+)$", query):
    #     p = re.search(r"^\?e ([^\(\)]+) \(\) \|(( #[^\s]+)+)$", query)
    #     section = p.group(1)
    #     if section not in file:
    #         print(
    #             Fore.RED
    #             + Style.BRIGHT
    #             + "[Err ] Section doesn't exist."
    #             + Style.RESET_ALL
    #         )
    #         continue
    #     hashtags = p.group(2).split()
    #     snp_hashtag(section, file[section], hashtags, any)

    # elif re.search(r"^\?e ([^\(\)]+) \(\) &(( #[^ ]+)+)$", query):
    #     p = re.search(r"^\?e ([^\(\)]+) \(\) &(( #[^ ]+)+)$", query)
    #     section = p.group(1)
    #     if section not in file:
    #         print(
    #             Fore.RED
    #             + Style.BRIGHT
    #             + "[Err ] Section doesn't exist."
    #             + Style.RESET_ALL
    #         )
    #         continue
    #     hashtags = p.group(2).split()
    #     snp_hashtag(section, file[section], hashtags, all)

    else:
        command, *arg = query.split()
        arg = " ".join(arg)

        if "(" in arg or ")" in arg:
            print(
                Fore.RED
                + Style.BRIGHT
                + "[Err] We don't allow '(' or ')' in section name or entry."
                + Style.RESET_ALL
            )
            continue

        if command == "+s":
            if arg in file:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err] Section already exists, use +e to add new entry."
                    + Style.RESET_ALL
                )
            elif not arg:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err] Section name can't be blank."
                    + Style.RESET_ALL
                )
            else:
                file[arg] = []
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + f"[out] New Section '{arg}' added."
                    + Style.RESET_ALL
                )
                changed = True
        elif command == "+e":
            if arg not in file:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err] Section doesn't exist. Use '+s' to create a section."
                    + Style.RESET_ALL
                )
                continue
            line = input("line >> ").strip()
            if not line:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err] Blank line entry not yet supported."
                    + Style.RESET_ALL
                )
            else:
                file[arg].append(line)
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + f"[out] Entry added. Reference no. is '{len(file[arg])}'."
                    + Style.RESET_ALL
                )
                changed = True

        elif command == "?e":
            if arg not in file:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err] Section doesn't exist."
                    + Style.RESET_ALL
                )
                continue

            ref_no = input("Ref No>> ").strip()
            if ref_no == "*":
                for i in range(len(file[arg])):
                    print(f"[out] ({i+1}.) {file[arg][i]}")
            elif ref_no == "":
                continue
            else:
                try:
                    print(file[arg][int(ref_no) - 1])
                except:
                    print(
                        Fore.RED
                        + Style.BRIGHT
                        + "[Err ] Enter from existing Reference numbers."
                        + Style.RESET_ALL
                    )
                    continue

        elif command[0] == "-":
            if arg not in file:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "[Err ] Section doesn't exist."
                    + Style.RESET_ALL
                )
                continue

            if command[1] == "s":
                decision = (
                    input(
                        f"This section contains {len(file[arg])} entries, This will delete all its entries along with section.\n"
                        + "Press 'Y' to delete, press any other key to cancel this operation\n>> "
                    )
                    .strip()
                    .upper()
                )
                if decision == "Y":
                    file.pop(arg)
                    print(
                        Fore.GREEN
                        + Style.BRIGHT
                        + f"[out] Section {arg} and its entries deleted."
                        + Style.RESET_ALL
                    )
                    changed = True
                else:
                    print("[out] Deletion Aborted.")
                    continue

            elif command[1] == "e":
                ref_no = input("Ref No>> ").strip()
                if ref_no == "*":
                    decision = (
                        input(
                            "All the entries will be deleted.\nPress 'Y' to delete, press any other key to cancel this operation\n>> "
                        )
                        .strip()
                        .upper()
                    )
                    if decision == "Y":
                        file[arg].clear()
                        print(
                            Fore.GREEN
                            + Style.BRIGHT
                            + "Entries deleted."
                            + Style.RESET_ALL
                        )
                        changed = True
                else:
                    decision = input(
                        Fore.RED
                        + Style.BRIGHT
                        + f"You are deleting: {file[arg][int(ref_no)-1]}\nPress 'Y' to delete, press any other key to cancel this operation\n>> "
                        + Style.RESET_ALL
                    ).strip()
                    if decision == "Y":
                        file[arg].pop(int(ref_no) - 1)
                        print(
                            Fore.GREEN
                            + Style.BRIGHT
                            + "Entry deleted."
                            + Style.RESET_ALL
                        )
                        changed = True

        elif command == "save":
            if arg not in ["0", "1", "2"]:
                continue
            if not changed:
                print("[out] There's nothing to save")
                continue

            slot = f"{path}slot" + arg
            if arg in existing_slots:
                des = input(
                    Fore.RED
                    + Style.BRIGHT
                    + f"[out] This will overwrite the contents in slot {arg}\n[out] Press 'O' to Overwrite, press any other key to cancel save operation.\n>>"
                    + Style.RESET_ALL
                ).strip()
                if des != "O":
                    continue
            res = save(file, slot)
            if res:
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + f"[out] saved all sections and its contents to slot {arg}."
                    + Style.RESET_ALL
                )
                existing_slots.add(arg)
                changed = False
            else:
                print("some error")
                continue

        elif command == "restore":
            if arg not in ["0", "1", "2"]:
                continue
            if changed:
                des = input(
                    Fore.RED
                    + Style.BRIGHT
                    + f"[out] Loading from slot {arg} will overwrite the sections present in this session,\n[out] Press 'R' to continue restoring, press any other key to cancel this operation.\n>>"
                    + Style.RESET_ALL
                )
                if des != "R":
                    continue
            file = load(f"{path}slot{arg}")
            print(f"[out] sucessfully restored from slot {arg}.")

        else:
            print("Invalid command. Enter '??' for help.")
