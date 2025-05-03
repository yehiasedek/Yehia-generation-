
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import textwrap
import os

# الإعدادات الافتراضية
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1349
DEFAULT_BG_COLOR = "#fdf8f2"
DEFAULT_TEXT_COLOR = "#5e1414"
DEFAULT_HIGHLIGHT_COLOR = "#1e6f5c"
DEFAULT_FONT_PATH = "fonts/Amiri-Regular.ttf"
DEFAULT_QURAN_FONT_PATH = "fonts/AmiriQuran-Regular.ttf"

st.set_page_config(layout="wide")
st.title("توليد صورة من نص عربي مشكول")

# إدخال النص
text_input = st.text_area("أدخل النص العربي بالكامل (مع التشكيل)", height=300)

# تشكيل تلقائي (placeholder فقط)
if st.button("تشكيل تلقائي"):
    st.warning("ميزة التشكيل التلقائي لم تُفعل بعد.")

# اختيار الخط
font_files = {
    "Amiri": DEFAULT_FONT_PATH,
    "Amiri Quran": DEFAULT_QURAN_FONT_PATH,
    "Noto Naskh Arabic": "fonts/NotoNaskhArabic-Regular.ttf",
    "DejaVu Sans": "fonts/DejaVuSans.ttf"
}
font_choice = st.selectbox("اختر الخط", list(font_files.keys()))
font_path = font_files[font_choice]

# أبعاد الصورة
preset_ratios = {"1:1": (1, 1), "3:4": (3, 4), "4:3": (4, 3)}
preset = st.selectbox("نسبة أبعاد جاهزة", list(preset_ratios.keys()))
base_on = st.radio("حساب النسبة بناءً على", ["العرض", "الارتفاع"])
custom_width = st.number_input("العرض", value=DEFAULT_WIDTH)
if base_on == "العرض":
    ratio = preset_ratios[preset]
    img_width = custom_width
    img_height = int(custom_width * ratio[1] / ratio[0])
else:
    ratio = preset_ratios[preset]
    img_height = custom_width
    img_width = int(custom_width * ratio[0] / ratio[1])

# ألوان
bg_color = st.color_picker("لون الخلفية", DEFAULT_BG_COLOR)
text_color = st.color_picker("لون النص", DEFAULT_TEXT_COLOR)
highlight_color = st.color_picker("لون التمييز", DEFAULT_HIGHLIGHT_COLOR)

# محاذاة
alignment = st.selectbox("محاذاة النص", ["وسط", "يمين", "يسار"])

# رفع صورة خلفية اختيارية
bg_image_file = st.file_uploader("اختياري: اختر صورة خلفية", type=["png", "jpg", "jpeg"])

# زر إنشاء الصورة
if st.button("إنشاء الصورة"):
    try:
        font_size = 48
        font = ImageFont.truetype(font_path, font_size)

        if bg_image_file:
            image = Image.open(bg_image_file).convert("RGBA")
            image = image.resize((img_width, img_height))
        else:
            image = Image.new("RGB", (img_width, img_height), bg_color)

        draw = ImageDraw.Draw(image)
        reshaped_text = arabic_reshaper.reshape(text_input)
        bidi_text = get_display(reshaped_text)
        lines = textwrap.wrap(bidi_text, width=40)

        y = 50
        for line in lines:
            display_line = get_display(arabic_reshaper.reshape(line))
            bbox = draw.textbbox((0, 0), display_line, font=font)
            width = bbox[2] - bbox[0]

            if alignment == "وسط":
                x = (img_width - width) // 2
            elif alignment == "يمين":
                x = img_width - width - 40
            else:
                x = 40

            if "الْيَقِينِ" in line and line.startswith("أَتَعْرِفُ"):
                parts = line.split("الْيَقِينِ", 1)
                pre = get_display(arabic_reshaper.reshape(parts[0]))
                post = get_display(arabic_reshaper.reshape(parts[1]))
                x_pos = x

                draw.text((x_pos, y), pre, font=font, fill=text_color)
                pre_width = draw.textbbox((x_pos, y), pre, font=font)[2]
                draw.text((x_pos + pre_width, y), get_display(arabic_reshaper.reshape("الْيَقِينِ")), font=font, fill=highlight_color)
                post_width = draw.textbbox((x_pos + pre_width, y), get_display(arabic_reshaper.reshape("الْيَقِينِ")), font=font)[2]
                draw.text((x_pos + pre_width + post_width, y), post, font=font, fill=text_color)
            else:
                draw.text((x, y), display_line, font=font, fill=text_color)

            y += font_size + 15

        st.image(image, caption="الصورة الناتجة")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
