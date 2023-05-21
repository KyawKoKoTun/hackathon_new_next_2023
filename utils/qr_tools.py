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
    generate_qr_code('chair_22716fd7bbb6ab5efb883a9fe8444a0a3ae384a84b29310512cfd7d8db431b7b', '22716fd7bbb6ab5efb883a9fe8444a0a3ae384a84b29310512cfd7d8db431b7b.png')