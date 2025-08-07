import aiohttp
import asyncio
import datetime as dt
import json
from typing import Dict, List, Optional


async def read_sites() -> List[Dict]:
    """Read sites from JSON file asynchronously"""
    with open("sites.json", "r") as sjson:
        return json.load(sjson)


async def getXtreamInfo(
    session: aiohttp.ClientSession, site: str, username: str, password: str
) -> Optional[str]:
    """Check Xtream API endpoint asynchronously with timeout handling"""
    url = f"{site}/player_api.php?username={username}&password={password}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            try:
                data = await response.json()

                for key in data:
                    if isinstance(data[key], dict):
                        if "exp_date" in data[key]:
                            exp_date = dt.datetime.fromtimestamp(
                                int(data[key]["exp_date"])
                            )
                            exp_string = exp_date.strftime("%d/%m/%Y")
                            return (
                                f"::{exp_string}::=>::{site}::{username}::{password}\n"
                            )

            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON Error for {url}: {str(e)}")
                return None

    except asyncio.TimeoutError:
        print(f"Timeout occurred while accessing {url}")
        return None
    except aiohttp.ClientError as e:
        print(f"Connection error for {url}: {str(e)}")
        return None


async def check_site(
    session: aiohttp.ClientSession, site_data: Dict, working_file
) -> None:
    """Process a single site asynchronously"""
    for url, credentials in site_data.items():
        print(f"Checking {url}")
        working_file.write(f"{url}\n")

        tasks = []
        for username, password in credentials.items():
            tasks.append(getXtreamInfo(session, url, username, password))

        try:
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    print(result)
                    working_file.write(result)
        except Exception as e:
            print(f"Error processing tasks for {url}: {str(e)}")


async def main():
    """Main async function"""
    try:
        xtreams = await read_sites()

        async with aiohttp.ClientSession() as session:
            with open("working.txt", "w") as working:
                tasks = [
                    check_site(session, site_data, working) for site_data in xtreams
                ]
                await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Fatal error in main: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
