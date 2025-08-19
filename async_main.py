import aiohttp
import asyncio
import datetime as dt
import json
from typing import Dict, List, Optional, Tuple


async def read_sites() -> List[Dict]:
    """Read sites from JSON file asynchronously"""
    with open("sites.json", "r") as sjson:
        return json.load(sjson)


async def getXtreamInfo(
    session: aiohttp.ClientSession, site: str, username: str, password: str
) -> Optional[Tuple[dt.datetime, str]]:
    """Check Xtream API endpoint asynchronously with timeout handling"""
    url = f"{site}/player_api.php?username={username}&password={password}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            try:
                data = await response.json()

                for key in data:
                    if isinstance(data[key], dict):
                        if "exp_date" in data[key]:
                            exp_timestamp = int(data[key]["exp_date"])
                            exp_date = dt.datetime.fromtimestamp(exp_timestamp)
                            exp_string = exp_date.strftime("%d/%m/%Y")
                            result_line = (
                                f"::{exp_string}::=>{site}::{username}::{password}\n"
                            )
                            return (exp_date, result_line)

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
    session: aiohttp.ClientSession,
    site_data: Dict,
    results_list: List[Tuple[dt.datetime, str]],
) -> None:
    """Process a single site asynchronously and collect results"""
    for url, credentials in site_data.items():
        print(f"Checking {url}")

        tasks = []
        for username, password in credentials.items():
            tasks.append(getXtreamInfo(session, url, username, password))

        try:
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    results_list.append(result)
        except Exception as e:
            print(f"Error processing tasks for {url}: {str(e)}")


async def main():
    """Main async function"""
    try:
        xtreams = await read_sites()
        all_results = []  # List to store (datetime, result_line) tuples

        async with aiohttp.ClientSession() as session:
            tasks = [
                check_site(session, site_data, all_results) for site_data in xtreams
            ]
            await asyncio.gather(*tasks)

        # Sort results by date (descending order - newest first)
        all_results.sort(key=lambda x: x[0] if x else dt.datetime.min, reverse=True)

        # Write sorted results to file
        with open("working.txt", "w") as working:
            for exp_date, result_line in all_results:
                working.write(result_line)
                print(result_line.strip())  # Also print to console

    except Exception as e:
        print(f"Fatal error in main: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
