import cv2
import tkinter as tk
from tkinter import ttk
import threading
import datetime
import screeninfo
import numpy as np

def find_available_cameras(max_devices=10):
    available = []
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

def draw_vertical_angle_scale(angle, width=100, height=600):
    # Skala ayarları
    min_angle, max_angle = -180, 180
    bar_thickness = 10
    marker_width = 20
    text_offset = 40

    # Görüntü oluştur
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (0, 0, 0)  # Arka plan rengi

    # Skala pozisyonları
    start_y, end_y = height - 50, 50  # Y ekseni: yukarı artan
    bar_x = width // 2

    # Skala çizgisi
    cv2.line(img, (bar_x, start_y), (bar_x, end_y), (200, 200, 200), bar_thickness)

    # Orta çizgi
    mid_y = (start_y + end_y) // 2
    cv2.line(img, (bar_x - marker_width, mid_y), (bar_x + marker_width, mid_y), (180, 180, 180), 2)

    # Açıya göre konum hesapla
    scale_length = start_y - end_y
    relative_pos = int(((angle - min_angle) / (max_angle - min_angle)) * scale_length)
    angle_y = start_y - relative_pos

    # Üçgen işaretleyici (sağa bakan)
    triangle_pts = np.array([
        [bar_x + marker_width, angle_y],
        [bar_x + marker_width + 12, angle_y - 7],
        [bar_x + marker_width + 12, angle_y + 7]
    ])
    cv2.drawContours(img, [triangle_pts], 0, (255, 255, 255), -1)
    cv2.polylines(img, [triangle_pts], isClosed=True, color=(1, 1, 1), thickness=1)  # Kırmızı dış çizgiler

    # Açı değeri metni
    angle_text = f"{angle:.1f}"
    (text_width, text_height), baseline = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    text_x = width // 2 - 30
    text_y = 30
    fixed_width = 6 * 20  # 6 karakter uzunluğunda sabit genişlik (her karakter için yaklaşık 20 piksel)
    cv2.rectangle(img, 
                  (text_x - 5, text_y - text_height - baseline - 5), 
                  (text_x - 5 + fixed_width, text_y + baseline + 5), 
                  (1, 1, 1), 
                  -1)
    centered_text_x = text_x - 5 + (fixed_width - text_width) // 2
    cv2.putText(img, angle_text, (centered_text_x-25, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)


    return img
def draw_angle_scale(angle, width=600, height=100):
    # Temel ayarlar
    min_angle, max_angle = -180, 180
    bar_thickness = 10
    marker_height = 20
    text_offset = 40

    # Görüntü oluştur
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (0, 0, 0)  # Arka plan rengi

    # Skala pozisyonları
    bar_y = height // 2
    start_x, end_x = 50, width - 100


    # Skala çizgisi
    cv2.line(img, (start_x, bar_y), (end_x, bar_y), (200, 200, 200), bar_thickness)

    # Orta nokta
    mid_x = (start_x + end_x) // 2
    cv2.line(img, (mid_x, bar_y - marker_height), (mid_x, bar_y + marker_height), (180, 180, 180), 2)

    # Açı değerine göre konum hesapla
    scale_length = end_x - start_x
    relative_pos = int(((angle - min_angle) / (max_angle - min_angle)) * scale_length)
    angle_x = start_x + relative_pos

    # Üçgen işaretleyici
    triangle_pts = np.array([
        [angle_x, bar_y - marker_height],
        [angle_x - 7, bar_y - marker_height - 12],
        [angle_x + 7, bar_y - marker_height - 12]
    ])
    cv2.drawContours(img, [triangle_pts], 0, (255, 255, 255), -1)  # Beyaz dolgu
    cv2.polylines(img, [triangle_pts], isClosed=True, color=(1, 1, 1), thickness=1)  # Kırmızı dış çizgiler

    # Açı değeri metni
    angle_text = f"{angle:.1f}"
    (text_width, text_height), baseline = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    text_x = end_x + 20
    text_y = bar_y + 10
    fixed_width = 6 * 20  # 6 karakter uzunluğunda sabit genişlik (her karakter için yaklaşık 20 piksel)
    cv2.rectangle(img, 
                  (text_x - 5, text_y - text_height - baseline - 5), 
                  (text_x - 5 + fixed_width, text_y + baseline + 5), 
                  (1, 1, 1), 
                  -1)
    centered_text_x = text_x - 5 + (fixed_width - text_width) // 2
    cv2.putText(img, angle_text, (centered_text_x-18, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    return img

def draw_degree(degree):


    # Görsel boyutları
    width, height = 800, 100

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
    image = np.zeros((height, width, 3), dtype=np.uint8)

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
            cv2.line(image, (x, 30), (x, 70), (255, 255, 255), 2)
            label = f"{rounded_deg}"
            # cv2.putText(image, label, (x - 10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Eğer yön varsa ekle
            dir_text = deg_to_dir(rounded_deg)
            dir_text = str(dir_text)
            if dir_text:
                # OpenCV image to PIL image
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_image)

                # Load Arial font
                font_path = "arial.ttf"  # Ensure the Arial font file is available in the same directory or provide the correct path
                font = ImageFont.truetype(font_path, 16)

                # Draw text
                draw.text((x - 10, 75), dir_text, font=font, fill=(255, 255, 255))

                # Convert back to OpenCV image
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        elif rounded_deg % 15 == 0:
                    # Eğer yön varsa ekle
            dir_text = deg_to_dir(rounded_deg)
            dir_text = str(dir_text)
            # Küçük işaret (her 10 derecede bir)
            cv2.line(image, (x, 45), (x, 65), (150, 150, 150), 1)

            # OpenCV image to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)

            # Load Arial font
            font_path = "arial.ttf"  # Ensure the Arial font file is available in the same directory or provide the correct path
            font = ImageFont.truetype(font_path, 16)

            # Draw text
            draw.text((x - 10, 75), dir_text, font=font, fill=(255, 255, 255))

            # Convert back to OpenCV image
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

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

def draw_overlay(frame):
    height, width = frame.shape[:2]
    green = (0, 255, 0)
    red = (0, 0, 255)

    angle_scale_img = draw_angle_scale(display_data["X_ANGLE"])  # Örnek açı değeri
    scale_h, scale_w, _ = angle_scale_img.shape
    overlay = frame[0:scale_h + 0, (width - scale_w) // 2:(width + scale_w) // 2]
    mask = angle_scale_img > 0
    overlay[mask] = angle_scale_img[mask]

    angle_scale_img = draw_vertical_angle_scale(display_data["Y_ANGLE"])  # Örnek açı değeri
    scale_h, scale_w, _ = angle_scale_img.shape
    overlay = frame[70:scale_h+70, 0:scale_w]  # Ekranın soluna yasla
    mask = angle_scale_img > 0
    overlay[mask] = angle_scale_img[mask]

    text = "Mod: Termal\n" \
           f"Distance: {display_data['DISTANCE']}m\n" \
           "Lock: On"
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    lines = text.split("\n")
    max_line_width = max(cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0][0] for line in lines)
    box_width = max_line_width + 10
    box_height = (text_height + baseline) * len(lines) + 10
    cv2.rectangle(frame, (10, 10), (10 + box_width, 10 + box_height), (0, 0, 0), -1)
    for i, line in enumerate(lines):
        cv2.putText(frame, line, (15, 25 + i * (text_height + baseline)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (text_width, text_height), baseline = cv2.getTextSize(f"{now} UTC+3", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, 
                  (width - 300 - 5, 20 - text_height - baseline - 5), 
                  (width - 300 + text_width + 5, 20 + baseline + 5), 
                  (0, 0, 0), 
                  -1)
    cv2.putText(frame, f"{now} UTC+3", (width - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.arrowedLine(frame, (width - 60, 90), (width - 60, 60), red, 2, tipLength=0.5)
    cv2.putText(frame, "N", (width - 50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 1)

    cv2.rectangle(frame, (width - 130, height - 50), (width - 10, height - 0), (0, 0, 0), -1)
    cv2.putText(frame, f"{display_data['NORTH']}N", (width - 120, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"{display_data['EAST']}E", (width - 120, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Çembersel crosshair çiz
    center_x, center_y = width // 2, height // 2
    radius = 6
    thickness = 1
    color = (0, 255, 0)  # Yeşil renk
    cv2.circle(frame, (center_x, center_y), radius, color, thickness)
    cv2.line(frame, (center_x - radius, center_y), (center_x + radius, center_y), color, thickness)
    cv2.line(frame, (center_x, center_y - radius), (center_x, center_y + radius), color, thickness)

    # cv2.drawMarker(frame, (width // 2, height // 2), green, cv2.MARKER_CROSS, 20, 1)
    text = "Rounds: 50\nNamlu Yuklu\nAtis Hazir"
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    lines = text.split("\n")
    max_line_width = max(cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0][0] for line in lines)
    box_width = max_line_width + 10
    box_height = (text_height + baseline) * len(lines) - baseline   # Remove extra space
    cv2.rectangle(frame, (10, height - box_height - 20), (10 + box_width, height - 10), (0, 0, 0), -1)
    for i, line in enumerate(lines):
        cv2.putText(frame, line, (15, height - box_height - 5 + i * (text_height + baseline) + text_height-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    text = "ÇIKIŞ İÇİN (ESC)"
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, 
                  (width // 2 - 60, height // 2 + 200 - text_height - baseline), 
                  (width // 2 - 60 + text_width, height // 2 + 200 + baseline), 
                  (0, 0, 0), 
                  -1)
    # Use a compatible font for Turkish characters
    font_path = "arial.ttf"  # Ensure this font file exists in the working directory or provide a valid path
    font = cv2.FONT_HERSHEY_SIMPLEX  # Default fallback font

    try:
        font = ImageFont.truetype(font_path, 16)  # Load a TTF font for Turkish characters
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)
        draw.text((width // 2 - 60, height // 2 + 185), text, font=font, fill=(255, 255, 255))
        frame = np.array(pil_image)
    except ImportError:
        # Fallback to default OpenCV font if PIL is not available
        cv2.putText(frame, text, (width // 2 - 60, height // 2 + 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # for i, val in enumerate(["-2", "-1", "+0", "+1", "+2"]):
    #     cv2.putText(frame, val, (width // 2 - 60 + i * 30, height - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 1)

    # for i in range(4):
    #     cv2.putText(frame, f"--{15+i} -", (10, height // 2 - 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 1)

    return frame

def resize_with_aspect_ratio(image, screen_w, screen_h):
    h, w = image.shape[:2]
    scale = min(screen_w / w, screen_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))
    top = (screen_h - new_h) // 2
    bottom = screen_h - new_h - top
    left = (screen_w - new_w) // 2
    right = screen_w - new_w - left
    return cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0,0,0])

def run_camera(index):
    screen = screeninfo.get_monitors()[0]
    screen_w, screen_h = screen.width, screen.height

    cap = cv2.VideoCapture(index)

    cv2.namedWindow("Tam Ekran Arayüz", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Tam Ekran Arayüz", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            break
        print(frame.shape)
        frame = draw_overlay(frame)
        full_frame = resize_with_aspect_ratio(frame, screen_w, screen_h)
        cv2.imshow("Tam Ekran Arayüz", full_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

def start_gui():
    def on_button_click():
        selected_index = int(combo.get().split(" ")[-1])
        root.destroy()
        threading.Thread(target=run_camera, args=(selected_index,)).start()

    available = find_available_cameras()
    if not available:
        print("Kamera bulunamadi.")
        return

    global root
    root = tk.Tk()
    root.title("Kamera Sec")

    tk.Label(root, text="Kamera Seciniz:").pack(padx=10, pady=10)

    combo = ttk.Combobox(root, values=[f"Kamera {i}" for i in available], state="readonly")
    combo.current(0)
    combo.pack(padx=10, pady=5)

    start_button = tk.Button(root, text="Başlat", command=on_button_click)
    start_button.pack(padx=10, pady=10)

    root.mainloop()

import time
import random
from PIL import ImageFont, ImageDraw, Image

display_data = {
    "NORTH": 42.3682,
    "EAST": 26.1151,
    "DISTANCE": 120,
    "X_ANGLE": 0,
    "Y_ANGLE": 60
}

def update_angle():
    global display_data
    while True:
        for angle in range(-180, 181, 30):
            display_data["X_ANGLE"] = angle
            display_data["Y_ANGLE"] = angle
            display_data["NORTH"] = round(random.uniform(0, 180), 4)
            display_data["EAST"] = round(random.uniform(0, 180), 4)
            display_data["DISTANCE"] = round(random.uniform(0, 150), 2)
            time.sleep(0.5)

threading.Thread(target=update_angle, daemon=True).start()
start_gui()
