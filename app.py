import streamlit as st from PIL import Image, ImageDraw, ImageFont import arabic_reshaper from bidi.algorithm import get_display import textwrap import os

=== إعداد الخطوط ===

FONT_PATHS = { "Amiri": "Amiri-Regular.ttf", "Amiri Quran": "AmiriQuran-Regular.ttf", "Noto Naskh": "NotoNaskhArabic-Regular.ttf", "DejaVu Sans": "DejaVuSans.ttf" }

التأكد من تحميل الخطوط المطلوبة

for name, path in FONT_PATHS.items(): if not os.path.isfile(path): st.error(f"الخط '{name}' غير موجود في المسار: {path}")

=== الإعدادات الجانبية ===

st.sidebar.title("إعدادات التصميم")

تحميل صورة خلفية اختيارية

bg_image = st.sidebar.file_uploader("رفع صورة كخلفية (اختياري)", type=["png", "jpg", "jpeg"])

اختيار الخط

font_name = st.sidebar.selectbox("اختر الخط", list(FONT_PATHS.keys()), index=1) title_font_path = FONT_PATHS[font_name] body_font_path = FONT_PATHS[font_name]

حجم الخط

title_font_size = st.sidebar.slider("حجم خط العنوان", 20, 100, 48) body_font_size = st.sidebar.slider("حجم خط النص", 16, 80, 36)

اختيار الألوان

title_color = st.sidebar.color_picker("لون العنوان", "#2e4739") body_color = st.sidebar.color_picker("لون النص", "#5f2c1e")

اختيار المحاذاة

alignment = st.sidebar.selectbox("محاذاة النص", ["يمين", "توسيط", "يسار"], index=0)

أبعاد الصورة

st.sidebar.markdown("### أبعاد الصورة") default_width = 1080 default_height = 1349

aspect_options = { "1:1": (1, 1), "3:4": (3, 4), "4:5": (4, 5), "2:3": (2, 3), "16:9": (16, 9), "9:16": (9, 16) } aspect_choice = st.sidebar.selectbox("اختر نسبة الأبعاد (اختياري)", ["بدون", *aspect_options.keys()])

use_aspect_by = None if aspect_choice != "بدون": use_aspect_by = st.sidebar.radio("اضبط النسبة بناءً على:", ["العرض", "الارتفاع"], index=0)

width = st.sidebar.number_input("العرض (px)", min_value=200, max_value=4000, value=default_width) height = st.sidebar.number_input("الارتفاع (px)", min_value=200, max_value=4000, value=default_height)

if aspect_choice != "بدون": ar, br = aspect_options[aspect_choice] if use_aspect_by == "العرض": height = int(width * br / ar) else: width = int(height * ar / br)

=== إدخال المحتوى ===

st.title("مولّد صور بالنصوص العربية") title_text = st.text_input("العنوان:", "أتعرف ما معنى اليقين بالله؟") body_text = st.text_area("النص:", """ اليقين بالله هو الذي يُحقّق المُستحيل، اليقين بالله هو تكون كل الأبواب مغلقة وكل الظروف صعبة وكل المؤشرات توحي بعكس ما تتمناه لكنك على يقين بأن الله سيصلح كل شيء. """)

if st.button("توليد الصورة"): # إعداد الصورة if bg_image: image = Image.open(bg_image).convert("RGB").resize((width, height)) else: image = Image.new("RGB", (width, height), color=(245, 235, 211))  # خلفية افتراضية

draw = ImageDraw.Draw(image)

# إعداد الخطوط
try:
    title_font = ImageFont.truetype(title_font_path, title_font_size)
    body_font = ImageFont.truetype(body_font_path, body_font_size)
except Exception as e:
    st.error(f"خطأ في تحميل الخط: {e}")
    st.stop()

# تنسيق النص بالعربية
def prepare_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

title_text = prepare_text(title_text)
body_lines = []

max_text_width = width - 100  # هامش داخلي
for line in body_text.split("\n"):
    prepared = prepare_text(line)
    wrapped = textwrap.wrap(prepared, width=60)
    body_lines.extend(wrapped if wrapped else [""])

# حساب مواضع الرسم
y = 100
title_width, title_height = draw.textsize(title_text, font=title_font)
if alignment == "توسيط":
    title_x = (width - title_width) // 2
elif alignment == "يسار":
    title_x = width - title_width - 50
else:  # يمين
    title_x = 50

draw.text((title_x, y), title_text, font=title_font, fill=title_color)
y += title_height + 40

for line in body_lines:
    line_width, line_height = draw.textsize(line, font=body_font)
    if alignment == "توسيط":
        x = (width - line_width) // 2
    elif alignment == "يسار":
        x = width - line_width - 50
    else:
        x = 50
    draw.text((x, y), line, font=body_font, fill=body_color)
    y += line_height + 10

st.image(image, caption="الصورة الناتجة", use_column_width=True)

# حفظ الصورة للتحميل
image.save("output.png")
with open("output.png", "rb") as file:
    st.download_button("تحميل الصورة", file, file_name="arabic_text_image.png", mime="image/png")

