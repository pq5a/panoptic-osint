"""ASCII banner for PANOPTIC."""

CYAN = "\033[36m"
MAGENTA = "\033[35m"
GREY = "\033[90m"
RESET = "\033[0m"

BANNER = f"""
{CYAN}
 ██▓███   ▄▄▄       ███▄    █  ▒█████   ██▓███  ▄▄▄█████▓ ██▓ ▄████▄
▓██░  ██▒▒████▄     ██ ▀█   █ ▒██▒  ██▒▓██░  ██▒▓  ██▒ ▓▒▓██▒▒██▀ ▀█
▓██░ ██▓▒▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██░ ██▓▒▒ ▓██░ ▒░▒██▒▒▓█    ▄
▒██▄█▓▒ ▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒██▄█▓▒ ▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒
▒██▒ ░  ░ ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░▒██▒ ░  ░  ▒██▒ ░ ░██░▒ ▓███▀ ░
▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ▒▓▒░ ░  ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░
░▒ ░       ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░▒ ░         ░     ▒ ░  ░  ▒
░░         ░   ▒      ░   ░ ░ ░ ░ ░ ▒  ░░         ░       ▒ ░░
               ░  ░         ░     ░ ░                     ░  ░ ░
                                                               ░
        {MAGENTA}O S I N T   R E C O N N A I S S A N C E   F R A M E W O R K{CYAN}
{RESET}
"""

TAGLINE = f"{GREY}  27 modules · zero API keys required to start · one target, total visibility{RESET}\n"


def print_banner():
    print(BANNER)
    print(TAGLINE)
