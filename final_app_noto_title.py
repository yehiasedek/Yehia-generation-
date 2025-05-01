
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

st.set_page_config(page_title="مولد صور مزخرفة للنصوص العربية", layout="centered")
st.title("صانع صور للنصوص العربية")

title = st.text_input("العنوان:")
body = st.text_area("النص الكامل (يمكن أن يحتوي على أسطر):")

apply_tashkeel = st.checkbox("تشكيل النص تلقائيًا (محاكاة)", value=False)
if apply_tashkeel:
    title += "َ"
    body += "َ"

st.markdown("### إعدادات الخط والألوان")
font_size_title = st.slider("حجم خط العنوان", 20, 100, 44)
font_size_body = st.slider("حجم خط النص", 20, 80, 36)
title_color = st.color_picker("لون العنوان", "#3C5A4C")
body_color = st.color_picker("لون النص", "#7B3F3A")
bg_color = st.color_picker("لون الخلفية", "#F3E7D4")

# خيارات الخطوط للنص الأساسي
font_options = {
    "DejaVu Sans": "DejaVuSans.ttf",
    "Noto Naskh Arabic": "NotoNaskhArabic-Regular.ttf",
    "Arial": "Arial.ttf",
    "Amiri": "Amiri-Regular.ttf",
    "Amiri Quran": "AmiriQuran-Regular.ttf"
}
selected_font_name = st.selectbox("اختر خط النص:", list(font_options.keys()))
font_path_body = font_options[selected_font_name]
font_path_title = "NotoNaskhArabic-VariableFont_wght.ttf"

st.markdown("### إعدادات الصورة")
img_width = st.slider("عرض الصورة", 600, 1600, 1080, step=100)
img_height = st.slider("ارتفاع الصورة", 600, 2000, 1350, step=100)
alignment = st.selectbox("محاذاة النص:", ["وسط", "يمين", "يسار"])

if st.button("توليد الصورة"):
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype(font_path_title, font_size_title)
    except Exception as e:
        st.error(f"خطأ في تحميل خط العنوان: {font_path_title} - {e}")
        st.stop()

    try:
        body_font = ImageFont.truetype(font_path_body, font_size_body)
    except Exception as e:
        st.error(f"خطأ في تحميل خط النص: {font_path_body} - {e}")
        st.stop()

    reshaped_title = arabic_reshaper.reshape(title)
    reshaped_body = arabic_reshaper.reshape(body)
    displayed_title = get_display(reshaped_title)
    displayed_body = get_display(reshaped_body)

    title_bbox = title_font.getbbox(displayed_title)
    title_width = title_bbox[2] - title_bbox[0]
    if alignment == "وسط":
        title_x = (img_width - title_width) // 2
    elif alignment == "يمين":
        title_x = img_width - title_width - 50
    else:
        title_x = 50
    title_y = 80
    draw.text((title_x, title_y), displayed_title, font=title_font, fill=title_color)

    body_y = title_y + font_size_title + 40
    for line in displayed_body.split("\n"):
        line_bbox = body_font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        if alignment == "وسط":
            body_x = (img_width - line_width) // 2
        elif alignment == "يمين":
            body_x = img_width - line_width - 50
        else:
            body_x = 50
        draw.text((body_x, body_y), line, font=body_font, fill=body_color)
        body_y += font_size_body + 10

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.image(buf.getvalue())
    st.download_button("تحميل الصورة", buf.getvalue(), file_name="image.png", mime="image/png")
