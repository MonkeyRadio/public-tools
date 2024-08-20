import eyed3
import sys

class Image:
  def __init__(self, dict):
    self.dict = dict

  @property
  def artist_name(self) -> str:
    return self.dict["artist_name"]

  @property
  def album_name(self) -> str:
    return self.dict["album_name"]
  
  @property
  def picture_type(self) -> str:
    return self.dict["picture_type"]
  
  @property
  def image_data(self):
    return self.dict["image_data"]

def extract(filepath: str):
  try:
    audio_file = eyed3.load(filepath)
    album_name = audio_file.tag.album
    artist_name = audio_file.tag.artist
    for image in audio_file.tag.images:
        return Image({
          "artist_name": artist_name,
          "album_name": album_name,
          "image_data": image.image_data,
          "picture_type": image.picture_type
        })
    return None
  except Exception as e:
    return None
