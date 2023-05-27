from flask_qrcode import QRcode, SvgFragmentImage

qrc = QRcode()


def gen_qrcode(text):
    return qrc.qrcode(text, mode="raw", image_factory=SvgFragmentImage)
