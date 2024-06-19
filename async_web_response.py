import asyncio
import aiohttp
import json
import time
from random import random


def load_urls(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

async def fetch(session, url, user, password):
    max_retries = 3
    for _ in range(max_retries):
        try:
            async with session.get(url, timeout=20, auth=aiohttp.BasicAuth(user, password)) as response:
                if response.status == 401:
                    print(f"401 Unauthorized for {url} - Invalid credentials")
                elif response.status == 404:
                    print(f"404 found at {url}")
                elif response.status == 500:
                    print(f"500 found at {url}")
                break
        except aiohttp.ClientError as e:
            print(f"ClientError occurred for {url}: {e}")
        except asyncio.TimeoutError:
            print(f"TimeoutError for {url}")
        except Exception as e:
            print(f"Exception occurred for {url}: {e}")
        await asyncio.sleep(random()) 
    else:
        print(f"Failed to fetch {url} after {max_retries} attempts.")

def get_tasks(session, urls, base_url, user, password):
    tasks = []
    for paths in urls:
        url = f'{base_url}{paths}'
        tasks.append(asyncio.create_task(fetch(session,url,user,password)))
    return tasks
    
async def main(file_path,base_url,user,password):
    urls = load_urls(file_path)
    async with aiohttp.ClientSession(connector= aiohttp.TCPConnector(ssl=False, limit= 100)) as session:
        tasks = get_tasks(session, urls, base_url, user, password)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    file_path = './user-data/url_paths.json'
    base_url = f'https://www.example.com' #add you URL
    user = '' #add Username
    password = '' #add Password
    asyncio.run(main(file_path,base_url,user,password))
    end = time.time()