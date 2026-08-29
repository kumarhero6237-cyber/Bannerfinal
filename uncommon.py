#Made of love by Uncommon.exe
#Join @uncommoncore , @uncommoncoregc
#Credit Changer Fck Your Mom
#If You Change Your Mom Is se-x worker (maal)
#Credit Chor MAA KI CH-UT
#Made By Uncommon Credit : @uncommonexe
#Reuplode Without Credit Fck Your Mom
#OB54 LEAK

import io
import os
import asyncio
import base64
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, Union, BinaryIO
from concurrent.futures import ThreadPoolExecutor

import httpx
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# ================= ADJUSTMENT SETTINGS =================
AVATAR_ZOOM = 1.26
AVATAR_SHIFT_Y = 0
AVATAR_SHIFT_X = 0

BANNER_START_X = 0.25
BANNER_START_Y = 0.29
BANNER_END_X = 0.81
BANNER_END_Y = 0.65

BANNER_COLOR_FACTOR = 1.6
BANNER_BRIGHTNESS_FACTOR = 0.65
BANNER_CONTRAST_FACTOR = 1.8
BANNER_SHARPNESS_FACTOR = 3.0
AVATAR_SHARPNESS_FACTOR = 2.5

STROKE_NAME = 3
STROKE_GUILD = 2
STROKE_LEVEL = 3
# ======================================================

@asynccontextmanager
async def uncommon_lifespan(app: FastAPI) -> None:
    """
    Lifespan context manager for FastAPI application.
    Ensures clean shutdown of HTTP client and thread pool.
    """
    yield
    await uncommon_client.aclose()
    uncommon_process_pool.shutdown()

app = FastAPI(lifespan=uncommon_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= CONSTANTS =================
# UPDATED: New API endpoint with key parameter
INFO_API_URL = "https://india-dun-two.vercel.app//uc-info"

BASE64_CDN = "aHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL1NoYWhHQ3JlYXRvci9pY29uQG1haW4vUE5H"
CDN_URL = base64.b64decode(BASE64_CDN).decode("utf-8")

FONT_FILE = "arial_unicode_bold.otf"
FONT_CHEROKEE = "NotoSansCherokee.ttf"

uncommon_client = httpx.AsyncClient(
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=10.0,
    follow_redirects=True
)

uncommon_process_pool = ThreadPoolExecutor(max_workers=4)


# ================= HELPERS =================
def uncommon_load_unicode_font(size: int, font_file: str = FONT_FILE) -> ImageFont.FreeTypeFont:
    """
    Load a Unicode-compatible TrueType font at the given size.

    Args:
        size: Font size in points.
        font_file: Filename of the font to load.

    Returns:
        PIL ImageFont object; falls back to default font if loading fails.
    """
    try:
        font_path = os.path.join(os.path.dirname(__file__), font_file)
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()


async def uncommon_fetch_image_bytes(item_id: Optional[str]) -> Optional[bytes]:
    """
    Fetch image data from CDN for a given item ID.

    Args:
        item_id: String identifier of the image (e.g., avatar ID).

    Returns:
        Raw image bytes if successful, else None.
    """
    if not item_id or str(item_id) in ("0", "None"):
        return None
    try:
        resp = await uncommon_client.get(f"{CDN_URL}/{item_id}.png")
        if resp.status_code == 200:
            return resp.content
    except Exception:
        pass
    return None


def uncommon_bytes_to_image(img_bytes: Optional[bytes]) -> Image.Image:
    """
    Convert bytes to a PIL Image object.

    Args:
        img_bytes: Raw image bytes.

    Returns:
        RGBA PIL Image, or a blank transparent image if conversion fails.
    """
    if img_bytes:
        try:
            return Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        except Exception:
            pass
    return Image.new("RGBA", (100, 100), (0, 0, 0, 0))


def uncommon_process_banner_image(
    data: Dict[str, Any],
    avatar_bytes: Optional[bytes],
    banner_bytes: Optional[bytes],
    pin_bytes: Optional[bytes]
) -> io.BytesIO:
    """
    Generate the final banner image from fetched assets and player info.

    Args:
        data: Dictionary containing 'level', 'name', 'guild'.
        avatar_bytes: Raw avatar image bytes.
        banner_bytes: Raw banner image bytes.
        pin_bytes: Raw pin image bytes (unused but kept for consistency).

    Returns:
        BytesIO containing the final PNG image.
    """
    avatar_img = uncommon_bytes_to_image(avatar_bytes)
    banner_img = uncommon_bytes_to_image(banner_bytes)
    pin_img = uncommon_bytes_to_image(pin_bytes)

    level = str(data.get("level") or "0")
    name = str(data.get("name") or "Unknown")
    guild = str(data.get("guild") or "")

    TARGET_HEIGHT = 400

    # ---- Avatar processing ----
    zoom_size = int(TARGET_HEIGHT * AVATAR_ZOOM)
    avatar_img = avatar_img.resize((zoom_size, zoom_size), Image.LANCZOS)

    center = zoom_size // 2
    half = TARGET_HEIGHT // 2
    avatar_img = avatar_img.crop((
        center - half - AVATAR_SHIFT_X,
        center - half - AVATAR_SHIFT_Y,
        center + half - AVATAR_SHIFT_X,
        center + half - AVATAR_SHIFT_Y
    ))
    enhancer = ImageEnhance.Sharpness(avatar_img)
    avatar_img = enhancer.enhance(AVATAR_SHARPNESS_FACTOR)

    # ---- Banner processing ----
    enhancer = ImageEnhance.Color(banner_img)
    banner_img = enhancer.enhance(BANNER_COLOR_FACTOR)
    enhancer = ImageEnhance.Contrast(banner_img)
    banner_img = enhancer.enhance(BANNER_CONTRAST_FACTOR)
    enhancer = ImageEnhance.Brightness(banner_img)
    banner_img = enhancer.enhance(BANNER_BRIGHTNESS_FACTOR)

    banner_img = banner_img.rotate(3, expand=True)
    bw, bh = banner_img.size
    banner_img = banner_img.crop((
        bw * BANNER_START_X,
        bh * BANNER_START_Y,
        bw * BANNER_END_X,
        bh * BANNER_END_Y
    ))

    bw, bh = banner_img.size
    banner_img = banner_img.resize(
        (int(TARGET_HEIGHT * (bw / bh) * 2), TARGET_HEIGHT),
        Image.LANCZOS
    )
    enhancer = ImageEnhance.Sharpness(banner_img)
    banner_img = enhancer.enhance(BANNER_SHARPNESS_FACTOR)

    # ---- Composite ----
    final = Image.new("RGBA", (avatar_img.width + banner_img.width, TARGET_HEIGHT))
    final.paste(avatar_img, (0, 0))
    final.paste(banner_img, (avatar_img.width, 0))

    draw = ImageDraw.Draw(final)

    font_big = uncommon_load_unicode_font(125)
    font_big_c = uncommon_load_unicode_font(125, FONT_CHEROKEE)
    font_small = uncommon_load_unicode_font(95)
    font_small_c = uncommon_load_unicode_font(95, FONT_CHEROKEE)
    font_lvl = uncommon_load_unicode_font(50)

    def is_cherokee(ch: str) -> bool:
        return 0x13A0 <= ord(ch) <= 0x13FF or 0xAB70 <= ord(ch) <= 0xABBF

    # ---- Draw name ----
    x_name = avatar_img.width + 65
    y_name = 40
    cx = x_name
    for ch in name:
        f = font_big_c if is_cherokee(ch) else font_big
        draw.text(
            (cx, y_name),
            ch,
            font=f,
            fill="white",
            stroke_width=STROKE_NAME,
            stroke_fill="black"
        )
        cx += f.getlength(ch)

    # ---- Draw guild ----
    x_guild = avatar_img.width + 65
    y_guild = 220
    cx = x_guild
    for ch in guild:
        f = font_small_c if is_cherokee(ch) else font_small
        draw.text(
            (cx, y_guild),
            ch,
            font=f,
            fill="white",
            stroke_width=STROKE_GUILD,
            stroke_fill="black"
        )
        cx += f.getlength(ch)

    # ---- Pin (if available) ----
    if pin_img and pin_img.size != (100, 100):
        pin_img = pin_img.resize((130, 130))
        final.paste(pin_img, (0, TARGET_HEIGHT - 130), pin_img)

    # ---- Level label ----
    lvl = f"Lvl.{level}"
    bbox = draw.textbbox((0, 0), lvl, font=font_lvl)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    text_x = final.width - tw - 30
    text_y = TARGET_HEIGHT - th - 40

    draw.text(
        (text_x, text_y),
        lvl,
        font=font_lvl,
        fill="white",
        stroke_width=STROKE_LEVEL,
        stroke_fill="black"
    )

    out = io.BytesIO()
    final.save(out, "PNG")
    out.seek(0)
    return out


# ================= ROUTES =================
@app.get("/", response_class=HTMLResponse)
async def uncommon_home() -> HTMLResponse:
    """
    Serve the landing page with a UI for generating banners.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>.  RAMSAGAR   [HACKER] API</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background: #000;
                padding: 20px;
                margin: 0;
                position: relative;
            }

            body::before {
                content: '';
                position: fixed;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 40% 50%, rgba(180, 130, 50, 0.06), transparent 60%),
                            radial-gradient(circle at 70% 30%, rgba(255, 215, 0, 0.03), transparent 50%);
                pointer-events: none;
                z-index: 0;
            }

            .glass {
                max-width: 820px;
                width: 100%;
                padding: 45px 40px;
                background: rgba(8, 8, 8, 0.75);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-radius: 40px;
                border: 1px solid rgba(210, 180, 80, 0.25);
                box-shadow:
                    0 40px 100px rgba(0, 0, 0, 0.9),
                    inset 0 1px 0 rgba(255, 215, 0, 0.10),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.8),
                    0 0 80px rgba(210, 180, 80, 0.04);
                text-align: center;
                transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
                animation: floatIn 0.9s ease-out;
                position: relative;
                z-index: 1;
            }

            .glass:hover {
                transform: translateY(-8px) scale(1.01);
                border-color: rgba(210, 180, 80, 0.55);
                box-shadow:
                    0 50px 120px rgba(0, 0, 0, 0.95),
                    inset 0 1px 0 rgba(255, 215, 0, 0.2),
                    0 0 100px rgba(210, 180, 80, 0.08);
            }

            @keyframes floatIn {
                0% { opacity: 0; transform: scale(0.96) translateY(30px); }
                100% { opacity: 1; transform: scale(1) translateY(0); }
            }

            .title {
                font-size: 3.2rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                background: linear-gradient(135deg, #f5e6b0, #d4af37, #f5e6b0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 60px rgba(212, 175, 55, 0.15);
                margin-bottom: 4px;
            }

            .sub-brand {
                font-size: 0.9rem;
                font-weight: 300;
                color: rgba(210, 180, 80, 0.4);
                letter-spacing: 6px;
                text-transform: uppercase;
                margin-bottom: 28px;
                border-bottom: 1px solid rgba(210, 180, 80, 0.08);
                padding-bottom: 14px;
                display: inline-block;
            }

            .form-group {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 12px;
                margin: 10px 0 20px;
            }

            .form-group input {
                flex: 1 1 240px;
                padding: 14px 22px;
                border-radius: 60px;
                border: 1px solid rgba(210, 180, 80, 0.25);
                background: rgba(0, 0, 0, 0.5);
                color: #e8e0d0;
                font-size: 1rem;
                font-family: 'JetBrains Mono', monospace;
                outline: none;
                transition: border-color 0.3s, box-shadow 0.3s;
                backdrop-filter: blur(4px);
            }

            .form-group input:focus {
                border-color: #d4af37;
                box-shadow: 0 0 30px rgba(212, 175, 55, 0.1);
            }

            .form-group input::placeholder {
                color: rgba(200, 190, 170, 0.4);
            }

            .form-group button {
                padding: 14px 34px;
                border-radius: 60px;
                border: 1px solid #d4af37;
                background: rgba(212, 175, 55, 0.10);
                color: #f5e6b0;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                backdrop-filter: blur(4px);
                letter-spacing: 0.5px;
            }

            .form-group button:hover {
                background: rgba(212, 175, 55, 0.25);
                box-shadow: 0 0 40px rgba(212, 175, 55, 0.15);
                transform: scale(1.02);
            }

            .banner-preview {
                margin: 20px 0 10px;
                padding: 10px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 20px;
                border: 1px solid rgba(210, 180, 80, 0.10);
                min-height: 120px;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: all 0.3s ease;
            }

            .banner-preview img {
                max-width: 100%;
                border-radius: 12px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
            }

            .banner-preview .placeholder {
                color: rgba(200, 190, 170, 0.3);
                font-size: 1.1rem;
                letter-spacing: 1px;
            }

            .banner-preview .error {
                color: #ff6b6b;
                font-weight: 500;
            }

            .endpoint-box {
                margin: 12px 0 8px;
                padding: 12px 20px;
                background: rgba(0, 0, 0, 0.4);
                border-radius: 60px;
                border: 1px solid rgba(210, 180, 80, 0.12);
                display: inline-block;
                backdrop-filter: blur(4px);
            }

            .endpoint-box code {
                font-family: 'JetBrains Mono', monospace;
                color: #d4c8b0;
                font-size: 0.95rem;
                word-break: break-all;
            }

            .endpoint-box code span {
                color: #f5d06a;
            }

            .divider {
                border: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(210, 180, 80, 0.25), transparent);
                margin: 20px 0;
            }

            .credits {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 12px 30px;
                font-size: 1.05rem;
                color: rgba(200, 190, 175, 0.6);
            }

            .credits a {
                color: #d4af37;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s ease;
                border-bottom: 2px solid transparent;
                padding-bottom: 2px;
            }

            .credits a:hover {
                color: #f5e6b0;
                border-bottom-color: #d4af37;
                text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
            }

            .credits .channel a {
                color: #c0a86a;
            }

            .credits .channel a:hover {
                color: #f5d06a;
                border-bottom-color: #c0a86a;
            }

            @media (max-width: 600px) {
                .glass { padding: 25px 18px; }
                .title { font-size: 2.2rem; }
                .form-group input { flex: 1 1 100%; }
                .form-group button { width: 100%; }
                .endpoint-box code { font-size: 0.8rem; }
            }
        </style>
    </head>
    <body>
        <div class="glass">
            <div class="title"> RAMSAGAR    [HACKER] API</div>
            <div class="sub-brand">✦ Free Fire Banner Generator ✦</div>

            <!-- Form -->
            <div class="form-group">
                <input type="text" id="uidInput" placeholder="Enter UID (e.g. 11111111)" value="11111111">
                <button id="fetchBtn">✨ Generate</button>
            </div>

            <!-- Banner preview -->
            <div class="banner-preview" id="preview">
                <span class="placeholder">Enter a UID and click Generate</span>
            </div>

            <!-- API endpoint display -->
            <div class="endpoint-box">
                <code>API Endpoint <span>/uc-banner?uid=<span id="endpointUid">11111111</span></span></code>
            </div>

            <hr class="divider">

            <div class="credits">
                <span>⚜️ Made by <a href="https://t.me/RAMSAGAR_OFC" target="_blank">©️RAMSAGAR</a></span>
                <span class="channel">📢 Channel <a href="https://whatsapp.com/channel/0029VaEIdBk4yltWBFi0E711" target="_blank">WHATSAPP</a></span>
            </div>
        </div>

        <script>
            const uidInput = document.getElementById('uidInput');
            const fetchBtn = document.getElementById('fetchBtn');
            const preview = document.getElementById('preview');
            const endpointUid = document.getElementById('endpointUid');

            function updateEndpoint(uid) {
                endpointUid.textContent = uid || 'YOUR_UID';
            }

            function showError(msg) {
                preview.innerHTML = `<span class="error">❌ ${msg}</span>`;
            }

            function showPlaceholder() {
                preview.innerHTML = `<span class="placeholder">Enter a UID and click Generate</span>`;
            }

            function showImage(uid) {
                const img = document.createElement('img');
                img.src = `/uc-banner?uid=${encodeURIComponent(uid)}`;
                img.alt = 'Banner';
                img.onerror = function() {
                    showError('Failed to load banner. Check UID or try again.');
                };
                preview.innerHTML = '';
                preview.appendChild(img);
            }

            fetchBtn.addEventListener('click', function() {
                const uid = uidInput.value.trim();
                if (!uid) {
                    showError('Please enter a valid UID.');
                    return;
                }
                updateEndpoint(uid);
                showImage(uid);
            });

            // Auto‑generate on page load with default UID
            window.addEventListener('load', function() {
                const defaultUid = uidInput.value.trim();
                if (defaultUid) {
                    updateEndpoint(defaultUid);
                    showImage(defaultUid);
                }
            });

            // Update endpoint display when user types (optional)
            uidInput.addEventListener('input', function() {
                const uid = this.value.trim();
                if (uid) updateEndpoint(uid);
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/uc-banner")
async def uncommon_get_banner(uid: str) -> Response:
    """
    Generate and return a banner image for the given Free Fire UID.

    Args:
        uid: Free Fire player UID.

    Returns:
        PNG image response.
    """
    # Updated: use new API with key parameter
    url = f"{INFO_API_URL}?uid={uid}&key=RAM-SAGAR"
    try:
        resp = await uncommon_client.get(url)
        if resp.status_code != 200:
            raise HTTPException(502, f"Info API returned {resp.status_code}")
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch player info: {str(e)}")

    data = resp.json()

    # New API does not return a 'code' field; validate presence of basicInfo
    if "basicInfo" not in data:
        raise HTTPException(404, "Invalid response: missing basicInfo")

    basic_info = data.get("basicInfo", {})
    clan_info = data.get("clanBasicInfo", {})

    name = basic_info.get("nickname", "Unknown")
    level = basic_info.get("level", "0")
    guild = clan_info.get("clanName", "")

    avatar_id = basic_info.get("headPic")
    banner_id = basic_info.get("bannerId")
    pin_id = None  # Not used, kept for compatibility

    avatar_bytes, banner_bytes, pin_bytes = await asyncio.gather(
        uncommon_fetch_image_bytes(avatar_id),
        uncommon_fetch_image_bytes(banner_id),
        uncommon_fetch_image_bytes(pin_id),
    )

    img_buffer = await asyncio.get_event_loop().run_in_executor(
        uncommon_process_pool,
        uncommon_process_banner_image,
        {
            "level": level,
            "name": name,
            "guild": guild,
        },
        avatar_bytes,
        banner_bytes,
        pin_bytes,
    )

    return Response(img_buffer.getvalue(), media_type="image/png")


# ================= MAIN ENTRY POINT =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)

#By Uncommon.exe
#Join @uncommoncore , @uncommoncoregc
#Credit Changer Fck Your Mom
#If You Change Your Mom Is se-x worker (maal)
#Credit Chor MAA KI CH-UT
#Made By Uncommon Credit : @uncommonexe
#Reuplode Without Credit Fck Your Mom
#OB54 LEAK
