import qrcode
import os


def generate(url, user):
    # Creating an instance of qrcode
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    return img.save(os.path.join("static", str(user) + ".png"))
