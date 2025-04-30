reset = "\033[0m"

def set_red(text):
    red = "\033[31m"
    return red + text + reset

def set_blue(text):
    blue = "\033[34m"
    return blue + text + reset

def set_green(text):
    green = "\033[32m"
    return green + text + reset

def set_cyan(text):
    cyan = "\033[36m"
    return cyan + text + reset

def set_magenta(text):
    magenta = "\033[35m"
    return magenta + text + reset

def set_white(text):
    white = "\033[37m"
    return white + text + reset

def set_yellow(text):
    yellow = "\033[33m"
    return yellow + text + reset

def default_color(text):
    return reset + text + reset
