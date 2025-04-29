
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_degree(degree):


    # Görsel boyutları
    width, height = 600, 100

    # Göstermek istediğimiz merkez derece
    center_deg = degree

    # Fonksiyon: dereceyi yön ismine çevir
    def deg_to_dir(deg):
        directions = {
            0: 'N',
            45: 'NE',
            90: 'E',
            135: 'SE',
            180: 'S',
            225: 'SW',
            270: 'W',
            315: 'NW'
        }
        deg = deg % 360
        if deg % 45 == 0:
            return directions[deg]
        return deg

    # Yeni boş görsel oluştur (siyah zemin)
    image = np.zeros((height, width, 4), dtype=np.uint8)

    # Her piksel başına kaç derece düşüyor (180 derece ekran genişliği)
    deg_per_pixel = 180 / width

    # Merkezdeki dereceye göre sol ve sağ sınırı hesapla
    start_deg = center_deg - 90

    # Çizim
    for x in range(width):
        current_deg = (start_deg + x * deg_per_pixel) % 360
        rounded_deg = int(round(current_deg))

        # Her 60 derecede bir büyük işaret ve sayı
        if rounded_deg % 45 == 0:
            cv2.line(image, (x, 30), (x, 70), (255, 255, 255,1), 2)
            label = f"{rounded_deg}"
            # cv2.putText(image, label, (x - 10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Eğer yön varsa ekle
            dir_text = deg_to_dir(rounded_deg)
            dir_text = str(dir_text)
            if dir_text:
                # OpenCV image to PIL image
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))
                draw = ImageDraw.Draw(pil_image)

                # Load Arial font
                font_path = "arial.ttf"  # Ensure the Arial font file is available in the same directory or provide the correct path
                font = ImageFont.truetype(font_path, 24)  # Reduced font size for thinner text

                # Draw text
                draw.text((x - 10, 75), dir_text, font=font, fill=(255, 255, 255,1))

                # Convert back to OpenCV image
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)
        elif rounded_deg % 15 == 0:
                    # Eğer yön varsa ekle
            dir_text = deg_to_dir(rounded_deg)
            dir_text = str(dir_text)
            # Küçük işaret (her 10 derecede bir)
            cv2.line(image, (x, 45), (x, 65), (150, 150, 150,1), 1)

            # OpenCV image to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))
            draw = ImageDraw.Draw(pil_image)

            # Load Arial font
            font_path = "arial.ttf"  # Ensure the Arial font file is available in the same directory or provide the correct path
            font = ImageFont.truetype(font_path, 18)

            # Draw text
            draw.text((x - 10, 75), dir_text, font=font, fill=(255, 255, 255,1))

            # Convert back to OpenCV image
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)

    # Merkezde 10 piksellik bir üçgen (kırmızı) ve 1 piksel siyah kenarlık
    triangle_points = np.array([
        (width // 2, height // 5),  # Üst nokta
        (width // 2 - 5, 0),  # Sol alt nokta
        (width // 2 + 5, 0)   # Sağ alt nokta
    ], np.int32)

    # Çizgi kenarlığı (siyah)
    cv2.polylines(image, [triangle_points], isClosed=True, color=(0, 0, 0), thickness=1)

    # Üçgenin içini doldur (beyaz)
    cv2.fillPoly(image, [triangle_points], (255, 255, 255))

    # # Görseli kaydet
    # output_path = "heading_indicator_317deg.png"
    # cv2.imwrite(output_path, image)

    # output_path
    return image
# Sonsuz döngü fonksiyonu
def loop_draw_degree():
    while True:
        for degree in range(0, 1):
            print(degree)
            # Dereceyi çiz
            image = draw_degree(degree)

            # Görseli göster
            cv2.imshow("Heading Indicator", image)

            # 0.1 saniye bekle
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basılırsa çık
                cv2.destroyAllWindows()
                return

loop_draw_degree()