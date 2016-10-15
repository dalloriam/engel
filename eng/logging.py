from colorama import Fore, Back, Style


def info(message):
  print(Style.RESET_ALL + message)

def reset():
  print(Style.RESET_ALL)

def success(message):
  print(Fore.GREEN + "+ " + message)

def error(message):
  print(Fore.RED + "Error: " + message)
  reset()
  exit()
