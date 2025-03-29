import asyncio
import os
import random
import uuid

import aiohttp


async def download_image(session, url, save_folder):
    try:
        async with session.get(url) as response:
            path = os.path.join(save_folder, str(uuid.uuid4()) + '.jpg')
            with open(path, 'wb') as f:
                f.write(await response.read())
    except Exception as e:
        print(f"Error downloading {url}: {e}")


async def download_images(num_images, save_folder):
    os.makedirs(save_folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_images):
            image_url = f"https://picsum.photos/500/500?random={random.randint(1, 100000)}"
            tasks.append(download_image(session, image_url, save_folder))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    num_images = int(input("Enter the number of images to download: "))
    save_folder = "artifacts/1_image/"
    asyncio.run(download_images(num_images, save_folder))
