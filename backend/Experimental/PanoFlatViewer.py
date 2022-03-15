import sys, getopt

if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter

    tkinter = Tkinter  # I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk, ImageChops
import PIL


def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        # pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        pilImage = pilImage.resize((w, h), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w / 2, h / 2, image=image)
    root.mainloop()



def main(argv):
    left = 0
    top = 0
    right = 0
    bottom = 0
    imgPath=""
    try:
        opts, args = getopt.getopt(argv, "hl:t:r:b:i:", ["left=", "top=", "right=", "bottom=","image="])
    except getopt.GetoptError:
        print('Usage: -l <left> -t <top> -r <right> -b <bottom> -i <image_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: -l <left> -t <top> -r <right> -b <bottom> -i <image_path>')
            sys.exit()
        elif opt in ("-l", "--left"):
            left = int(arg)
        elif opt in ("-t", "--top"):
            top = int(arg)
        elif opt in ("-r", "--right"):
            right = int(arg)
        elif opt in ("-b", "--bottom"):
            bottom = int(arg)
        elif opt in ("-i", "--image"):
            imgPath = arg

    PIL.Image.MAX_IMAGE_PIXELS = 933120000

    img1 = Image.open(imgPath)
    imgWidth, imgHeight = img1.size

    im1 = img1.crop((left, top, right, imgHeight))


    showPIL(im1)


if __name__ == "__main__":
    main(sys.argv[1:])
