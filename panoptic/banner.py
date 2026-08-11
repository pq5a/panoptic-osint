# just prints the name + module count when you run the tool.
# no need for anything fancier than this.

def print_banner():
    print()
    print("PANOPTIC")
    print("-" * 8)


def print_module_list(commands):
    # commands = dict of name -> (func, argname, help_text)
    print(f"{len(commands)} modules\n")
    i = 1
    for name, (_, argname, help_text) in commands.items():
        print(f"[{i}] {name} <{argname}> - {help_text}")
        i += 1
    print()
