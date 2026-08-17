import os
import base64
import html

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def demo_svg(prompt, level):
    """Generate a local PromptLab illustration without any API."""

    prompt = (prompt or "").strip()
    p = prompt.lower()

    level = max(0, min(int(level), 3))

    backgrounds = [
        ("#7c3aed", "#111827"),
        ("#06b6d4", "#0f172a"),
        ("#f59e0b", "#451a03"),
        ("#ec4899", "#3b0764"),
    ]

    bg1, bg2 = backgrounds[level]

    elements = []

    # SUN / SUNSET
    if any(word in p for word in [
        "sun", "sunset", "sunrise", "golden hour", "warm"
    ]):
        elements.append(
            '<circle cx="570" cy="115" r="65" fill="#ffd166"/>'
        )

    # MOON
    if any(word in p for word in ["moon", "night", "nighttime"]):
        elements.append(
            '<circle cx="570" cy="105" r="48" fill="#f8fafc"/>'
            '<circle cx="590" cy="88" r="48" fill="#111827"/>'
        )

    # STARS
    if any(word in p for word in ["star", "stars", "night"]):
        for x, y, r in [
            (90, 90, 3),
            (170, 130, 4),
            (260, 70, 3),
            (360, 110, 4),
            (450, 65, 3),
            (650, 170, 4),
        ]:
            elements.append(
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff"/>'
            )

    # MOUNTAINS
    if any(word in p for word in [
        "mountain", "mountains", "hill", "hills"
    ]):
        elements.append(
            '<path d="M0 410 L150 220 L250 340 L360 180 '
            'L540 410Z" fill="#26364a"/>'
        )
        elements.append(
            '<path d="M360 180 L540 410 L720 260 L720 520 '
            'L0 520 L0 410Z" fill="#1e293b"/>'
        )

    # FOREST / TREES
    if any(word in p for word in [
        "forest", "tree", "trees", "pine"
    ]):
        for x, y, size in [
            (70, 300, 70),
            (150, 270, 90),
            (500, 280, 85),
            (610, 250, 100),
        ]:
            elements.append(
                f'<path d="M{x} {y+120} '
                f'L{x+size/2} {y} '
                f'L{x+size} {y+120}Z" fill="#123c35"/>'
            )
            elements.append(
                f'<rect x="{x+size/2-7}" y="{y+120}" '
                f'width="14" height="45" fill="#654321"/>'
            )

    # RIVER / LAKE / WATER
    if any(word in p for word in [
        "river", "lake", "water", "ocean", "sea"
    ]):
        elements.append(
            '<path d="M0 390 Q180 330 360 390 T720 390 '
            'L720 520 L0 520Z" fill="#1786a5"/>'
        )
        elements.append(
            '<path d="M80 420 Q180 400 280 420 T480 420" '
            'fill="none" stroke="#8be9fd" stroke-width="5" opacity=".7"/>'
        )

    # FLOWERS
    if any(word in p for word in [
        "flower", "flowers", "garden"
    ]):
        for x, y in [
            (150, 410),
            (220, 390),
            (430, 400),
            (500, 420),
        ]:
            elements.append(
                f'<circle cx="{x}" cy="{y}" r="9" fill="#ff6b9a"/>'
                f'<circle cx="{x+10}" cy="{y}" r="9" fill="#ffd166"/>'
                f'<circle cx="{x+5}" cy="{y-9}" r="9" fill="#f8fafc"/>'
                f'<rect x="{x+3}" y="{y+9}" width="5" '
                f'height="45" fill="#166534"/>'
            )

    # CLOUDS
    if any(word in p for word in [
        "cloud", "clouds", "sky"
    ]):
        elements.append(
            '<ellipse cx="170" cy="150" rx="65" ry="30" fill="#ffffff" opacity=".8"/>'
            '<ellipse cx="220" cy="140" rx="50" ry="35" fill="#ffffff" opacity=".8"/>'
            '<ellipse cx="125" cy="145" rx="45" ry="25" fill="#ffffff" opacity=".8"/>'
        )

    # HOUSE
    if any(word in p for word in [
        "house", "home", "building"
    ]):
        elements.append(
            '<rect x="270" y="300" width="180" height="140" '
            'fill="#f8fafc"/>'
            '<path d="M250 300 L360 210 L470 300Z" '
            'fill="#b91c1c"/>'
            '<rect x="330" y="355" width="55" height="85" '
            'fill="#7c2d12"/>'
            '<rect x="290" y="330" width="35" height="35" '
            'fill="#38bdf8"/>'
            '<rect x="395" y="330" width="35" height="35" '
            'fill="#38bdf8"/>'
        )

    # CAR
    if any(word in p for word in [
        "car", "vehicle", "automobile"
    ]):
        elements.append(
            '<rect x="250" y="370" width="220" height="65" rx="18" '
            'fill="#ef4444"/>'
            '<path d="M290 370 L325 325 L410 325 L445 370Z" '
            'fill="#dc2626"/>'
            '<circle cx="300" cy="440" r="25" fill="#111827"/>'
            '<circle cx="420" cy="440" r="25" fill="#111827"/>'
            '<circle cx="300" cy="440" r="10" fill="#94a3b8"/>'
            '<circle cx="420" cy="440" r="10" fill="#94a3b8"/>'
        )

    # PERSON
    if any(word in p for word in [
        "person", "people", "man", "woman", "boy", "girl", "human"
    ]):
        elements.append(
            '<circle cx="360" cy="250" r="42" fill="#f1c27d"/>'
            '<circle cx="360" cy="365" r="70" fill="#2563eb"/>'
            '<rect x="330" y="410" width="25" height="70" fill="#1e293b"/>'
            '<rect x="365" y="410" width="25" height="70" fill="#1e293b"/>'
        )

    # 3D EFFECT
    if "3d" in p or "three dimensional" in p:
        elements.append(
            '<ellipse cx="360" cy="455" rx="190" ry="25" '
            'fill="#000000" opacity=".2"/>'
        )

    # CINEMATIC FRAME
    if "cinematic" in p:
        elements.append(
            '<rect x="12" y="12" width="696" height="496" '
            'fill="none" stroke="#ffffff" stroke-width="14" '
            'opacity=".35"/>'
        )

    # If no recognizable subject was found
    if not elements:
        elements.append(
            '<circle cx="360" cy="245" r="105" '
            'fill="#f8fafc" opacity=".9"/>'
        )
        elements.append(
            '<circle cx="330" cy="225" r="12" fill="#7c3aed"/>'
            '<circle cx="390" cy="225" r="12" fill="#7c3aed"/>'
            '<path d="M320 275 Q360 310 400 275" '
            'fill="none" stroke="#7c3aed" stroke-width="8"/>'
        )

    safe_prompt = html.escape(prompt[:70])

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 720 520">'
    )

    svg += (
        '<defs>'
        '<linearGradient id="background" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{bg1}"/>'
        f'<stop offset="100%" stop-color="{bg2}"/>'
        '</linearGradient>'
        '</defs>'
    )

    svg += (
        '<rect width="720" height="520" '
        'fill="url(#background)"/>'
    )

    svg += "".join(elements)

    svg += (
        '<rect x="20" y="445" width="680" height="55" rx="14" '
        'fill="#000000" opacity=".35"/>'
        f'<text x="40" y="478" fill="white" font-size="18" '
        f'font-family="Arial">PromptLab • {safe_prompt}</text>'
        '</svg>'
    )

    encoded = base64.b64encode(svg.encode()).decode()

    return f"data:image/svg+xml;base64,{encoded}"


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}

    prompt = (data.get("prompt") or "").strip()

    if not prompt:
        return jsonify({
            "error": "Please enter a prompt."
        }), 400

    try:
        level = int(data.get("level", 0))
    except (TypeError, ValueError):
        level = 0

    level = max(0, min(level, 3))

    # PromptLab now works completely without OpenAI.
    image = demo_svg(prompt, level)

    return jsonify({
        "image": image,
        "mode": "local",
        "message": "Image generated locally by PromptLab.",
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "openai_configured": False,
        "image_model": "local-svg",
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=True,
    )
