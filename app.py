
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

st.set_page_config(page_title="مولد صور للنصوص العربية", layout="centered")
st.title("تطبيق إنشاء صور مزخرفة للنصوص العربية")

# واجهة الإدخال
title = st.text_input("العنوان:")
body = st.text_area("النص الكامل (يمكن أن يحتوي على أسطر):")

st.markdown("### إعدادات الخط")
font_size_title = st.slider("حجم خط العنوان", 20, 100, 40)
font_size_body = st.slider("حجم خط النص", 20, 80, 30)
font_path = st.selectbox("اختر الخط:", ["DejaVuSans.ttf", "NotoNaskhArabic-Regular.ttf", "Arial.ttf"])

st.markdown("### الألوان")
text_color = st.color_picker("لون النص", "#000000")
bg_color_top = st.color_picker("لون خلفية البداية", "#FFFFF0")
bg_color_bottom = st.color_picker("لون خلفية النهاية", "#F5F5DC")

st.markdown("### إعدادات الصورة")
img_width = st.slider("عرض الصورة", 400, 1600, 800, step=100)
img_height = st.slider("ارتفاع الصورة", 400, 2000, 1000, step=100)

if st.button("توليد الصورة"):
    # إنشاء الصورة
    image = Image.new("RGB", (img_width, img_height), bg_color_top)
    draw = ImageDraw.Draw(image)
    for y in range(img_height):
        gradient = tuple(
            int(int(bg_color_top.lstrip("#")[i:i+2], 16) + (int(bg_color_bottom.lstrip("#")[i:i+2], 16) - int(bg_color_top.lstrip("#")[i:i+2], 16)) * y / img_height)
            for i in (0, 2, 4)
        )
        draw.line([(0, y), (img_width, y)], fill=gradient)

    # تحميل الخطوط
    try:
        title_font = ImageFont.truetype(font_path, font_size_title)
        body_font = ImageFont.truetype(font_path, font_size_body)
    except:
        st.error("تعذر تحميل الخط. تأكد من وجود الملف في مجلد المشروع.")
        st.stop()

    reshaped_title = arabic_reshaper.reshape(title)
    reshaped_body = arabic_reshaper.reshape(body)
    displayed_title = get_display(reshaped_title)
    displayed_body = get_display(reshaped_body)

    # توسيط العنوان
    title_bbox = title_font.getbbox(displayed_title)
    title_x = (img_width - (title_bbox[2] - title_bbox[0])) // 2
    title_y = 50
    draw.text((title_x, title_y), displayed_title, font=title_font, fill=text_color)

    # النص الأساسي
    body_y = title_y + font_size_title + 20
    for line in displayed_body.split("\n"):
        line_bbox = body_font.getbbox(line)
        body_x = (img_width - (line_bbox[2] - line_bbox[0])) // 2
        draw.text((body_x, body_y), line, font=body_font, fill=text_color)
        body_y += font_size_body + 10

    # عرض وتحميل الصورة
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.image(buf.getvalue())
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="image.png", mime="image/png")
