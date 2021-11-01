from PIL import Image
import urllib.request
import os


class ImageCropper:

    def crop_image(self, path, new_directory):
        cropped_size = (152, 152)
        files = os.listdir(path)
        for f in files:
            if f not in new_directory:
                print(f)
                i = Image.open(f'{path}/{f}')
                filename, extension = os.path.splitext(f)
                i.thumbnail(cropped_size)
                i.save(f"static/{new_directory}/{filename}{extension}")

class DBWriter:

    def write_to_db(self):
        pass

url = 'https://www.pngall.com/wp-content/uploads/7/Satan-PNG-Images.png'
pic = urllib.request.urlretrieve(url, f"static/img/hello-profile-pic.png")

im = Image.open(pic[0])
fn, ext = os.path.splitext(pic[0])
print(fn, ext)

crop = ImageCropper()
crop.crop_image('static/img', 'cropped-imgs')
print(os.listdir('static/img'))
