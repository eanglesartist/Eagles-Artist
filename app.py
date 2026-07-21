import streamlit as st
from openai import OpenAI
import replicate
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

# --- ១. កំណត់ការរៀបចំទំព័រ ---
st.set_page_config(page_title="AI Creative Studio", page_icon="🎬", layout="wide")

# --- ២. ការគ្រប់គ្រង API Keys (សុវត្ថិភាព) ---
# អ្នកអាចដាក់ Key ផ្ទាល់នៅទីនេះសម្រាប់តេស្ត ឬប្រើ st.secrets
OPENAI_KEY = st.sidebar.text_input("បញ្ចូល OpenAI API Key:", type="password")
REPLICATE_KEY = st.sidebar.text_input("បញ្ចូល Replicate API Token:", type="password")

if not OPENAI_KEY or not REPLICATE_KEY:
    st.info("💡 សូមបញ្ចូល API Keys នៅរបារចំហៀងខាងឆ្វេង ដើម្បីចាប់ផ្តើមដំណើរការ។")
    st.stop()

client = OpenAI(api_key=OPENAI_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_KEY

# --- ៣. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI) ---
st.title("🎬 AI Multi-Creative Studio")
st.write("បង្កើតរូបភាព រចនា Poster និងបំប្លែងទៅជាវីដេអូ ក្នុងកន្លែងតែមួយ!")

# បង្កើត Columns សម្រាប់បែងចែកការងារ
col_input, col_output = st.columns([1, 1])

with col_input:
    st.header("🎨 ១. បង្កើតរូបភាព")
    image_prompt = st.text_area("រៀបរាប់ពីរូបភាពដែលអ្នកចង់បាន:", placeholder="ឧទាហរណ៍: រូបភាពភ្នំដែលមានពន្លឺព្រះអាទិត្យពណ៌មាស...")
    
    st.header("✍️ ២. បន្ថែមអក្សរលើ Poster")
    poster_text = st.text_input("វាយអក្សរសម្រាប់ដាក់លើរូបភាព:")
    t1, t2 = st.columns(2)
    with t1:
        text_color = st.color_picker("ពណ៌អក្សរ", "#FFFFFF")
    with t2:
        text_size = st.slider("ទំហំអក្សរ", 20, 200, 80)

    generate_btn = st.button("🚀 ចាប់ផ្តើមបង្កើត Poster")

# --- ៤. ដំណើរការបង្កើតរូបភាព និង Poster ---
if generate_btn:
    if not image_prompt:
        st.warning("សូមបញ្ចូលការពិពណ៌នារូបភាព!")
    else:
        with st.spinner("កំពុងបង្កើតរូបភាពដោយ AI..."):
            try:
                # ១. បង្កើតរូបភាពជាមួយ DALL-E 3
                response = client.images.generate(
                    model="dall-e-3", prompt=image_prompt, size="1024x1024", n=1
                )
                img_url = response.data[0].url
                
                # ២. ទាញយករូបភាព និងបន្ថែមអក្សរ
                res = requests.get(img_url)
                img = Image.open(BytesIO(res.content))
                
                if poster_text:
                    draw = ImageDraw.Draw(img)
                    # ប្រើ Font លំនាំដើម (អ្នកអាចប្តូរដាក់ Font ខ្មែរបានបើមាន file .ttf)
                    try:
                        font = ImageFont.truetype("arial.ttf", text_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # ដាក់អក្សរនៅកណ្តាល
                    w, h = img.size
                    bbox = draw.textbbox((0, 0), poster_text, font=font)
                    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text(((w - tw) / 2, 100), poster_text, fill=text_color, font=font)

                # រក្សាទុករូបភាពក្នុង Session ដើម្បីប្រើសម្រាប់ Video
                st.session_state['current_img'] = img
                st.session_state['img_url'] = img_url
                st.success("Poster ត្រូវបានបង្កើតរួចរាល់!")
            except Exception as e:
                st.error(f"កំហុស: {e}")

# --- ៥. បង្ហាញលទ្ធផល និងបង្កើតវីដេអូ ---
with col_output:
    if 'current_img' in st.session_state:
        st.header("🖼️ លទ្ធផល Poster")
        st.image(st.session_state['current_img'], use_column_width=True)
        
        # ប៊ូតុងទាញយករូបភាព
        buf = BytesIO()
        st.session_state['current_img'].save(buf, format="PNG")
        st.download_button("⬇️ ទាញយករូបភាព PNG", buf.getvalue(), "poster.png", "image/png")

        st.divider()

        # ៦. ផ្នែកបង្កើតវីដេអូ
        st.header("🎥 ៣. បំប្លែងទៅជាវីដេអូ")
        st.write("ប្រើ AI ដើម្បីធ្វើឱ្យរូបភាពខាងលើមានចលនា (Video ៥ វិនាទី)")
        
        if st.button("🎬 បង្កើតវីដេអូឥឡូវនេះ"):
            with st.spinner("កំពុងបំប្លែងរូបភាពទៅជាវីដេអូ (ចំណាយពេលប្រហែល ១ នាទី)..."):
                try:
                    # ប្រើ Stable Video Diffusion តាម Replicate
                    output = replicate.run(
                        "stability-ai/stable-video-diffusion:3f045789",
                        input={"input_image": st.session_state['img_url']}
                    )
                    st.video(output)
                    st.success("វីដេអូត្រូវបានបង្កើតរួចរាល់!")
                except Exception as e:
                    st.error(f"មិនអាចបង្កើតវីដេអូបានទេ: {e}")