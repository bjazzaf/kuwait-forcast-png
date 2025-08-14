
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import qrcode

# Sample forecast data for 4 locations (static for demo)
forecast_data = [
    {"location": "Qaruh", "temp": (31, 36), "wind": 22, "dir": "↗ NE", "wave": (0.8, 2.3), "humidity": (58, 71)},
    {"location": "Umm Al-Maradim", "temp": (30, 35), "wind": 19, "dir": "↑ N", "wave": (0.5, 1.9), "humidity": (55, 68)},
    {"location": "Kubbar", "temp": (32, 37), "wind": 24, "dir": "→ E", "wave": (1.1, 2.7), "humidity": (60, 74)},
    {"location": "Az Zawr", "temp": (30, 34), "wind": 17, "dir": "↖ NW", "wave": (0.3, 1.2), "humidity": (52, 66)},
]

# Map wave height to sea state
def sea_state(min_ft, max_ft):
    avg = (min_ft + max_ft) / 2
    if avg <= 1.5:
        return "Calm", "#EAF4E2"
    elif avg <= 3.9:
        return "Moderate", "#EAF4E2"
    elif avg <= 6.5:
        return "Rough", "#FCE6D3"
    else:
        return "Very Rough", "#FCE6D3"

# Determine condition based on wind + waves
def condition(wind, max_wave):
    if wind < 25 and max_wave < 3:
        return "Safe", "#EAF4E2"
    return "Avoid", "#FCE6D3"

# Draw forecast table as PNG
def draw_forecast(image_name):
    width, height = 1200, 600
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 18)

    title = "Marine & Weather Forecast"
    draw.text((width // 2 - 160, 20), title, font=font, fill="black")
    subtitle = datetime.utcnow().strftime("(%A - %B %d, %Y)")
    draw.text((width // 2 - 130, 50), subtitle, font=font, fill="black")

    headers = ["Location", "Temp (°C)", "Wind (km/h)", "Dir", "Wave (ft)", "Sea State", "Humidity (%)", "Condition"]
    x, y = 50, 100
    cell_w = 140
    draw.rectangle([x, y, x + len(headers)*cell_w, y + 40], fill="#D9EDF7")
    for i, h in enumerate(headers):
        draw.text((x + i * cell_w + 5, y + 10), h, font=font, fill="black")

    for idx, row in enumerate(forecast_data):
        y_offset = y + 40 + idx * 40
        wave_str = f"{row['wave'][0]}–{row['wave'][1]}"
        temp_str = f"{row['temp'][0]}–{row['temp'][1]}"
        hum_str = f"{row['humidity'][0]}–{row['humidity'][1]}"
        state, bg = sea_state(*row['wave'])
        cond, bg = condition(row["wind"], row["wave"][1])
        row_data = [
            row["location"], temp_str, str(row["wind"]), row["dir"],
            wave_str, state, hum_str, cond
        ]
        draw.rectangle([x, y_offset, x + len(headers)*cell_w, y_offset + 40], fill=bg)
        for i, val in enumerate(row_data):
            draw.text((x + i * cell_w + 5, y_offset + 10), val, font=font, fill="black")

    # Note section
    draw.text((x, y_offset + 60), "**Note:** Sea Current: Upwelling", font=font, fill="black")

    # QR Code
    qr = qrcode.make("https://bjazzaf.github.io/kuwait-forecast-png/")
    qr = qr.resize((100, 100))
    img.paste(qr, (width - 120, height - 120))

    # Watermark
    stamp = datetime.utcnow().strftime("Generated: %Y-%m-%d %H:%M UTC")
    draw.text((10, height - 30), stamp, font=font, fill="gray")

    # EXIF metadata
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Author", "bjazzaf")
    meta.add_text("Software", "forecast_generator.py")
    meta.add_text("DateTimeOriginal", datetime.utcnow().isoformat())

    img.save(image_name, pnginfo=meta)
    print(f"Saved {image_name}")

# Create both forecast images
draw_forecast("forecast_today.png")
draw_forecast("forecast_tomorrow.png")
