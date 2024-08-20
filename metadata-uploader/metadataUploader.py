import os
import time
import requests
from argparse import ArgumentParser
import json
import time

def transform_metadata_trackNumber(metadata):
    try:
        metadata['trackNumber'] = int(metadata['trackNumber'])
    except ValueError:
        del metadata['trackNumber']

def transform_metadata_year(metadata):
    try:
        metadata['year'] = int(metadata['year'])
    except ValueError:
        del metadata['year']

def transform_metadata_type(metadata):
    match metadata['type']:
        case 'Music':
            metadata['type'] = 'single'
        case 'Musique':
            metadata['type'] = 'single'
        case _:
            metadata['type'] = 'mediamask'

def transform_metadata(metadata):
    transform_metadata_type(metadata)
    transform_metadata_year(metadata)
    transform_metadata_trackNumber(metadata)
    return metadata

def login(args):
    url = f'{args.api_url}/v4/auth/login'
    data = {'nickname': args.nickname, 'password': args.password}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['token']


def send_metadata(args):
    file_path = args.file_path
    token = login(args)
    url = f'{args.diffusion_api_url}/v1/metadata/current?radioId={args.radio_id}&contentId={args.content_id}'
    headers = {'Authorization': f'Bearer {token}'}
    with open(file_path, 'r') as file:
        metadata = file.read()
    data = json.loads(metadata)
    response = requests.post(url, headers=headers, json=transform_metadata(data))
    print(response.json())
    response.raise_for_status()
    print('Metadata sent successfully')

def detect_file_changes(args, interval=0.2):
    file_path = args.file_path
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            try:
              print('Metadata file has changed, sending metadata...')
              time.sleep(1)
              send_metadata(args)
            except (Exception, requests.HTTPError) as e:
              print(f'Error: {e}')
            last_modified = current_modified
        time.sleep(interval)


parser = ArgumentParser(
  add_help=True,
  prog='Monkey Mairlist Metadata Uploader',
  )
parser.add_argument(
  'file_path',
  type=str,
  help='File path to watch for changes',
  )
parser.add_argument(
  '--api_url',
  type=str,
  help='API URL to use for login',
  required=True,
  )
parser.add_argument(
  '--diffusion_api_url',
  type=str,
  help='API URL to use for metadata diffusion',
  required=True,
  )
parser.add_argument(
  '--nickname',
  type=str,
  help='Nickname to use for authentication',
  required=True,
  )
parser.add_argument(
  '--password',
  type=str,
  help='Password to use for authentication',
  required=True,
  )
parser.add_argument(
  '--radio_id',
  type=str,
  help='Radio ID to use for metadata',
  required=True,
  )
parser.add_argument(
  '--content_id',
  type=str,
  help='Content ID to use for metadata',
  required=True,
  )

args = parser.parse_args()
# Usage
detect_file_changes(args)