import aiohttp
import asyncio
import argparse
import logging
import pathlib
import os

logger = logging.getLogger(__name__)


MIME_TYPES = {
    '.gif': 'image/gif',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
}
POST_IMAGES_PATH = 'http://some_sevice/images'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', default="./")
    return parser.parse_args()


def find_images(image_dir):
    absolute_path = pathlib.Path(image_dir).absolute()

    images = []
    for path in absolute_path.glob('**/*'):
        if path.suffix in MIME_TYPES:
            images.append(path)

    return images


async def send_image(path):
    form_data = aiohttp.FormData()

    file_name = path.name
    content_type = MIME_TYPES[path.suffix]
    field_name = path.stem
    form_data.add_field(
        field_name,
        path.read_bytes(),
        filename=file_name,
        content_type=content_type,
    )

    async with aiohttp.ClientSession() as session:
        resp = await session.post(POST_IMAGES_PATH, data=form_data)
        text = await resp.text()
        logger.info(
            'Server responed with status %s and text %s on file %s',
            resp.status,
            text,
            file_name,
        )


async def main(loop, args):
    images = find_images(args.image_dir)
    if not images:
        logger.info('No images found')
        return

    await asyncio.gather(*[send_image(path) for path in images])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = parse_args()
    loop.run_until_complete(main(loop, args))
