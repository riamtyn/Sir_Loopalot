import time

startTime = time.time()

def err(text):
    elapsedTime = int(time.time() - startTime)
    print(f'[\033[31m ERROR \033[0m] -- {text} -- Error occured at {elapsedTime} seconds')

def succ(text):
    elapsedTime = int(time.time() - startTime)
    print(f'[\033[32m SUCCESS \033[0m] -- {text} -- Completed at {elapsedTime} seconds')

def warn(text):
    elapsedTime = int(time.time() - startTime)
    print(f'[\033[33m SUCCESS \033[0m] -- {text} -- Completed at {elapsedTime} seconds')
