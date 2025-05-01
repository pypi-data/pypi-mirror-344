# **Secure Proxy Client**

`Secure Proxy Client` bu xavfsiz va bepul proksi orqali ma'lumotlarni olish uchun `async` kutubxona. Foydalanish uchun **token** talab qilinadi.

## 📌 **Xususiyatlari**
✅ Xavfsiz **proxy** orqali so'rov yuborish  
✅ **Async** yordamida tezkor ishlash  
✅ Video va boshqa fayllarni yuklab olish imkoniyati  

---

## 🔧 **O'rnatish**

```bash
pip install secure_proxy
```

---

## 🚀 **Foydalanish**

📌 **Kutubxona asinxron ishlaydi**, shuning uchun `async` kod yozish talab qilinadi. Quyidagi misolda video yuklab olish va saqlash jarayoni ko'rsatilgan.

```python
import asyncio
import aiofiles
from secure_proxy import SecureProxyClient

# 🔑 Proxy tokeningizni shu yerga yozing
PROXY_TOKEN = "your-proxy-token"

# 📌 Yuklab olinadigan video URL manzili
VIDEO_URL = "https://your-video-url.com/video.mp4"

# 📁 Saqlanadigan fayl nomi
OUTPUT_FILE = "video.mp4"

async def download_video():
    """ Video yuklab olish va saqlash """
    client = SecureProxyClient(proxy_token=PROXY_TOKEN)
    
    print("📥 Yuklab olinmoqda...")

    # 🔗 Proxy orqali video faylni yuklab olish
    content, status = await client.request(url=VIDEO_URL)
    
    if status != 200:
        print(f"❌ Xatolik: HTTP {status}")
        return

    # 💾 Faylni saqlash
    async with aiofiles.open(OUTPUT_FILE, "wb") as f:
        await f.write(content)

    print(f"✅ Video muvaffaqiyatli yuklandi! ({OUTPUT_FILE})")

if __name__ == "__main__":
    asyncio.run(download_video())
```

---

## 🎯 **Xulosa**
🚀 **Secure Proxy Client** yordamida **async** uslubida xavfsiz va tezkor **proxy orqali so'rov yuborish**, fayllarni yuklab olish va saqlash mumkin.

✅ **Oson o'rnatish**  
✅ **Asinxron ishlash**  
✅ **Tezkor video yuklab olish**  

❗ **Token olish uchun administrator bilan bog'laning!**  

---

**🔗 Bog'lanish**  
📧 Email: `abdujalilov2629@gmail.com`  
💬 Telegram: [@abduvohid_dev](https://t.me/abduvohid_dev)

