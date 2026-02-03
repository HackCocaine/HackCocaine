#!/usr/bin/env python3
"""
GitHub Metrics Dashboard - Animated GIF Generator
Creates smooth, high-resolution particle animations for GitHub README.
"""

import base64
import json
import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Metrics collection with defaults
stars = int(os.environ.get("STARS", "0") or "0")
forks = int(os.environ.get("FORKS", "0") or "0")
issues = int(os.environ.get("ISSUES", "0") or "0")
commits = int(os.environ.get("COMMITS", "0") or "0")
contributors = int(os.environ.get("CONTRIBUTORS", "0") or "0")
prs_30d = int(os.environ.get("PRS_30D", "0") or "0")
issues_30d = int(os.environ.get("ISSUES_30D", "0") or "0")

assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

metrics_data = {
    "stars": stars,
    "forks": forks,
    "issues": issues,
    "commits": commits,
    "contributors": contributors,
    "prs_30d": prs_30d,
    "issues_30d": issues_30d,
}
with open("metrics_data.json", "w") as f:
    json.dump(metrics_data, f, indent=2)


class Colors:
    STAR = {
        "primary": (255, 200, 80),
        "secondary": (255, 150, 50),
        "glow": (255, 220, 150),
        "bg": (12, 10, 18),
    }
    FORK = {
        "primary": (150, 120, 255),
        "secondary": (80, 200, 255),
        "glow": (200, 180, 255),
        "bg": (12, 10, 18),
    }
    ISSUE = {
        "primary": (255, 100, 70),
        "secondary": (255, 160, 100),
        "glow": (255, 200, 160),
        "bg": (18, 12, 12),
    }
    CONTRIBUTOR = {
        "primary": (80, 210, 150),
        "secondary": (100, 170, 240),
        "glow": (170, 240, 210),
        "bg": (10, 12, 15),
    }


class Particle:
    def __init__(self, x, y, vx, vy, size, color, life=1.0, decay=0.02):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.base_size = max(0.5, float(size))
        self.size = self.base_size
        self.color = color
        self.life = min(1.0, max(0.1, float(life)))
        self.decay = max(0.005, min(0.05, float(decay)))
        self.pulse = random.random() * 6.28

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        self.pulse += 0.15
        if self.life < 0.1:
            self.life = 0.1
        return self.life > 0.05

    def get_size(self):
        pulse_factor = 0.85 + 0.15 * math.sin(self.pulse)
        return self.base_size * self.life * pulse_factor


class ParticleSystem:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.particles = []

    def spawn(
        self,
        x,
        y,
        count=1,
        size=3.0,
        speed=1.5,
        color=(255, 255, 255),
        life=1.0,
        decay=0.02,
        angle=None,
    ):
        size = max(0.5, float(size))
        speed = max(0.1, float(speed))
        for _ in range(count):
            a = angle if angle is not None else random.random() * 6.28
            s = speed * (0.5 + random.random() * 0.5)
            self.particles.append(
                Particle(
                    x, y, math.cos(a) * s, math.sin(a) * s, size, color, life, decay
                )
            )

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def render(self, img):
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)

        for p in self.particles:
            sz = p.get_size() * 2.5
            alpha = int(70 * p.life)
            glow_draw.ellipse(
                [p.x - sz, p.y - sz, p.x + sz, p.y + sz], fill=p.color + (alpha,)
            )

        img_p = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img_p)

        for p in self.particles:
            sz = p.get_size()
            draw.ellipse([p.x - sz, p.y - sz, p.x + sz, p.y + sz], fill=p.color)

        return img_p


class MetricVisualizer:
    def __init__(self, w, h, palette, label):
        self.w, self.h = w, h
        self.palette = palette
        self.label = label
        self.system = ParticleSystem(w, h)
        self.font_size = max(14, h // 8)
        self.value_font_size = max(24, h // 5)

    def make_frame(self, metric_value, frame_idx, total_frames):
        img = Image.new("RGB", (self.w, self.h), self.palette["bg"])
        draw = ImageDraw.Draw(img)

        # Label (top)
        bbox = draw.textbbox((0, 0), self.label)
        text_w = bbox[2] - bbox[0]
        draw.text(
            ((self.w - text_w) / 2, 12), self.label, fill=self.palette["secondary"]
        )

        # Value (bottom, larger)
        value_str = f"{metric_value:,}"
        bbox = draw.textbbox((0, 0), value_str)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(
            ((self.w - text_w) / 2, self.h - text_h - 18),
            value_str,
            fill=self.palette["primary"],
        )

        return img

    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        pass

    def animate(self, metric_value, path, frames=30, fps=12):
        print(f"  {self.label}: {metric_value} ({frames} frames @ {fps}fps)...")
        result_frames = []

        # Pre-seed particles
        for _ in range(25):
            self.system.spawn(
                random.uniform(20, self.w - 20),
                random.uniform(30, self.h - 50),
                1,
                2,
                0.3,
                self.palette["glow"],
                0.8,
                0.015,
            )

        for i in range(frames):
            frame = self.make_frame(metric_value, i, frames)
            self.animate_frame(frame, metric_value, i, frames)
            result_frames.append(frame)

        result_frames[0].save(
            path,
            save_all=True,
            append_images=result_frames[1:],
            duration=int(1000 / fps),
            loop=0,
            optimize=True,
            disposal=2,
        )
        print(f"    Saved: {path}")


class StarVisualizer(MetricVisualizer):
    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        t = frame_idx * 0.2
        cx, cy = self.w / 2, self.h / 2 + 5

        # Orbiting particles
        count = max(12, min(35, int(math.log(max(1, metric_value + 1)) * 8)))
        for i in range(count):
            angle = (i / count) * 6.28 + t * 0.5
            r = 35 + 12 * math.sin(t * 2 + i * 0.3)
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            self.system.spawn(
                x, y, 1, 2.5, 0.2, self.palette["primary"], 0.6, 0.01, angle + 1.57
            )

        # Background twinkle
        for _ in range(4):
            x = random.uniform(15, self.w - 15)
            y = random.uniform(35, self.h - 70)
            b = 0.4 + 0.5 * math.sin(t * 3 + x * 0.1)
            c = tuple(int(v * b) for v in self.palette["glow"])
            self.system.spawn(x, y, 1, 1.2, 0, c, 0.4, 0.02)

        self.system.update()
        new_img = self.system.render(img)
        img.paste(new_img, (0, 0))


class ForkVisualizer(MetricVisualizer):
    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        t = frame_idx * 0.18
        cx, cy = self.w / 2, self.h / 2 + 5

        # Branches
        branches = max(5, min(12, int(math.sqrt(max(1, metric_value + 1))) + 2))
        for i in range(branches):
            angle = (i / branches) * 6.28 - 1.57 + t * 0.15
            length = 40 + 8 * math.sin(t + i * 0.4)
            ex = cx + math.cos(angle) * length
            ey = cy + math.sin(angle) * length
            draw = ImageDraw.Draw(img)
            draw.line([cx, cy, ex, ey], fill=self.palette["primary"], width=2)

        # Particles
        count = max(10, min(30, int(math.log(max(1, metric_value + 1)) * 5)))
        for i in range(count):
            angle = (i / count) * 6.28 + t * 0.4
            r = 22 + 18 * abs(math.sin(t * 0.8 + i * 0.2))
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            self.system.spawn(x, y, 1, 2, 0.25, self.palette["glow"], 0.5, 0.012)

        self.system.update()
        new_img = self.system.render(img)
        img.paste(new_img, (0, 0))


class IssueVisualizer(MetricVisualizer):
    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        t = frame_idx * 0.25
        cx, cy = self.w / 2, self.h / 2 + 5

        # Pulse rings
        pulse = 25 + 8 * math.sin(t * 2.2)
        for i in range(2):
            rs = pulse + i * 10
            draw = ImageDraw.Draw(img)
            draw.ellipse(
                [cx - rs, cy - rs, cx + rs, cy + rs],
                outline=self.palette["primary"],
                width=2,
            )

        # Rising
        count = max(8, min(25, max(1, metric_value // 2)))
        for i in range(count):
            y = self.h - 55 - (frame_idx / total_frames) * 75 + 15 * math.sin(t + i)
            x = cx + (i - count / 2) * 12 * math.sin(t + i * 0.4)
            sz = max(0.5, 2 + math.sin(t * 1.8 + i) * 0.8)
            self.system.spawn(x, y, 1, sz, 0.35, self.palette["primary"], 0.7, 0.015)

        self.system.update()
        new_img = self.system.render(img)
        img.paste(new_img, (0, 0))


class ContributorVisualizer(MetricVisualizer):
    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        t = frame_idx * 0.15
        cx, cy = self.w / 2, self.h / 2 + 5

        # Nodes
        nodes = max(5, min(14, max(1, metric_value)))
        node_pos = []
        for i in range(nodes):
            angle = (i / nodes) * 6.28 + t * 0.18
            r = 25 + 12 * math.sin(t + i * 0.35)
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            node_pos.append((x, y))
            draw = ImageDraw.Draw(img)
            draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=self.palette["primary"])

        # Connections
        for i in range(len(node_pos)):
            for j in range(i + 1, len(node_pos)):
                x1, y1 = node_pos[i]
                x2, y2 = node_pos[j]
                d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if d < 60:
                    alpha = int(180 * (1 - d / 60))
                    c = tuple(int(v * alpha / 255) for v in self.palette["secondary"])
                    draw = ImageDraw.Draw(img)
                    draw.line([x1, y1, x2, y2], fill=c, width=1)

        # Orbiting
        count = max(8, min(20, int(math.log(max(1, metric_value + 1)) * 4)))
        for i in range(count):
            angle = (i / count) * 6.28 + t * 0.6
            r = 18 + 8 * math.sin(t + i * 0.25)
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            self.system.spawn(x, y, 1, 1.5, 0.2, self.palette["glow"], 0.45, 0.018)

        self.system.update()
        new_img = self.system.render(img)
        img.paste(new_img, (0, 0))


def hstack(images):
    if not images:
        raise ValueError("No images")
    ws, hs = zip(*(i.size for i in images))
    h = max(hs)
    w = sum(ws)
    res = Image.new("RGB", (w, h))
    x = 0
    for img in images:
        res.paste(img, (x, (h - img.height) // 2))
        x += img.width
    return res


def create_dashboard(gif_paths, out_path, fps=10):
    """Create combined dashboard with longer duration."""
    print("  Creating combined dashboard...")
    all_frames = []
    frame_counts = []

    for p in gif_paths:
        try:
            frames = []
            with Image.open(p) as img:
                try:
                    while True:
                        frames.append(img.copy())
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass
            all_frames.append(frames)
            frame_counts.append(len(frames))
            print(f"    {p}: {len(frames)} frames")
        except Exception as e:
            print(f"    Warning: {p} - {e}")
            all_frames.append([Image.new("RGB", (400, 200), (25, 25, 35))])
            frame_counts.append(1)

    min_frames = min(frame_counts)
    print(f"    Combining {min_frames} frames each...")

    result = []
    for i in range(min_frames):
        row = []
        for j, frames in enumerate(all_frames):
            frame = frames[min(i, len(frames) - 1)].resize((400, 200), Image.LANCZOS)
            row.append(frame)
        result.append(hstack(row))

    # Save with slower FPS for longer duration
    duration_ms = int(1000 / fps)  # 100ms = 10fps
    result[0].save(
        out_path,
        save_all=True,
        append_images=result[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(
        f"    Saved: {out_path} ({len(result)} frames, {fps}fps, {duration_ms}ms/frame)"
    )


def create_svg_embedded_gif(gif_path, output_path, width=800, height=200):
    """Create SVG that embeds GIF for better GitHub README compatibility."""
    print("  Creating SVG embed...")

    with open(gif_path, "rb") as f:
        gif_data = base64.b64encode(f.read()).decode("ascii")

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>GitHub Metrics Dashboard</title>
  <desc>Animated particle visualization showing repository metrics: {stars} stars, {forks} forks, {issues} issues, {contributors} contributors</desc>
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml" style="display:flex;justify-content:center;align-items:center;width:100%;height:100%;background:transparent;">
      <img src="data:image/gif;base64,{gif_data}" alt="Repository Metrics Dashboard showing {stars} stars, {forks} forks, {issues} issues, {contributors} contributors" style="max-width:100%;height:auto;border-radius:8px;background:transparent;"/>
    </div>
  </foreignObject>
</svg>'''

    with open(output_path, "w") as f:
        f.write(svg)
    print(f"    Saved: {output_path}")


def main():
    print("=" * 60)
    print("GitHub Metrics Dashboard Generator")
    print("=" * 60)
    print(f"Metrics: ⭐ {stars} | 🍴 {forks} | 📋 {issues} | 👥 {contributors}")
    print("=" * 60)

    # Higher resolution for individual metrics
    w, h = 400, 200
    fps_individual = 12
    frames_individual = 30

    # Slower FPS for dashboard = longer duration
    fps_dashboard = 10
    # Dashboard uses frames from individual GIFs

    print("\n🎨 Generating high-resolution animations...")
    paths = []

    StarVisualizer(w, h, Colors.STAR, "⭐ Stars").animate(
        stars, "assets/metric_stars.gif", frames_individual, fps_individual
    )
    paths.append("assets/metric_stars.gif")

    ForkVisualizer(w, h, Colors.FORK, "🍴 Forks").animate(
        forks, "assets/metric_forks.gif", frames_individual, fps_individual
    )
    paths.append("assets/metric_forks.gif")

    IssueVisualizer(w, h, Colors.ISSUE, "📋 Issues").animate(
        issues, "assets/metric_issues.gif", frames_individual, fps_individual
    )
    paths.append("assets/metric_issues.gif")

    ContributorVisualizer(w, h, Colors.CONTRIBUTOR, "👥 Contributors").animate(
        contributors,
        "assets/metric_contributors.gif",
        frames_individual,
        fps_individual,
    )
    paths.append("assets/metric_contributors.gif")

    # Create combined dashboard (uses same frames, just arranged in grid)
    create_dashboard(paths, "assets/metrics_dashboard.gif", fps_dashboard)

    # Create SVG embed
    create_svg_embedded_gif(
        "assets/metrics_dashboard.gif",
        "assets/metrics_dashboard.svg",
        width=800,
        height=200,
    )

    print("\n" + "=" * 60)
    print("✅ Done!")
    print(f"   Individual resolution: {w}x{h}")
    print(f"   Dashboard resolution: 800x200 (4 metrics @ 400x200 each)")
    print(f"   Individual FPS: {fps_individual} ({1000 / fps_individual:.0f}ms/frame)")
    print(f"   Dashboard FPS: {fps_dashboard} ({1000 / fps_dashboard:.0f}ms/frame)")
    print("=" * 60)


if __name__ == "__main__":
    main()
