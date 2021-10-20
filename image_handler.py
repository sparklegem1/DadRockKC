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
# im.save(f'static/img/{fn}.png')
crop = ImageCropper()
crop.crop_image('static/img', 'cropped-imgs')
print(os.listdir('static/img'))
# crop = ImageCropper()
# crop.crop_image('static/img', 'cropped-imgs')
# im_dim =  (756, 960)

# width, height = im.size
# print(im.size)
#
# xcenter = im.size / 2
# # Setting the points for cropped image
# x1 = xcenter - 100
# y1 =
# x2 = xcenter + 100
# y2 = 800
#
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((x1, y1, x2, y2))
# newsize = (152, 152)
# im1 = im1.resize(newsize)
# # Shows the image in image viewer
# im1.show()