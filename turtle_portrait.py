"""
=============================================================================
💖 PYTHON TURTLE — 100% CRYSTAL-CLEAR PORTRAIT & LIVING ROMANTIC ENVIRONMENT 💖
=============================================================================
Features:
  1. Act 1: Preliminary Hand-Drawn Silhouette Sketch.
  2. Act 2: Magic Color Bloom (100% crystal-clear, razor-sharp photographic
            portrait with ZERO marks, ZERO lines, completely flawless faces).
  3. Act 3: Living Romantic Environment (Continuous 60 FPS Animation):
            - Beating / pulsing twin interlocking hearts above the couple.
            - Continuous stream of 35+ floating romantic hearts drifting upward.
            - Twinkling golden fairy lights / fireflies in twilight sky.
            - Click anywhere to spawn a burst of floating love hearts!
            - [Space] Pause/Play  |  [↑/↓] Speed  |  [Esc] Finish/Quit.
=============================================================================
"""

import os
import sys
import time
import math
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageTk
import turtle


def prepare_portrait_assets(image_path="portrait.jpg", target_width=620):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")

    h, w = img.shape[:2]
    target_height = int(h * target_width / w)
    img_resized = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 9, 75, 75)

    # 1. 100% Photographic Original (Completely unblemished, sharp, and clean)
    pil_orig = Image.fromarray(img_rgb)

    # 2. Pencil Sketch underlayer for opening sketch act
    inv = 255 - gray
    gauss = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - gauss, scale=256)
    sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    pil_sketch = Image.fromarray(sketch_rgb)

    # 3. Detect Faces for bloom centers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    face_centers = []
    for (fx, fy, fw, fh) in faces:
        cx = fx + fw // 2
        cy = fy + int(fh * 0.55) # Centered on smile
        face_centers.append((cx, cy, max(fw, fh) // 2 + 30))

    # Sort faces right-to-left: woman's smile first, then man's smile
    face_centers.sort(key=lambda item: item[0], reverse=True)

    # 4. Clean Preliminary Vector Contours for Turtle Sketching
    edges_main = cv2.Canny(blur, 45, 120)
    cnts_main, _ = cv2.findContours(edges_main, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

    sketch_paths = []
    for cnt in cnts_main:
        approx = cv2.approxPolyDP(cnt, 1.3, False)
        pts = approx.reshape(-1, 2)
        if len(pts) >= 4:
            sketch_paths.append(pts)

    return {
        "dimensions": (target_width, target_height),
        "pil_orig": pil_orig,
        "pil_sketch": pil_sketch,
        "face_centers": face_centers,
        "sketch_paths": sketch_paths
    }


def compute_heart_coords(cx, cy, size=1.0, angle=0):
    """Generates coordinates for a smooth mathematical heart."""
    rad_rot = math.radians(angle)
    cos_rot, sin_rot = math.cos(rad_rot), math.sin(rad_rot)
    coords = []
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        hx = size * 16 * (math.sin(rad) ** 3)
        hy = -size * (13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad))
        rx = hx * cos_rot - hy * sin_rot
        ry = hx * sin_rot + hy * cos_rot
        coords.extend([cx + rx, cy + ry])
    return coords


def run_animation(image_path="portrait.jpg"):
    print("=" * 65, flush=True)
    print("💖 Launching Living Romantic Environment & Crystal-Clear Portrait...", flush=True)
    print("=" * 65, flush=True)

    assets = prepare_portrait_assets(image_path, target_width=620)
    target_w, target_h = assets["dimensions"]
    pil_orig = assets["pil_orig"]
    pil_sketch = assets["pil_sketch"]
    face_centers = assets["face_centers"]
    sketch_paths = assets["sketch_paths"]

    # Coordinate mapping: from image pixels to turtle coordinates
    y_offset = -22
    def to_turtle(px, py):
        tx = px - target_w / 2
        ty = (target_h / 2 - py) + y_offset
        return tx, ty

    # Setup Screen
    screen = turtle.Screen()
    win_w = target_w + 220
    win_h = target_h + 230
    screen.setup(width=win_w, height=win_h)
    screen.title("💖 Forever & Always — Our Romantic Love Story 💖")
    screen.bgcolor("#140522") # Midnight romantic amethyst twilight
    screen.colormode(255)
    cv = screen.getcanvas()

    state = {
        "paused": False,
        "speed": 18,
        "skip": False,
        "living_mode": False
    }

    def toggle_pause():
        state["paused"] = not state["paused"]

    def speed_up():
        state["speed"] = min(80, state["speed"] + 10)

    def slow_down():
        state["speed"] = max(2, state["speed"] - 4)

    def finish_now():
        state["skip"] = True

    screen.onkey(toggle_pause, "space")
    screen.onkey(speed_up, "Up")
    screen.onkey(slow_down, "Down")
    screen.onkey(finish_now, "Escape")
    screen.onkey(finish_now, "q")
    screen.listen()

    # Draw Studio Frame and Archival Matting
    screen.tracer(0, 0)
    frame_t = turtle.Turtle()
    frame_t.hideturtle()
    frame_t.speed(0)

    pad = 12
    x0, y0 = to_turtle(-pad, -pad)
    x1, y1 = to_turtle(target_w + pad, target_h + pad)

    # Soft romantic glowing frame
    frame_t.penup()
    frame_t.goto(x0 - 4, y0 + 4)
    frame_t.pendown()
    frame_t.color("#e11d48", "#240a33") # Rose glow shadow
    frame_t.pensize(6)
    frame_t.goto(x1 + 4, y0 + 4)
    frame_t.goto(x1 + 4, y1 - 4)
    frame_t.goto(x0 - 4, y1 - 4)
    frame_t.goto(x0 - 4, y0 + 4)

    # Cream inner matting
    frame_t.penup()
    frame_t.goto(x0, y0)
    frame_t.pendown()
    frame_t.color("#f43f5e", "#faf8f5")
    frame_t.pensize(2)
    frame_t.begin_fill()
    frame_t.goto(x1, y0)
    frame_t.goto(x1, y1)
    frame_t.goto(x0, y1)
    frame_t.goto(x0, y0)
    frame_t.end_fill()

    # Gold accent inner border
    frame_t.penup()
    frame_t.goto(x0 + 4, y0 - 4)
    frame_t.pendown()
    frame_t.color("#fbbf24")
    frame_t.pensize(1.5)
    frame_t.goto(x1 - 4, y0 - 4)
    frame_t.goto(x1 - 4, y1 + 4)
    frame_t.goto(x0 + 4, y1 + 4)
    frame_t.goto(x0 + 4, y0 - 4)
    frame_t.penup()

    # Top & Bottom UI Header
    ui_t = turtle.Turtle()
    ui_t.hideturtle()
    ui_t.speed(0)

    top_y = target_h / 2 + y_offset + 42
    bottom_y = -target_h / 2 + y_offset - 48

    def update_ui(title, subtitle):
        ui_t.clear()
        ui_t.penup()
        ui_t.goto(0, top_y + 14)
        ui_t.color("#fef08a")
        ui_t.write(title, align="center", font=("Georgia", 14, "bold"))

        ui_t.goto(0, top_y - 12)
        ui_t.color("#fb7185")
        ui_t.write(subtitle, align="center", font=("Arial", 11, "normal"))

        ui_t.goto(0, bottom_y)
        ui_t.color("#cbd5e1")
        ui_t.write("✦ Click anywhere to send floating hearts • [Space] Pause • [Esc] Skip ✦",
                   align="center", font=("Arial", 10, "italic"))

    # Initial Canvas Image: The Pencil Sketch
    tk_sketch = ImageTk.PhotoImage(pil_sketch)
    img_item = cv.create_image(0, -y_offset, image=tk_sketch)
    setattr(screen, "_current_photo", tk_sketch)

    # Dedicated Sketch Turtle for Act 1
    sketch_t = turtle.Turtle()
    sketch_t.shape("classic")
    sketch_t.shapesize(0.8, 0.8)
    sketch_t.color("#38bdf8")
    sketch_t.speed(0)

    step_counter = 0
    def refresh():
        nonlocal step_counter
        step_counter += 1
        if step_counter >= state["speed"]:
            screen.update()
            step_counter = 0
            while state["paused"]:
                time.sleep(0.05)
                screen.update()

    # =============================================================
    # ACT 1: Preliminary Hand-Drawn Sketching
    # =============================================================
    update_ui("💖 FOREVER & ALWAYS • OUR ROMANTIC STORY 💖",
              "Act 1/3: Sketching Facial Silhouettes & Romantic Outlines...")
    screen.update()

    sketch_t.pensize(1.2)
    sketch_t.color("#334155")

    for pts in sketch_paths:
        if state["skip"]:
            break
        if len(pts) == 0:
            continue
        start_x, start_y = to_turtle(pts[0][0], pts[0][1])
        sketch_t.penup()
        sketch_t.goto(start_x, start_y)
        sketch_t.pendown()
        for pt in pts[1:]:
            tx, ty = to_turtle(pt[0], pt[1])
            sketch_t.goto(tx, ty)
            refresh()

    screen.update()
    time.sleep(0.2)

    # =============================================================
    # ACT 2: Magic Watercolor & Photographic Color Bloom
    # =============================================================
    update_ui("🎨 MAGIC COLOR PAINTBRUSH 🎨",
              "Act 2/3: Revealing 100% Crystal-Clear Photo (Zero Marks On Faces)...")

    # Erase sketch lines completely so faces are 100% unblemished!
    sketch_t.hideturtle()
    sketch_t.clear()

    brush_t = turtle.Turtle()
    brush_t.shape("circle")
    brush_t.shapesize(0.9, 0.9)
    brush_t.color("#fbbf24")
    brush_t.speed(0)

    reveal_mask = Image.new("L", (target_w, target_h), 0)
    draw_mask = ImageDraw.Draw(reveal_mask)

    def apply_color_dab(bx, by, dab_radius=45):
        draw_mask.ellipse([bx - dab_radius, by - dab_radius, bx + dab_radius, by + dab_radius], fill=255)
        comp = Image.composite(pil_orig, pil_sketch, reveal_mask)
        new_tk = ImageTk.PhotoImage(comp)
        cv.itemconfig(img_item, image=new_tk)
        cv.tag_raise(img_item) # Photo is completely in front!
        setattr(screen, "_current_photo", new_tk)

    # Spiral 1: Woman's Face (Right) - Radiating outward from her radiant smile!
    if len(face_centers) > 0 and not state["skip"]:
        cx, cy, max_r = face_centers[0]
        for theta in np.linspace(0, 5.5 * math.pi, 36):
            if state["skip"]:
                break
            r = (theta / (5.5 * math.pi)) * (max_r + 25)
            bx = cx + r * math.cos(theta)
            by = cy + r * math.sin(theta)
            tx, ty = to_turtle(bx, by)
            brush_t.penup()
            brush_t.goto(tx, ty)
            apply_color_dab(bx, by, dab_radius=46)
            screen.update()
            time.sleep(0.015)

    # Spiral 2: Man's Face (Left) - Radiating outward from his warm smile!
    if len(face_centers) > 1 and not state["skip"]:
        cx, cy, max_r = face_centers[1]
        for theta in np.linspace(0, 5.5 * math.pi, 36):
            if state["skip"]:
                break
            r = (theta / (5.5 * math.pi)) * (max_r + 25)
            bx = cx + r * math.cos(theta)
            by = cy + r * math.sin(theta)
            tx, ty = to_turtle(bx, by)
            brush_t.penup()
            brush_t.goto(tx, ty)
            apply_color_dab(bx, by, dab_radius=46)
            screen.update()
            time.sleep(0.015)

    # Sweep across clothes and background
    if not state["skip"]:
        sweep_points = []
        for y in range(int(target_h * 0.65), target_h, 38):
            x_range = range(20, target_w - 20, 50) if ((y // 38) % 2 == 0) else range(target_w - 20, 20, -50)
            for x in x_range:
                sweep_points.append((x, y))
        for x in range(30, target_w - 30, 55):
            sweep_points.append((x, 30))

        for (bx, by) in sweep_points:
            if state["skip"]:
                break
            tx, ty = to_turtle(bx, by)
            brush_t.penup()
            brush_t.goto(tx, ty)
            apply_color_dab(bx, by, dab_radius=68)
            screen.update()
            time.sleep(0.012)

    # Full Reveal of 100% Photographic Clarity
    draw_mask.rectangle([0, 0, target_w, target_h], fill=255)
    final_tk = ImageTk.PhotoImage(pil_orig)
    cv.itemconfig(img_item, image=final_tk)
    cv.tag_raise(img_item)
    setattr(screen, "_current_photo", final_tk)
    brush_t.hideturtle()
    screen.update()

    # Save 100% accurate snapshot to workspace
    pil_orig.save("preview_artwork.png")

    # =============================================================
    # ACT 3: Living Romantic Environment (Continuous Animation Loop)
    # =============================================================
    update_ui("💖 FOREVER & ALWAYS • OUR LOVE STORY 💖",
              "✨ Two Hearts Beating as One • Floating Love Atmosphere ✨")

    # Colors for floating hearts
    romantic_colors = [
        ("#e11d48", "#be123c"),  # Passion Crimson
        ("#ff2a85", "#db2777"),  # Hot Magenta Rose
        ("#fb7185", "#f43f5e"),  # Soft Coral Blush
        ("#ff758f", "#e11d48"),  # Cotton Candy Pink
        ("#f59e0b", "#d97706"),  # Shimmering Gold
        ("#c084fc", "#9333ea"),  # Sweet Lilac
        ("#ffffff", "#f43f5e")   # Pure Love Diamond
    ]

    # Create Twin Interconnected Beating Hearts above the couple
    twin_heart_y = -(top_y - 22) # Tkinter canvas coordinates
    heart_left_coords = compute_heart_coords(-26, twin_heart_y, size=1.15, angle=-12)
    heart_left_item = cv.create_polygon(heart_left_coords, fill="#e11d48", outline="#be123c", width=2, smooth=True)

    heart_right_coords = compute_heart_coords(26, twin_heart_y, size=1.15, angle=12)
    heart_right_item = cv.create_polygon(heart_right_coords, fill="#fb7185", outline="#e11d48", width=2, smooth=True)

    # Golden center twinkle between twin hearts
    center_star = cv.create_oval(-5, twin_heart_y - 5, 5, twin_heart_y + 5, fill="#fef08a", outline="#fbbf24", width=1.5)

    # Create Background Twinkling Fairy Lights / Stars
    fairy_lights = []
    for _ in range(35):
        # Place lights around outside perimeter of photo
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            lx = random.uniform(-win_w // 2 + 15, -target_w // 2 - 20)
            ly = random.uniform(-win_h // 2 + 30, win_h // 2 - 30)
        elif side == "right":
            lx = random.uniform(target_w // 2 + 20, win_w // 2 - 15)
            ly = random.uniform(-win_h // 2 + 30, win_h // 2 - 30)
        elif side == "top":
            lx = random.uniform(-win_w // 2 + 30, win_w // 2 - 30)
            ly = random.uniform(-win_h // 2 + 15, -target_h // 2 - 30)
        else:
            lx = random.uniform(-win_w // 2 + 30, win_w // 2 - 30)
            ly = random.uniform(target_h // 2 + 30, win_h // 2 - 15)

        r = random.uniform(1.5, 3.5)
        fl_color = random.choice(["#fef08a", "#fde047", "#fed7aa", "#f472b6", "#e0e7ff"])
        item = cv.create_oval(lx - r, ly - r, lx + r, ly + r, fill=fl_color, outline="")
        fairy_lights.append({
            "id": item,
            "x": lx, "y": ly, "r": r,
            "phase": random.uniform(0, 2 * math.pi),
            "speed": random.uniform(0.04, 0.08)
        })

    # Create 35 Continuous Floating Hearts
    floating_hearts = []

    def spawn_floating_heart(start_y=None):
        side = random.choice(["left", "right", "wide_left", "wide_right"])
        if side == "left":
            hx = random.uniform(-win_w // 2 + 25, -target_w // 2 - 15)
        elif side == "right":
            hx = random.uniform(target_w // 2 + 15, win_w // 2 - 25)
        elif side == "wide_left":
            hx = random.uniform(-win_w // 2 + 10, -target_w // 2 - 30)
        else:
            hx = random.uniform(target_w // 2 + 30, win_w // 2 - 10)

        hy = start_y if start_y is not None else random.uniform(-win_h // 2 + 50, win_h // 2 + 80)
        sz = random.uniform(0.45, 0.95)
        ang = random.uniform(-20, 20)
        fill, out = random.choice(romantic_colors)

        coords = compute_heart_coords(hx, hy, size=sz, angle=ang)
        item = cv.create_polygon(coords, fill=fill, outline=out, width=1.5, smooth=True)

        return {
            "id": item,
            "x": hx, "y": hy,
            "sz": sz, "ang": ang,
            "vy": random.uniform(1.8, 3.5),
            "sway_amp": random.uniform(15, 35),
            "sway_freq": random.uniform(0.03, 0.07),
            "phase": random.uniform(0, 2 * math.pi),
            "fill": fill, "out": out
        }

    # Pre-populate 35 floating hearts at various heights
    for _ in range(35):
        floating_hearts.append(spawn_floating_heart())

    # Click-to-burst Heart Spawner
    burst_hearts = []
    def on_click(canvas_x, canvas_y):
        # In turtle screen.onclick, coordinates are in turtle system!
        # Convert to canvas coordinates: cx = tx, cy = -ty
        cx = canvas_x
        cy = -canvas_y
        for _ in range(8):
            sz = random.uniform(0.5, 0.9)
            ang = random.uniform(-30, 30)
            fill, out = random.choice(romantic_colors)
            coords = compute_heart_coords(cx, cy, size=sz, angle=ang)
            item = cv.create_polygon(coords, fill=fill, outline=out, width=1.5, smooth=True)
            burst_hearts.append({
                "id": item,
                "x": cx, "y": cy,
                "vx": random.uniform(-3.5, 3.5),
                "vy": random.uniform(-2.5, -6.0),
                "sz": sz, "ang": ang,
                "life": 45,
                "fill": fill, "out": out
            })

    screen.onclick(on_click)

    # Romantic Calligraphy Ribbon
    callig_y = -(bottom_y + 14)
    cv.create_text(0, callig_y, text="💖 Two Hearts, One Beautiful Story • Forever & Always 💖",
                   fill="#fb7185", font=("Georgia", 13, "bold italic"))

    # Living Animation Loop Variables
    frame_count = 0
    heartbeat_phase = 0.0

    print("=" * 65, flush=True)
    print("✨ Romantic Living Environment is now ACTIVE on screen!", flush=True)
    print("✨ Click anywhere on the window to send bursts of love hearts!", flush=True)
    print("=" * 65, flush=True)

    # Run Real-Time 60 FPS Romantic Environment Loop
    def animation_tick():
        nonlocal frame_count, heartbeat_phase

        if not state["paused"]:
            frame_count += 1
            heartbeat_phase += 0.08

            # 1. Beating Heart Pulse Effect (lub-DUB heartbeat rhythm)
            # Pulse twin hearts in size:
            beat = 1.0 + 0.12 * (math.sin(heartbeat_phase) ** 3)
            # Update left heart
            coords_l = compute_heart_coords(-26 * beat, twin_heart_y, size=1.15 * beat, angle=-12)
            cv.coords(heart_left_item, *coords_l)
            # Update right heart
            coords_r = compute_heart_coords(26 * beat, twin_heart_y, size=1.15 * beat, angle=12)
            cv.coords(heart_right_item, *coords_r)

            # 2. Twinkle Fairy Lights
            for fl in fairy_lights:
                fl["phase"] += fl["speed"]
                # Slight scale or flicker
                twinkle_r = fl["r"] * (0.75 + 0.35 * math.sin(fl["phase"]))
                cv.coords(fl["id"], fl["x"] - twinkle_r, fl["y"] - twinkle_r,
                                    fl["x"] + twinkle_r, fl["y"] + twinkle_r)

            # 3. Animate 35 Floating Hearts Drifting Upward
            for fh in floating_hearts:
                fh["y"] -= fh["vy"]
                fh["phase"] += fh["sway_freq"]
                curr_x = fh["x"] + fh["sway_amp"] * math.sin(fh["phase"])

                # Wrap around to bottom if floated off screen top
                if fh["y"] < -win_h // 2 - 40:
                    fh["y"] = win_h // 2 + 40
                    fh["x"] = random.choice([
                        random.uniform(-win_w // 2 + 20, -target_w // 2 - 15),
                        random.uniform(target_w // 2 + 15, win_w // 2 - 20)
                    ])
                    curr_x = fh["x"]

                coords = compute_heart_coords(curr_x, fh["y"], size=fh["sz"], angle=fh["ang"])
                cv.coords(fh["id"], *coords)

            # 4. Animate Interactive Click-Burst Hearts
            for bh in list(burst_hearts):
                bh["x"] += bh["vx"]
                bh["y"] += bh["vy"]
                bh["vy"] += 0.08 # gentle gravity deceleration
                bh["life"] -= 1

                if bh["life"] <= 0 or bh["y"] < -win_h // 2 - 30:
                    cv.delete(bh["id"])
                    burst_hearts.remove(bh)
                else:
                    coords = compute_heart_coords(bh["x"], bh["y"], size=bh["sz"], angle=bh["ang"])
                    cv.coords(bh["id"], *coords)

            screen.update()

        # Schedule next tick (~60 fps = 16ms)
        screen.ontimer(animation_tick, 16)

    # Start the continuous animation loop!
    screen.update()
    animation_tick()
    turtle.mainloop()


if __name__ == "__main__":
    img_file = "portrait.jpg"
    if len(sys.argv) > 1:
        img_file = sys.argv[1]
    run_animation(img_file)
