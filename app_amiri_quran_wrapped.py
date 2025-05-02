
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import textwrap

st.set_page_config(page_title="مولد صور عربية", layout="centered")
st.title("مولد صور للنصوص العربية بخط Amiri Quran وتشكيل كامل")

title = st.text_input("العنوان (مُشكّل):")
body = st.text_area("النص الكامل (مُشكّل):")

font_size_title = st.slider("حجم خط العنوان", 24, 100, 44)
font_size_body = st.slider("حجم خط النص", 20, 80, 36)
text_color_title = st.color_picker("لون العنوان", "#3C5A4C")
text_color_body = st.color_picker("لون النص", "#7B3F3A")
bg_color = st.color_picker("لون الخلفية", "#F3E7D4")

img_width = 1080
img_height = 1350

def wrap_arabic_text(text, font, max_width, draw):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    words = bidi_text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = word + ' ' + line if line else word
        width = draw.textlength(test_line, font=font)
        if width <= max_width - 100:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

if st.button("توليد الصورة"):
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    try:
        font_path = "AmiriQuran-Regular.ttf"
        title_font = ImageFont.truetype(font_path, font_size_title)
        body_font = ImageFont.truetype(font_path, font_size_body)
    except Exception as e:
        st.error(f"فشل تحميل الخط: {e}")
        st.stop()

    # رسم العنوان
    reshaped_title = arabic_reshaper.reshape(title)
    displayed_title = get_display(reshaped_title)
    title_width = draw.textlength(displayed_title, font=title_font)
    title_x = (img_width - title_width) // 2
    title_y = 80
    draw.text((title_x, title_y), displayed_title, font=title_font, fill=text_color_title)

    # تقسيم النص الطويل
    body_lines = []
    for paragraph in body.split("\n"):
        body_lines.extend(wrap_arabic_text(paragraph.strip(), body_font, img_width, draw))

    # رسم النص
    y = title_y + font_size_title + 50
    for line in body_lines:
        line_width = draw.textlength(line, font=body_font)
        x = (img_width - line_width) // 2
        draw.text((x, y), line, font=body_font, fill=text_color_body)
        y += font_size_body + 10

    # عرض وتنزيل الصورة
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.image(buf.getvalue())
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="image.png", mime="image/png")
