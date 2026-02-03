#!/usr/bin/env python3
"""
GitHub Metrics Dashboard - Lightweight Particle Animation Generator

Creates beautiful, smooth particle-based visualizations using pure Python.
Fast, efficient, and renders in seconds on CPU.
"""

import json
import math
import os
import random
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

# Metrics collection
stars = int(os.environ.get("STARS", "0"))
forks = int(os.environ.get("FORKS", "0"))
issues = int(os.environ.get("ISSUES", "0"))
commits = int(os.environ.get("COMMITS", "0"))
contributors = int(os.environ.get("CONTRIBUTORS", "0"))
prs_30d = int(os.environ.get("PRS_30D", "0"))
issues_30d = int(os.environ.get("ISSUES_30D", "0"))

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
    """Color palettes for each metric type."""

    STAR = {
        "primary": (255, 200, 80),
        "secondary": (255, 150, 50),
        "glow": (255, 220, 150),
        "bg": (15, 12, 20),
    }
    FORK = {
        "primary": (150, 120, 255),
        "secondary": (80, 200, 255),
        "glow": (200, 180, 255),
        "bg": (15, 12, 20),
    }
    ISSUE = {
        "primary": (255, 120, 80),
        "secondary": (255, 180, 100),
        "glow": (255, 220, 180),
        "bg": (20, 15, 15),
    }
    CONTRIBUTOR = {
        "primary": (80, 220, 150),
        "secondary": (100, 180, 255),
        "glow": (180, 255, 220),
        "bg": (12, 15, 18),
    }

    DASHBOARD_BG = (10, 10, 15)


class Particle:
    def __init__(self, x, y, vx, vy, size, color, life=1.0, decay=0.01):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.base_size = size
        self.size = size
        self.color = color
        self.life = life
        self.decay = decay
        self.pulse_phase = random.random() * 2 * math.pi

    def update(self, dt=1.0):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= self.decay * dt
        self.pulse_phase += 0.1 * dt
        return self.life > 0

    def get_current_size(self):
        pulse = 0.85 + 0.15 * math.sin(self.pulse_phase)
        return self.base_size * self.life * pulse


class ParticleSystem:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.particles = []
        self.time = 0.0

    def clear(self):
        self.particles.clear()

    def spawn(
        self,
        x,
        y,
        count=1,
        size_range=(2, 6),
        speed_range=(0.5, 2.0),
        color=(255, 255, 255),
        life=1.0,
        decay=0.01,
        angle_range=(0, 2 * math.pi),
    ):
        for _ in range(count):
            angle = random.uniform(*angle_range)
            speed = random.uniform(*speed_range)
            self.particles.append(
                Particle(
                    x,
                    y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    random.uniform(*size_range),
                    color,
                    life,
                    decay,
                )
            )

    def update(self, dt=1.0):
        self.time += dt
        self.particles = [p for p in self.particles if p.update(dt)]
        return len(self.particles)

    def render(self, img, glow=True):
        draw = ImageDraw.Draw(img)

        if glow:
            glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_img)
            for p in self.particles:
                size = p.get_current_size() * 3
                alpha = int(60 * p.life)
                glow_draw.ellipse(
                    [p.x - size, p.y - size, p.x + size, p.y + size],
                    fill=p.color + (alpha,),
                )
            img = Image.alpha_composite(img.convert("RGBA"), glow_img).convert("RGB")
            draw = ImageDraw.Draw(img)

        for p in self.particles:
            size = p.get_current_size()
            draw.ellipse([p.x - size, p.y - size, p.x + size, p.y + size], fill=p.color)


class MetricVisualizer:
    def __init__(self, width, height, palette, label):
        self.width, self.height = width, height
        self.palette = palette
        self.label = label
        self.system = ParticleSystem(width, height)
        self.time = 0.0

    def get_particle_count(self, metric_value):
        if metric_value == 0:
            return 5
        return min(40, max(5, int(math.log(metric_value + 1) * 6)))

    def generate_frame(self, metric_value, frame_idx, total_frames):
        bg_color = self.palette["bg"]
        img = Image.new("RGB", (self.width, self.height), bg_color)
        self.time = frame_idx * 0.12

        center_x, center_y = self.width // 2, self.height // 2

        # Draw label at top
        draw = ImageDraw.Draw(img)
        label_text = f"{self.label}"
        bbox = draw.textbbox((0, 0), label_text)
        text_w = bbox[2] - bbox[0]
        draw.text(
            ((self.width - text_w) / 2, 15), label_text, fill=self.palette["secondary"]
        )

        # Draw metric value at bottom
        value_text = f"{metric_value:,}"
        bbox = draw.textbbox((0, 0), value_text)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((self.width - text_w) / 2, self.height - text_h - 20),
            value_text,
            fill=self.palette["primary"],
        )

        return img

    def animate(self, metric_value, output_path, keyframes=12, fps=10):
        print(f"  Generating {self.label} ({keyframes} frames)...")
        frames = []

        for i in range(keyframes):
            frame = self.generate_frame(metric_value, i, keyframes)
            frames.append(frame)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=int(1000 / fps),
            loop=0,
            optimize=True,
        )
        print(f"  Saved: {output_path}")


class StarVisualizer(MetricVisualizer):
    def generate_frame(self, metric_value, frame_idx, total_frames):
        img = super().generate_frame(metric_value, frame_idx, total_frames)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.width // 2, self.height // 2 - 10
        time = self.time

        # Orbiting particles
        count = self.get_particle_count(metric_value)
        for i in range(count):
            angle = (i / count) * 2 * math.pi + time * 0.4
            radius = 35 + 15 * math.sin(time + i * 0.2)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            self.system.spawn(
                x, y, 1, (2, 4), (0.1, 0.3), self.palette["primary"], 0.5, 0.012
            )

        # Twinkling stars
        for _ in range(3):
            x = random.randint(30, self.width - 30)
            y = random.randint(50, self.height - 80)
            brightness = 0.4 + 0.6 * math.sin(time * 2 + x * 0.1)
            color = tuple(int(c * brightness) for c in self.palette["glow"])
            self.system.spawn(x, y, 1, (1, 2), (0, 0), color, 0.4, 0.02)

        self.system.update()
        self.system.render(img, glow=True)

        return img


class ForkVisualizer(MetricVisualizer):
    def generate_frame(self, metric_value, frame_idx, total_frames):
        img = super().generate_frame(metric_value, frame_idx, total_frames)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.width // 2, self.height // 2 - 10
        time = self.time

        # Branching network
        branches = min(8, max(2, int(math.sqrt(metric_value + 1)) + 2))
        for i in range(branches):
            angle = (i / branches) * 2 * math.pi - math.pi / 2 + time * 0.1
            length = 45 + 10 * math.sin(time + i * 0.4)
            end_x = center_x + math.cos(angle) * length
            end_y = center_y + math.sin(angle) * length
            draw.line(
                [center_x, center_y, end_x, end_y],
                fill=self.palette["primary"],
                width=2,
            )

        # Floating particles
        count = self.get_particle_count(metric_value)
        for i in range(count):
            angle = (i / count) * 2 * math.pi + time * 0.3
            radius = 25 + 20 * abs(math.sin(time + i * 0.15))
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            self.system.spawn(
                x, y, 1, (2, 3), (0.2, 0.4), self.palette["glow"], 0.4, 0.015
            )

        self.system.update()
        self.system.render(img, glow=True)
        return img


class IssueVisualizer(MetricVisualizer):
    def generate_frame(self, metric_value, frame_idx, total_frames):
        img = super().generate_frame(metric_value, frame_idx, total_frames)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.width // 2, self.height // 2 - 10
        time = self.time

        # Pulse rings
        pulse_size = 30 + 10 * math.sin(time * 2.5)
        for i in range(2):
            ring_size = pulse_size + i * 12
            draw.ellipse(
                [
                    center_x - ring_size,
                    center_y - ring_size,
                    center_x + ring_size,
                    center_y + ring_size,
                ],
                outline=self.palette["primary"],
                width=2,
            )

        # Rising particles
        count = self.get_particle_count(metric_value)
        for i in range(count):
            y = (
                self.height
                - 70
                - (frame_idx / total_frames) * 80
                + 20 * math.sin(time + i)
            )
            x = center_x + (i - count / 2) * 15 + 8 * math.sin(time + i * 0.5)
            size = 2.5 + math.sin(time * 2 + i) * 1
            self.system.spawn(
                x,
                y,
                1,
                (size, size),
                (0, -0.4 - i * 0.02),
                self.palette["primary"],
                0.6,
                0.012,
            )

        self.system.update()
        self.system.render(img, glow=True)
        return img


class ContributorVisualizer(MetricVisualizer):
    def generate_frame(self, metric_value, frame_idx, total_frames):
        img = super().generate_frame(metric_value, frame_idx, total_frames)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.width // 2, self.height // 2 - 10
        time = self.time

        # Connected nodes
        nodes = min(12, max(2, metric_value))
        node_pos = []
        for i in range(nodes):
            angle = (i / nodes) * 2 * math.pi + time * 0.12
            radius = 30 + 15 * math.sin(time + i * 0.4)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            node_pos.append((x, y))
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=self.palette["primary"])

        # Connections
        for i in range(len(node_pos)):
            for j in range(i + 1, len(node_pos)):
                x1, y1 = node_pos[i]
                x2, y2 = node_pos[j]
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < 70:
                    alpha = int(150 * (1 - dist / 70))
                    color = tuple(
                        int(c * alpha / 255) for c in self.palette["secondary"]
                    )
                    draw.line([x1, y1, x2, y2], fill=color, width=1)

        # Orbiting particles
        count = self.get_particle_count(metric_value)
        for i in range(count):
            angle = (i / count) * 2 * math.pi + time * 0.5
            radius = 20 + 10 * math.sin(time + i * 0.25)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            self.system.spawn(
                x, y, 1, (1.5, 2.5), (0.1, 0.25), self.palette["glow"], 0.4, 0.015
            )

        self.system.update()
        self.system.render(img, glow=True)
        return img


def hstack_images(images):
    if not images:
        raise ValueError("No images to stack")
    widths, heights = zip(*(img.size for img in images))
    max_h = max(heights)
    total_w = sum(widths)
    result = Image.new("RGB", (total_w, max_h))
    x = 0
    for img in images:
        result.paste(img, (x, (max_h - img.height) // 2))
        x += img.width
    return result


def vstack_images(images):
    if not images:
        raise ValueError("No images to stack")
    widths, heights = zip(*(img.size for img in images))
    max_w = max(widths)
    total_h = sum(heights)
    result = Image.new("RGB", (max_w, total_h))
    y = 0
    for img in images:
        result.paste(img, ((max_w - img.width) // 2, y))
        y += img.height
    return result


def create_combined_gif(frame_paths, output_path, fps=10):
    print("Creating combined dashboard...")
    all_frames = []
    for path in frame_paths:
        try:
            frames = []
            with Image.open(path) as img:
                while True:
                    frames.append(img.copy())
                    try:
                        img.seek(img.tell() + 1)
                    except EOFError:
                        break
            all_frames.append(frames)
            print(f"  Loaded {len(frames)} frames from {path}")
        except Exception as e:
            print(f"  Warning: Could not load {path}: {e}")
            all_frames.append([Image.new("RGB", (200, 120), (30, 30, 40))])

    min_frames = min(len(f) for f in all_frames)
    print(f"  Combining {min_frames} frames each...")

    combined = []
    for i in range(min_frames):
        row = []
        for frames in all_frames:
            row.append(
                frames[min(i, len(frames) - 1)].resize((200, 120), Image.LANCZOS)
            )
        dashboard = hstack_images(row)
        combined.append(dashboard)

    combined[0].save(
        output_path,
        save_all=True,
        append_images=combined[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )
    print(f"  Saved: {output_path}")


def main():
    print("=" * 50)
    print("GitHub Metrics Dashboard Generator")
    print("=" * 50)
    print(f"Metrics: ⭐ {stars} | 🍴 {forks} | 📋 {issues} | 👥 {contributors}")
    print("=" * 50)

    width, height = 200, 120
    fps = 10
    keyframes = 12

    # Generate individual metric GIFs
    frame_paths = []

    print("\n🎨 Generating visualizations...")
    StarVisualizer(width, height, Colors.STAR, "⭐ Stars").animate(
        stars, "assets/metric_stars.gif", keyframes, fps
    )
    frame_paths.append("assets/metric_stars.gif")

    ForkVisualizer(width, height, Colors.FORK, "🍴 Forks").animate(
        forks, "assets/metric_forks.gif", keyframes, fps
    )
    frame_paths.append("assets/metric_forks.gif")

    IssueVisualizer(width, height, Colors.ISSUE, "📋 Issues").animate(
        issues, "assets/metric_issues.gif", keyframes, fps
    )
    frame_paths.append("assets/metric_issues.gif")

    ContributorVisualizer(width, height, Colors.CONTRIBUTOR, "👥 Contributors").animate(
        contributors, "assets/metric_contributors.gif", keyframes, fps
    )
    frame_paths.append("assets/metric_contributors.gif")

    # Create combined dashboard
    create_combined_gif(frame_paths, "assets/metrics_dashboard.gif", fps)

    print("\n" + "=" * 50)
    print("✅ Complete! Output: assets/metrics_dashboard.gif")
    print("=" * 50)


if __name__ == "__main__":
    main()
