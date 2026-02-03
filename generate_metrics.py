#!/usr/bin/env python3
"""
GitHub Metrics Dashboard - Particle Animation Generator
Creates beautiful animated visualizations with persistent particle systems.
"""

import json
import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw

# Metrics collection
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
        self.base_size = max(0.5, size)
        self.size = self.base_size
        self.color = color
        self.life = min(1.0, max(0.1, life))
        self.decay = max(0.005, min(0.05, decay))
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

    def make_frame(self, metric_value, frame_idx, total_frames):
        img = Image.new("RGB", (self.w, self.h), self.palette["bg"])
        draw = ImageDraw.Draw(img)

        # Label
        lw = draw.textlength(self.label)
        draw.text(((self.w - lw) / 2, 10), self.label, fill=self.palette["secondary"])

        # Value
        val = f"{metric_value:,}"
        vw = draw.textlength(val)
        vh = 18
        draw.text(
            ((self.w - vw) / 2, self.h - vh - 8), val, fill=self.palette["primary"]
        )

        return img

    def animate(self, metric_value, path, frames=16, fps=12):
        print(f"  {self.label}: {frames} frames...")
        result_frames = []

        # Initialize system with some particles
        for _ in range(15):
            self.system.spawn(
                self.w / 2 + random.uniform(-40, 40),
                self.h / 2 + random.uniform(-20, 20),
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
        )
        print(f"    Saved: {path}")

    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        pass


class StarVisualizer(MetricVisualizer):
    def animate_frame(self, img, metric_value, frame_idx, total_frames):
        t = frame_idx * 0.2
        cx, cy = self.w / 2, self.h / 2 + 5

        # Orbiting particles
        count = max(8, min(25, int(math.log(max(1, metric_value + 1)) * 8)))
        for i in range(count):
            angle = (i / count) * 6.28 + t * 0.5
            r = 35 + 12 * math.sin(t * 2 + i * 0.3)
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            self.system.spawn(
                x, y, 1, 2.5, 0.2, self.palette["primary"], 0.6, 0.01, angle + 1.57
            )

        # Twinkling background
        for _ in range(2):
            x = random.uniform(20, self.w - 20)
            y = random.uniform(35, self.h - 55)
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

        # Branching
        branches = max(3, min(8, int(math.sqrt(max(1, metric_value + 1))) + 2))
        for i in range(branches):
            angle = (i / branches) * 6.28 - 1.57 + t * 0.15
            length = 40 + 8 * math.sin(t + i * 0.4)
            ex = cx + math.cos(angle) * length
            ey = cy + math.sin(angle) * length
            draw = ImageDraw.Draw(img)
            draw.line([cx, cy, ex, ey], fill=self.palette["primary"], width=2)

        # Particles on branches
        count = max(6, min(20, int(math.log(max(1, metric_value + 1)) * 5)))
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

        # Rising particles
        count = max(5, min(18, max(1, metric_value // 3)))
        for i in range(count):
            y = self.h - 50 - (frame_idx / total_frames) * 70 + 15 * math.sin(t + i)
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
        nodes = max(3, min(10, max(1, metric_value)))
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
        count = max(5, min(15, int(math.log(max(1, metric_value + 1)) * 4)))
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


def make_dashboard(gif_paths, out_path, fps=12):
    print("  Combining into dashboard...")
    all_frames = []
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
            print(f"    {p}: {len(frames)} frames")
        except Exception as e:
            print(f"    Warning: {p} - {e}")
            all_frames.append([Image.new("RGB", (200, 120), (25, 25, 35))])

    min_f = min(len(f) for f in all_frames)
    print(f"    Using {min_f} frames each...")

    result = []
    for i in range(min_f):
        row = [
            f[min(i, len(f) - 1)].resize((200, 120), Image.LANCZOS) for f in all_frames
        ]
        result.append(hstack(row))

    result[0].save(
        out_path,
        save_all=True,
        append_images=result[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )
    print(f"    Saved: {out_path}")


def main():
    print("=" * 50)
    print("GitHub Metrics Dashboard")
    print(f"⭐ {stars} | 🍴 {forks} | 📋 {issues} | 👥 {contributors}")
    print("=" * 50)

    w, h = 200, 120
    fps, frames = 12, 16

    print("\n🎨 Generating...")
    paths = []

    StarVisualizer(w, h, Colors.STAR, "⭐ Stars").animate(
        stars, "assets/metric_stars.gif", frames, fps
    )
    paths.append("assets/metric_stars.gif")

    ForkVisualizer(w, h, Colors.FORK, "🍴 Forks").animate(
        forks, "assets/metric_forks.gif", frames, fps
    )
    paths.append("assets/metric_forks.gif")

    IssueVisualizer(w, h, Colors.ISSUE, "📋 Issues").animate(
        issues, "assets/metric_issues.gif", frames, fps
    )
    paths.append("assets/metric_issues.gif")

    ContributorVisualizer(w, h, Colors.CONTRIBUTOR, "👥 Contributors").animate(
        contributors, "assets/metric_contributors.gif", frames, fps
    )
    paths.append("assets/metric_contributors.gif")

    make_dashboard(paths, "assets/metrics_dashboard.gif", fps)

    print("\n✅ Done: assets/metrics_dashboard.gif")
    print("=" * 50)


if __name__ == "__main__":
    main()
