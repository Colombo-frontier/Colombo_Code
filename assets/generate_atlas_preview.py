#!/usr/bin/env python3
"""Render the README preview from the current Atlas layout and setting statuses.

Run with Python 3 and Pillow installed:
    python assets/generate_atlas_preview.py

The presentation is deliberately simpler than the interactive Atlas. It uses
the Atlas's aggregate status per setting, its exact 3D positions, and its
adopted Colombo markers. Native records and the interactive Atlas are untouched.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "colombo_sensorium/Complexity_altas/data/derived"
WIDTH, HEIGHT = 1000, 680
SUPERSAMPLE = 2
GREEN = "#49d696"
ORANGE = "#f6a24d"
CORAL = "#ff5266"
PALE_RIM = "#fff1ea"
TEXT = "#ecf5f8"
MUTED = "#9db2c1"
BG = "#08131e"
SCENE = (26, 111, WIDTH - 26, 582)


def rgb(color):
    return tuple(bytes.fromhex(color.lstrip("#")))


def font(size, bold=False):
    names = [
        Path("/System/Library/Fonts/Supplemental") /
        ("Arial Bold.ttf" if bold else "Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") /
        ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for path in names:
        if path.exists():
            return ImageFont.truetype(str(path), round(size * SUPERSAMPLE))
    return ImageFont.load_default(size=round(size * SUPERSAMPLE))


def box(coords):
    return tuple(round(x * SUPERSAMPLE) for x in coords)


def ellipse(draw, x, y, radius, fill=None, outline=None, width=1):
    draw.ellipse(box((x - radius, y - radius, x + radius, y + radius)),
                 fill=fill, outline=outline, width=round(width * SUPERSAMPLE))


def load_data():
    overview_path = DATA / "atlas_overview.json"
    layout_path = DATA / "atlas_nebula.json"
    overview = json.loads(overview_path.read_text())
    layout = json.loads(layout_path.read_text())
    points = overview["points"]
    ids = {p["id"] for p in points}
    assert len(ids) == len(points) == len(layout["positions"])
    assert ids == set(layout["positions"])
    assert all(p["status"] in {x["id"] for x in overview["status_legend"]}
               for p in points)
    for p in points:
        p["xyz"] = layout["positions"][p["id"]]
        p["preview_color"] = GREEN if p["status"] in {"optimal", "near"} else ORANGE
        p["marked"] = p.get("colombo", {}).get("state") == "adopted"
    summary = {
        "settings": len(points),
        "task_clusters": len(layout["clusters"]),
        "green": sum(p["preview_color"] == GREEN for p in points),
        "orange": sum(p["preview_color"] == ORANGE for p in points),
        "colombo_rings": sum(p["marked"] for p in points),
        "native_statuses": dict(Counter(p["status"] for p in points)),
        "overview_sha256": hashlib.sha256(overview_path.read_bytes()).hexdigest(),
        "layout_sha256": hashlib.sha256(layout_path.read_bytes()).hexdigest(),
    }
    return points, layout, summary


def view(xyz, yaw):
    x, y, z = xyz
    pitch = .19
    sy, cy, sp, cp = math.sin(yaw), math.cos(yaw), math.sin(pitch), math.cos(pitch)
    x1, z1 = x * cy - z * sy, x * sy + z * cy
    y2, z2 = y * cp - z1 * sp, y * sp + z1 * cp
    depth = 6.9 / (6.9 - z2)
    return x1 * depth, -y2 * depth, z2, depth


def scene_scale(points):
    # Fit every star and its outer halo throughout the full orbit, with one
    # fixed camera scale so that the animation never breathes or clips points.
    samples = [view(p["xyz"], math.tau * i / 256) for p in points for i in range(256)]
    xmax = max(abs(p[0]) for p in samples)
    ymin, ymax = min(p[1] for p in samples), max(p[1] for p in samples)
    cx, cy = WIDTH / 2, 348
    return min((SCENE[2] - cx - 28) / xmax,
               (cy - SCENE[1] - 42) / -ymin,
               (SCENE[3] - cy - 34) / ymax)


def background(summary):
    im = Image.new("RGB", (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), BG)
    d = ImageDraw.Draw(im)
    # Subtle vertical color shifts preserve the native dark Atlas atmosphere.
    for y in range(HEIGHT * SUPERSAMPLE):
        t = y / (HEIGHT * SUPERSAMPLE)
        color = tuple(round(a + (b - a) * t) for a, b in zip((8, 20, 31), (12, 27, 39)))
        d.line((0, y, WIDTH * SUPERSAMPLE, y), fill=color)
    d.rounded_rectangle(box((1, 1, WIDTH - 2, HEIGHT - 2)),
                        radius=round(18 * SUPERSAMPLE), outline="#2c4353", width=2)
    d.text(box((32, 22)), "Complexity Atlas", font=font(31, True), fill=TEXT)
    d.rounded_rectangle(box((321, 27, 362, 52)), radius=round(6 * SUPERSAMPLE),
                        fill="#1c3444", outline="#355367", width=1)
    d.text(box((330, 30)), "3D", font=font(15, True), fill="#c0d6df")
    d.text(box((33, 67)),
           f"{summary['settings']} settings  /  {summary['task_clusters']} task constellations",
           font=font(16), fill=MUTED)
    d.rounded_rectangle(box(SCENE), radius=round(12 * SUPERSAMPLE),
                        outline="#294253", width=round(SUPERSAMPLE))
    # The compact legend is the only status key in the README preview.
    line_y = 603
    d.line(box((32, line_y, WIDTH - 32, line_y)), fill="#2a3d4d", width=round(SUPERSAMPLE))
    legend_y = 634
    ellipse(d, 45, legend_y, 5, fill=GREEN)
    d.text(box((61, legend_y)), "(Near) optimal", font=font(16, True), fill=TEXT, anchor="lm")
    ellipse(d, 310, legend_y, 5, fill=ORANGE)
    d.text(box((326, legend_y)), "Gap / other regimes", font=font(16, True), fill=TEXT, anchor="lm")
    ellipse(d, 679, legend_y, 7, outline=CORAL, width=2)
    ellipse(d, 679, legend_y, 5.7, outline=PALE_RIM, width=.65)
    d.text(box((697, legend_y)), "Colombo output", font=font(16, True), fill=TEXT, anchor="lm")
    return im


def cloud_stamp():
    size = 256
    alpha = Image.new("L", (size, size))
    d = ImageDraw.Draw(alpha)
    for radius in range(125, 0, -1):
        t = 1 - radius / 126
        a = round(22 * (t ** 1.5))
        d.ellipse((128 - radius, 128 - radius, 128 + radius, 128 + radius), fill=a)
    cloud = Image.new("RGBA", (size, size), (70, 119, 140, 0))
    cloud.putalpha(alpha.filter(ImageFilter.GaussianBlur(8)))
    return cloud


def overlaps(a, b, margin=0):
    return (a[0] < b[2] + margin and a[2] > b[0] - margin and
            a[1] < b[3] + margin and a[3] > b[1] - margin)


def render(points, clusters, base, stamp, scale, yaw):
    im = base.copy().convert("RGBA")
    cx, cy = WIDTH / 2, 348

    def project(xyz):
        x, y, z, depth = view(xyz, yaw)
        return cx + x * scale, cy + y * scale, z, depth

    projected = [(p, project(p["xyz"])) for p in points]
    # Haze is neutral; only actual setting cores carry the two status colors.
    for c in sorted(clusters, key=lambda c: project(c["center"])[2]):
        x, y, z, depth = project(c["center"])
        radius = max(18, c["radius"] * scale * depth * 1.45)
        sw, sh = round(radius * 2.6 * SUPERSAMPLE), round(radius * 1.85 * SUPERSAMPLE)
        cloud = stamp.resize((sw, sh), Image.Resampling.BILINEAR)
        im.alpha_composite(cloud, (round(x * SUPERSAMPLE - sw / 2), round(y * SUPERSAMPLE - sh / 2)))

    glow = Image.new("RGBA", im.size)
    gd = ImageDraw.Draw(glow)
    for p, (x, y, z, depth) in projected:
        radius = 2.65 * depth
        color = rgb(p["preview_color"])
        ellipse(gd, x, y, radius * 2.4, fill=color + (14,))
        ellipse(gd, x, y, radius * 1.7, fill=color + (22,))
        if p["marked"]:
            ellipse(gd, x, y, radius + 5.4, outline=rgb(CORAL) + (30,), width=2.2)
    im = Image.alpha_composite(im, glow)
    d = ImageDraw.Draw(im)
    # Match the native paint order: adopted output halos remain visible in
    # dense clusters, while each core retains its mathematical-status color.
    for p, (x, y, z, depth) in sorted(projected, key=lambda item: (item[0]["marked"], item[1][2])):
        radius = 2.65 * depth
        assert SCENE[0] + 8 < x < SCENE[2] - 8
        assert SCENE[1] + 8 < y < SCENE[3] - 8
        ellipse(d, x, y, radius, fill=p["preview_color"])
        if p["marked"]:
            ellipse(d, x, y, radius + 3.1, outline=CORAL, width=1.8)
            ellipse(d, x, y, radius + 1.8, outline=PALE_RIM, width=.65)

    # Upright labels follow the current task centers. Keep them away from
    # setting cores and other labels; skip a label if an edge-on orbit has no
    # unobstructed placement, as the interactive Atlas itself does.
    label_boxes = []
    f = font(15, True)
    for c in sorted(clusters, key=lambda c: -c["count"]):
        x, y, z, depth = project(c["center"])
        label = c["label"]
        tw = d.textlength(label, font=f) / SUPERSAMPLE
        radius = c["radius"] * scale * depth
        member_y = [pos[1] for p, pos in projected if p["task"] == c["task"]]
        candidates = [(x, y - radius * .93 - 16), (x, min(member_y) - 25),
                      (x, y - radius * .75 - 5),
                      (x, y - radius * 1.20 - 20), (x, y + radius * .93 + 16),
                      (x - radius * 1.12 - tw / 2 - 12, y),
                      (x + radius * 1.12 + tw / 2 + 12, y)]
        for lx, ly in candidates:
            rect = (lx - tw / 2 - 5, ly - 11, lx + tw / 2 + 5, ly + 11)
            if not (SCENE[0] + 9 <= rect[0] < rect[2] <= SCENE[2] - 9 and
                    SCENE[1] + 10 <= rect[1] < rect[3] <= SCENE[3] - 10):
                continue
            if any(overlaps(rect, other, 6) for other in label_boxes):
                continue
            if any(overlaps(rect, (px - 7, py - 7, px + 7, py + 7))
                   for _, (px, py, _, _) in projected):
                continue
            d.text(box((lx, ly)), label, anchor="mm", font=f, fill=TEXT,
                   stroke_width=round(2 * SUPERSAMPLE), stroke_fill=BG)
            label_boxes.append(rect)
            break
    return im.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=128)
    parser.add_argument("--duration", type=int, default=80, help="Milliseconds per frame")
    parser.add_argument("--poster-only", action="store_true")
    args = parser.parse_args()
    points, layout, summary = load_data()
    scale = scene_scale(points)
    base, stamp = background(summary), cloud_stamp()
    first_yaw = -.21
    poster = render(points, layout["clusters"], base, stamp, scale, first_yaw)
    target = ROOT / "assets"
    poster.save(target / "complexity-atlas.jpg", quality=94, subsampling=0, optimize=True)
    if not args.poster_only:
        frames = [render(points, layout["clusters"], base, stamp, scale,
                         first_yaw + math.tau * i / args.frames)
                  for i in range(args.frames)]
        # One palette for the entire loop avoids per-frame palette flicker.
        samples = Image.new("RGB", (WIDTH * 4, HEIGHT * 2))
        for i in range(8):
            samples.paste(frames[i * len(frames) // 8], (i % 4 * WIDTH, i // 4 * HEIGHT))
        palette = samples.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
        indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
        indexed[0].save(target / "complexity-atlas.gif", save_all=True,
                        append_images=indexed[1:], duration=args.duration,
                        loop=0, optimize=True, disposal=1)
        summary["frames"] = len(frames)
        summary["duration_ms"] = len(frames) * args.duration
        summary["gif_bytes"] = (target / "complexity-atlas.gif").stat().st_size
    summary["poster_bytes"] = (target / "complexity-atlas.jpg").stat().st_size
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
