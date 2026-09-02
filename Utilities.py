# File to hold utilities, such as helper functions.

import colorama


def utilities_setup ():
    colorama.init()



def urgent_print (string):
    str(string)
    print(colorama.Fore.RED + 'Urgent: ' + string + colorama.Style.RESET_ALL)

def exit_print_and_exit():
    print(colorama.Fore.RED + colorama.Style.BRIGHT + 'EXITING' + colorama.Style.RESET_ALL)
    exit()

def warn_print(string):
    str(string)
    print(colorama.Fore.CYAN + 'Warning: ' + string + colorama.Style.RESET_ALL)

def good_print(string):
    print(colorama.Fore.GREEN + 'Good: ' + string + colorama.Style.RESET_ALL)



