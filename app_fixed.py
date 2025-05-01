
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

def create_image(title, body):
    width, height = 800, 1000
    bg1 = (255, 255, 240)
    bg2 = (245, 245, 220)

    image = Image.new("RGB", (width, height), bg1)
    for y in range(height):
        gradient = tuple(int(bg1[i] + (bg2[i] - bg1[i]) * y / height) for i in range(3))
        ImageDraw.Draw(image).line([(0, y), (width, y)], fill=gradient)

    draw = ImageDraw.Draw(image)
    font_path = os.path.join(os.path.dirname(__file__), "Amiri-Regular.ttf")
    title_font = ImageFont.truetype(font_path, 40)
    body_font = ImageFont.truetype(font_path, 30)

    reshaped_title = arabic_reshaper.reshape(title)
    reshaped_body = arabic_reshaper.reshape(body)
    displayed_title = get_display(reshaped_title)
    displayed_body = get_display(reshaped_body)

    bbox = draw.textbbox((0, 0), displayed_title, font=title_font)
    title_x = (width - (bbox[2] - bbox[0])) // 2
    title_y = 50
    body_x = 50
    body_y = title_y + 60

    draw.text((title_x, title_y), displayed_title, font=title_font, fill="black")
    for line in displayed_body.split("\n"):
        draw.text((body_x, body_y), line.strip(), font=body_font, fill="black")
        body_y += 40

    return image

st.set_page_config(page_title="توليد صورة عربية", layout="centered")
st.title("تطبيق توليد صورة مزخرفة")

title = st.text_input("العنوان:")
body = st.text_area("النص (مقسم إلى أسطر):")

if st.button("توليد الصورة"):
    img = create_image(title, body)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue())
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="image.png", mime="image/png")
