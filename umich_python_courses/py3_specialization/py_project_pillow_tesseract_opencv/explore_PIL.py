import PIL
from PIL import Image, ImageFont, ImageDraw, ImageChops

# read image and convert to RGB
src: Image.Image = Image.open("mt_flowers.jpg")
image = src.convert('RGB')
font = ImageFont.truetype('arial.ttf', 26)


def writeTxtOnImage(mode, width, txt, foregrnd_color, bkgrnd_color, font):
    """ Write txt in a horizontal band of specified width
        and height is specified by size of font
        mode - Image mode (e.g. 'RGB")
        width: width in px
        txt - a string to print
        foregrnd_color, bkgrnd_color - fill colors
        font - ImageFont to use for txt
     """
    txt_box = Image.new(mode, (width, int(font.getsize(txt)[1]*1.1)), bkgrnd_color)
    draw = ImageDraw.Draw(txt_box, txt_box.mode)
    draw.text((0, 0), txt, fill=foregrnd_color, font=font)
    return txt_box


def applyColorFilter(im, chan, intensity):
    """ Returns an image that has the specified color channel attenuated
    chan: [0, 1, 2] corresponds to a channel in (R,G,B)
    intensity: ranges from 0 to 1 a percentage on how strongly the chan is attenuated
    0 means the channel is completely eliminated, and 1 means chan unchanged
    return modified image """

    if intensity < 0 or intensity > 1:
        raise ValueError("intensity should be in range [0, 1]")
    if chan < 0 or chan > 3:
        raise ValueError("chan should be in range [1, 3]")

    color = [255, 255, 255]
    color[chan] = int(color[chan] * intensity)
    color_filt = Image.new(im.mode, im.size, tuple(color))
    return ImageChops.multiply(im, color_filt)


# build a list of 9 images which have different color filters
images = []
channels = list(range(3))
filt_intensity = (0.1, 0.5, 0.9)
for chan in channels:
    for intensity in filt_intensity:
        txt = "channel {} intensity {}".format(chan, intensity)
        txt_box = writeTxtOnImage(image.mode, image.width, txt, "white", "black", font)
        im = Image.new(image.mode, (image.width, image.height + txt_box.height))
        im.paste(image)
        im.paste(txt_box, (0, image.height))
        images.append(applyColorFilter(im, chan, intensity))


# create a contact sheet from different brightnesses
first_image = images[0]
contact_sheet = PIL.Image.new(first_image.mode, (first_image.width*3, first_image.height*3))
x = 0
y = 0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y))
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x = 0
        y = y+first_image.height
    else:
        x = x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2), int(contact_sheet.height/2)))
contact_sheet.show()

