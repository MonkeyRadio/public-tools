from argparse import ArgumentParser

parser = ArgumentParser(
  add_help=True,
  prog='Monkey Mairlist Metadata Uploader',
  )
parser.add_argument(
  'port',
  type=int,
  help='port to open the server',
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
  '--cdn_url',
  type=str,
  help='CDN URL to use for cover',
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