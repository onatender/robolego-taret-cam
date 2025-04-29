import cv2
import numpy as np

def draw_angle_scale(angle, width=600, height=100):
    # Temel ayarlar
    min_angle, max_angle = -180, 180
    bar_thickness = 10
    marker_height = 20
    text_offset = 40

    # Görüntü oluştur
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (30, 30, 40)  # Arka plan rengi

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
    cv2.drawContours(img, [triangle_pts], 0, (255, 255, 255), -1)

    # Açı değeri metni
    angle_text = f"{angle:.1f}"
    cv2.putText(img, angle_text, (end_x + 10, bar_y + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return img

# Test
angle_value = 180
img = draw_angle_scale(angle_value)
cv2.imshow("Angle Scale", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
