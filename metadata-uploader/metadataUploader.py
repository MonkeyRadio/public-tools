import requests
import json
import pictureExtractor

def transform_metadata_trackNumber(metadata):
    try:
        metadata['trackNumber'] = int(metadata['trackNumber'])
    except ValueError:
        del metadata['trackNumber']

def transform_metadata_duration(metadata):
    try:
        metadata['duration'] = int(metadata['duration'])
    except ValueError:
        del metadata['duration']

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
    transform_metadata_duration(metadata)
    return metadata

def login(args):
    url = f'{args.api_url}/v4/auth/login'
    data = {'nickname': args.nickname, 'password': args.password}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['token']

def send_cover(metadata, token, args):
    headers = {'Authorization': f'Bearer {token}'}
    if 'internalId' in metadata:
        url = f'{args.cdn_url}/radio-{args.radio_id}/{metadata["internalId"]}'
        response = requests.get(url)
        if response.status_code == 404 and 'filePath' in metadata:
            extracted_images = pictureExtractor.extract(metadata["filePath"])
            if extracted_images is None:
                return
            url = f'{args.api_url}/v4/cover/{args.radio_id}/{metadata["internalId"]}'
            files = {"file": (metadata["internalId"], extracted_images.image_data, 'image/jpeg')}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()

def send_metadata(args, data):
    token = login(args)
    url = f'{args.diffusion_api_url}/v1/metadata/current?radioId={args.radio_id}&contentId={args.content_id}'
    headers = {'Authorization': f'Bearer {token}'}
    try:
      send_cover(data, token, args)
    except (Exception, requests.HTTPError) as e:
      print(f'Cannot Send Cover Error: {e}')
    response = requests.post(url, headers=headers, json=transform_metadata(data))
    print(response.json())
    response.raise_for_status()
    print('Metadata sent successfully')
