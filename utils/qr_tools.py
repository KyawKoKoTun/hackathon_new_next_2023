import qrcode
import os


def generate_qr_code(data, file_name):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    directory = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'generated_qr_codes')
    file_path = os.path.join(directory, f"{file_name}.png")
    qr_img = qr.make_image(fill="black", back_color="white")
    qr_img.save(file_path)
    return file_name


if __name__ == '__main__':
    generate_qr_code('chair_93404727c8e3f212a9837338b2d355f3c7fbe54e187486725eaf1170bd4f5bc2', '93404727c8e3f212a9837338b2d355f3c7fbe54e187486725eaf1170bd4f5bc2.png')
