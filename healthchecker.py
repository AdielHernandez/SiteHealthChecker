import asyncio
import aiohttp
import json
import time
import pandas as pd
import numpy as np
from tqdm import tqdm

def load_urls(file_path:str) -> json:
    with open(file_path, 'r') as f:
        return json.load(f)

async def fetch(session:aiohttp.client.ClientSession, url:str, user: str, password:str, _) -> str:
    # number of retrie to try before returnin a failed fetch
    max_retries = 10
    for _ in range(max_retries):
        try:
            # makes a get to the url and checks the response
            async with session.get(url, timeout=200, auth=aiohttp.BasicAuth(user, password)) as response:
                if response.status >= 500:
                    return f"{response.status} found at {url}"
                elif response.status >= 400:
                    return f"{response.status} found at {url}"
                elif response.status >= 300:
                    return f"{response.status} found at {url}"
                elif response.status == 200:
                    return f"{response.status} found at {url}"
                break
        except aiohttp.ClientError as e:
            return f"ClientError occurred for {url}: {e}"
        except asyncio.TimeoutError:
            return f"TimeoutError for {url}"
        except Exception as e:
            return f"Exception occurred for {url}: {e}"
    else:
        return f"Failed to fetch {url} after {max_retries} attempts."

def get_tasks(session:aiohttp.client.ClientSession, urls, base_url:str, user:str, password: str, _) -> list:
    tasks = []
    for paths in urls:
        url = f'{base_url}{paths}'
        tasks.append(asyncio.create_task(fetch(session, url, user, password, _)))
    return tasks
    
def clean_data(raw_data:list):
    words_to_check = ["ClientError", "TimeoutError", "Exception", "Failed"]
    errors = []
    codes_200 = []
    codes_300 = []
    codes_400 = []
    codes_500 = []
    for i in raw_data:
        # checks if any of the words in the list is is found on that iteration and saves it on the errors list
        if any(word in i for word in words_to_check):
            errors.append(i)
        # get the first 3 digits of the str, converts to int and checks the code number to appends it the its corresponding list
        else:
            str_codes = i[:3]
            codes = int(str_codes)
            if codes >= 500:
                codes_500.append(i) 
            elif codes >= 400:
                codes_400.append(i)
            elif codes >= 300:
                codes_300.append(i)
            elif codes == 200:
                codes_200.append(i)
    dict_data = {'200 Codes':codes_200, '400 Codes':codes_400, '500 Codes':codes_500, 'Errors':errors}
    # checks the maximum length among all the lists in the dict_data
    max_length = max(len(lst) for lst in dict_data.values())
    # calculates difference between max lenght and current to append nan and make the length equal
    for key in dict_data:
        dict_data[key] = dict_data[key] + [np.nan] * (max_length - len(dict_data[key]))
    # creates dataframe
    df = pd.DataFrame(dict_data)
    # replace nan with empty space for better visualization on csv
    df = df.replace({np.nan: ''})
    # converts to csv
    df.to_csv('output.csv', index=False)

async def main(file_path:str,base_url:str,user:str,password:str):
    urls = load_urls(file_path)
    async with aiohttp.ClientSession(connector= aiohttp.TCPConnector(ssl=False, limit= 5)) as session:
        tasks = get_tasks(session, urls, base_url, user, password, len(urls))
        progress_bar = tqdm(total=len(urls), desc="Fetching and Cleaning", position=0, leave=True)
        results = []
        
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            progress_bar.update(1)
        clean_data(results)
        progress_bar.close()

if __name__ == "__main__":
    file_path = './user-data/updatedUris.json'
    base_url = f'https://google.com' #add you URL, ommit using the final rorward slash"/"
    user = '' #add Username
    password = '' #add Password
    asyncio.run(main(file_path,base_url,user,password))
    end = time.time()