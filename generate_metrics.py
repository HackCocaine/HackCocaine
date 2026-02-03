#!/usr/bin/env python3
"""
GitHub Metrics Dashboard - Lightweight Particle Animation Generator

Creates beautiful, smooth particle-based visualizations using pure Python.
Fast, efficient, and renders in seconds on CPU.

Visualization Style:
- Stars: Glowing golden star particles with pulsing core
- Forks: Network branching particles (紫色/cyan)
- Issues: Alert/warning pulse particles (orange/red)
- Contributors: Connected node network particles (green/blue)
- Activity: Timeline wave particles (blue/purple gradient)
"""

import json
import math
import os
import random
from pathlib import Path
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Metrics collection
stars = int(os.environ.get("STARS", "0"))
forks = int(os.environ.get("FORKS", "0"))
issues = int(os.environ.get("ISSUES", "0"))
commits = int(os.environ.get("COMMITS", "0"))
contributors = int(os.environ.get("CONTRIBUTORS", "0"))
prs_30d = int(os.environ.get("PRS_30D", "0"))
issues_30d = int(os.environ.get("ISSUES_30D", "0"))

# Create assets directory
assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Save metrics data
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


# ============================================================================
# COLOR PALETTES - Aesthetic and modern
# ============================================================================
class Colors:
    """Beautiful color palettes for each metric type."""

    STAR = {
        "primary": (255, 200, 80),  # Golden
        "secondary": (255, 150, 50),  # Orange-gold
        "glow": (255, 220, 150),  # Light gold
        "bg": (20, 18, 28),  # Dark background
    }

    FORK = {
        "primary": (150, 120, 255),  # Purple
        "secondary": (80, 200, 255),  # Cyan
        "glow": (200, 180, 255),  # Light purple
        "bg": (18, 20, 30),
    }

    ISSUE = {
        "primary": (255, 120, 80),  # Coral
        "secondary": (255, 180, 100),  # Warm orange
        "glow": (255, 220, 180),  # Light coral
        "bg": (25, 20, 20),
    }

    CONTRIBUTOR = {
        "primary": (80, 220, 150),  # Mint green
        "secondary": (100, 180, 255),  # Sky blue
        "glow": (180, 255, 220),  # Light mint
        "bg": (18, 22, 25),
    }

    ACTIVITY = {
        "primary": (120, 150, 255),  # Periwinkle
        "secondary": (180, 100, 255),  # Violet
        "glow": (200, 180, 255),  # Light violet
        "bg": (20, 18, 30),
    }

    DASHBOARD_BG = (15, 15, 22)


# ============================================================================
# PARTICLE SYSTEM - Lightweight and beautiful
# ============================================================================
class Particle:
    """A single particle with position, velocity, and visual properties."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        size: float,
        color: tuple,
        life: float = 1.0,
        decay: float = 0.01,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.base_size = size
        self.color = color
        self.life = life
        self.decay = decay
        self.pulse_phase = random.random() * 2 * math.pi

    def update(self, dt: float = 1.0) -> bool:
        """Update particle physics. Returns False if dead."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= self.decay * dt
        self.pulse_phase += 0.1 * dt
        return self.life > 0

    def get_current_size(self) -> float:
        """Get pulsating size."""
        pulse = 0.8 + 0.2 * math.sin(self.pulse_phase)
        return self.base_size * self.life * pulse


class ParticleSystem:
    """Manages a collection of particles with spawning and updates."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.particles: list[Particle] = []
        self.time = 0.0

    def clear(self):
        """Remove all particles."""
        self.particles.clear()

    def spawn(
        self,
        x: float,
        y: float,
        count: int = 1,
        size_range: tuple = (2, 6),
        speed_range: tuple = (0.5, 2.0),
        color: tuple = (255, 255, 255),
        life: float = 1.0,
        decay: float = 0.01,
        angle_range: tuple = (0, 2 * math.pi),
    ):
        """Spawn particles at a point with radial velocity."""
        for _ in range(count):
            angle = random.uniform(*angle_range)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(*size_range)

            self.particles.append(Particle(x, y, vx, vy, size, color, life, decay))

    def spawn_burst(
        self,
        x: float,
        y: float,
        count: int = 10,
        size: float = 4,
        speed: float = 3.0,
        color: tuple = (255, 255, 255),
        life: float = 1.0,
    ):
        """Spawn a burst of particles in all directions."""
        self.spawn(
            x,
            y,
            count,
            (size * 0.8, size * 1.2),
            (speed * 0.5, speed),
            color,
            life,
            0.02,
            (0, 2 * math.pi),
        )

    def update(self, dt: float = 1.0) -> int:
        """Update all particles. Returns count of alive particles."""
        self.time += dt
        self.particles = [p for p in self.particles if p.update(dt)]
        return len(self.particles)

    def render(self, img: Image.Image, glow: bool = True):
        """Render particles onto image with optional glow effect."""
        draw = ImageDraw.Draw(img)

        if glow:
            # Create glow layer
            glow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_img)

            for p in self.particles:
                size = p.get_current_size()
                # Draw glow
                glow_size = size * 4
                alpha = int(80 * p.life)
                glow_draw.ellipse(
                    [
                        p.x - glow_size,
                        p.y - glow_size,
                        p.x + glow_size,
                        p.y + glow_size,
                    ],
                    fill=p.color + (alpha,),
                )

            # Composite glow
            img = Image.alpha_composite(img.convert("RGBA"), glow_img).convert("RGB")
            draw = ImageDraw.Draw(img)

        for p in self.particles:
            size = p.get_current_size()
            draw.ellipse([p.x - size, p.y - size, p.x + size, p.y + size], fill=p.color)


# ============================================================================
# METRIC VISUALIZATIONS - Beautiful and data-driven
# ============================================================================
class MetricVisualizer:
    """Base class for metric visualizations."""

    def __init__(self, width: int, height: int, palette: dict):
        self.width = width
        self.height = height
        self.palette = palette
        self.system = ParticleSystem(width, height)
        self.time = 0.0

    def get_particle_count(self, metric_value: int) -> int:
        """Calculate particle count based on metric value."""
        if metric_value == 0:
            return 5
        return min(50, max(5, int(math.sqrt(metric_value) * 3)))

    def get_particle_speed(self, metric_value: int) -> float:
        """Calculate particle speed based on metric value."""
        return 0.5 + min(2.0, metric_value / 100)

    def generate_frame(
        self, metric_value: int, frame_idx: int, total_frames: int
    ) -> Image.Image:
        """Generate a single frame. Override in subclasses."""
        raise NotImplementedError


class StarVisualizer(MetricVisualizer):
    """Glowing star particles with pulsing core."""

    def get_particle_count(self, metric_value: int) -> int:
        if metric_value == 0:
            return 8
        return min(60, max(8, int(math.log(metric_value + 1) * 8)))

    def generate_frame(
        self, metric_value: int, frame_idx: int, total_frames: int
    ) -> Image.Image:
        bg_color = self.palette["bg"]
        img = Image.new("RGB", (self.width, self.height), bg_color)

        progress = frame_idx / total_frames
        time = frame_idx * 0.15

        # Central pulsing core
        core_size = 30 + 10 * math.sin(time * 2)
        center_x, center_y = self.width // 2, self.height // 2

        # Draw starburst from center
        for i in range(8):
            angle = (i / 8) * 2 * math.pi + time * 0.5
            length = 40 + 20 * math.sin(time + i * 0.5)
            end_x = center_x + math.cos(angle) * length
            end_y = center_y + math.sin(angle) * length

            # Draw ray
            draw = ImageDraw.Draw(img)
            draw.line(
                [center_x, center_y, end_x, end_y],
                fill=self.palette["primary"],
                width=2,
            )

        # Orbiting particles
        orbit_count = self.get_particle_count(metric_value)
        for i in range(orbit_count):
            angle = (i / orbit_count) * 2 * math.pi + time * 0.3
            radius = 50 + 20 * math.sin(time * 2 + i * 0.3)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius

            self.system.spawn(
                x, y, 1, (3, 5), (0.1, 0.3), self.palette["primary"], 0.5, 0.01
            )

        # Add twinkling background stars
        for _ in range(5):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            brightness = 0.5 + 0.5 * math.sin(time * 3 + x * 0.1)
            color = tuple(int(c * brightness) for c in self.palette["glow"])
            self.system.spawn(x, y, 1, (1, 2), (0, 0), color, 0.3, 0.02)

        # Draw particles
        self.system.update()
        self.system.render(img, glow=True)

        # Draw metric value
        draw = ImageDraw.Draw(img)
        text = f"{metric_value:,}"
        # Use default font if custom not available
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            ((self.width - text_width) / 2, self.height - text_height - 20),
            text,
            fill=self.palette["primary"],
        )

        return img


class ForkVisualizer(MetricVisualizer):
    """Network branching particles - fork visualization."""

    def generate_frame(
        self, metric_value: int, frame_idx: int, total_frames: int
    ) -> Image.Image:
        bg_color = self.palette["bg"]
        img = Image.new("RGB", (self.width, self.height), bg_color)

        time = frame_idx * 0.12
        center_x, center_y = self.width // 2, self.height // 2

        # Draw branching network
        num_branches = min(12, max(3, int(math.sqrt(metric_value + 1))))
        for i in range(num_branches):
            angle = (i / num_branches) * 2 * math.pi - math.pi / 2
            length = 60 + 15 * math.sin(time + i * 0.5)

            # Main branch
            end_x = center_x + math.cos(angle) * length
            end_y = center_y + math.sin(angle) * length

            draw = ImageDraw.Draw(img)
            draw.line(
                [center_x, center_y, end_x, end_y],
                fill=self.palette["primary"],
                width=2,
            )

            # Sub-branches
            for j in range(2):
                sub_angle = angle + (j - 0.5) * 0.5 + time * 0.1
                sub_length = length * 0.4
                sub_end_x = end_x + math.cos(sub_angle) * sub_length
                sub_end_y = end_y + math.sin(sub_angle) * sub_length

                draw.line(
                    [end_x, end_y, sub_end_x, sub_end_y],
                    fill=self.palette["secondary"],
                    width=1,
                )

        # Floating particles along branches
        particle_count = self.get_particle_count(metric_value)
        for i in range(particle_count):
            angle = (i / particle_count) * 2 * math.pi + time * 0.2
            radius = 40 + 30 * abs(math.sin(time + i * 0.2))
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius

            self.system.spawn(
                x, y, 1, (2, 4), (0.2, 0.5), self.palette["glow"], 0.4, 0.015
            )

        self.system.update()
        self.system.render(img, glow=True)

        # Draw metric value
        draw = ImageDraw.Draw(img)
        text = f"{metric_value:,}"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            ((self.width - text_width) / 2, self.height - text_height - 20),
            text,
            fill=self.palette["primary"],
        )

        return img


class IssueVisualizer(MetricVisualizer):
    """Alert/pulse particles - issue indicators."""

    def get_particle_count(self, metric_value: int) -> int:
        if metric_value == 0:
            return 5
        return min(40, max(5, int(metric_value / 2)))

    def generate_frame(
        self, metric_value: int, frame_idx: int, total_frames: int
    ) -> Image.Image:
        bg_color = self.palette["bg"]
        img = Image.new("RGB", (self.width, self.height), bg_color)

        time = frame_idx * 0.2
        center_x, center_y = self.width // 2, self.height // 2

        # Pulsing alert circle
        pulse_size = 40 + 15 * math.sin(time * 3)
        pulse_alpha = int(100 + 50 * math.sin(time * 3))

        draw = ImageDraw.Draw(img)

        # Outer pulse rings
        for i in range(3):
            ring_size = pulse_size + i * 15
            ring_alpha = int((100 - i * 30) * (0.5 + 0.5 * math.sin(time * 2)))
            if ring_alpha > 0:
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

        # Central exclamation mark area
        draw.ellipse(
            [center_x - 35, center_y - 35, center_x + 35, center_y + 35],
            outline=self.palette["secondary"],
            width=2,
        )

        # Rising particles (like issues being raised)
        particle_count = self.get_particle_count(metric_value)
        for i in range(particle_count):
            y = self.height - (frame_idx / total_frames) * self.height * 0.8
            x = center_x + (i - particle_count / 2) * 20 + 10 * math.sin(time + i)
            size = 3 + 2 * math.sin(time * 2 + i)

            self.system.spawn(
                x,
                y,
                1,
                (size, size),
                (0, -0.5 - i * 0.05),
                self.palette["primary"],
                0.6,
                0.012,
            )

        # Floating warning particles
        for _ in range(3):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 100)
            self.system.spawn(
                x, y, 1, (2, 4), (0.3, 0.6), self.palette["secondary"], 0.4, 0.02
            )

        self.system.update()
        self.system.render(img, glow=True)

        # Draw metric value
        draw = ImageDraw.Draw(img)
        text = f"{metric_value:,}"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            ((self.width - text_width) / 2, self.height - text_height - 20),
            text,
            fill=self.palette["primary"],
        )

        return img


class ContributorVisualizer(MetricVisualizer):
    """Connected node network - contributor visualization."""

    def generate_frame(
        self, metric_value: int, frame_idx: int, total_frames: int
    ) -> Image.Image:
        bg_color = self.palette["bg"]
        img = Image.new("RGB", (self.width, self.height), bg_color)

        time = frame_idx * 0.1
        center_x, center_y = self.width // 2, self.height // 2

        draw = ImageDraw.Draw(img)

        # Generate node positions
        num_nodes = min(20, max(3, metric_value))
        nodes = []
        for i in range(num_nodes):
            angle = (i / num_nodes) * 2 * math.pi + time * 0.1
            radius = 40 + 25 * math.sin(time * 2 + i * 0.5)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            nodes.append((x, y))
            draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=self.palette["primary"])

        # Draw connections
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                x1, y1 = nodes[i]
                x2, y2 = nodes[j]
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if dist < 100:  # Only connect nearby nodes
                    alpha = int(255 * (1 - dist / 100))
                    color = tuple(
                        int(c * alpha / 255) for c in self.palette["secondary"]
                    )
                    draw.line([x1, y1, x2, y2], fill=color, width=1)

        # Central hub particle
        self.system.spawn(
            center_x, center_y, 2, (4, 6), (0.5, 1.0), self.palette["glow"], 0.5, 0.01
        )

        # Orbiting connection particles
        particle_count = self.get_particle_count(metric_value)
        for i in range(particle_count):
            angle = (i / particle_count) * 2 * math.pi + time * 0.4
            radius = 30 + 15 * math.sin(time + i * 0.3)
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius

            self.system.spawn(
                x, y, 1, (2, 3), (0.1, 0.3), self.palette["primary"], 0.4, 0.015
            )

        self.system.update()
        self.system.render(img, glow=True)

        # Draw metric value
        draw = ImageDraw.Draw(img)
        text = f"{metric_value:,}"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            ((self.width - text_width) / 2, self.height - text_height - 20),
            text,
            fill=self.palette["primary"],
        )

        return img


# ============================================================================
# GIF GENERATION - Fast and efficient
# ============================================================================
def create_crossfade_frames(
    frames1: list[Image.Image], frames2: list[Image.Image], crossfade_steps: int = 3
) -> list[Image.Image]:
    """Create crossfade between two frame sequences."""
    result = []

    # Forward sequence with crossfade
    for i in range(len(frames1)):
        # Add original frame
        result.append(frames1[i])

        # Add crossfade frames before next keyframe
        if i < len(frames1) - 1 and crossfade_steps > 0:
            for j in range(1, crossfade_steps + 1):
                alpha = j / (crossfade_steps + 1)
                blended = Image.blend(
                    frames1[i].convert("RGBA"), frames1[i + 1].convert("RGBA"), alpha
                )
                result.append(blended.convert("RGB"))

    return result


def create_ping_pong(frames: list[Image.Image]) -> list[Image.Image]:
    """Create ping-pong loop (forward then backward)."""
    if len(frames) < 2:
        return frames

    # Forward
    result = frames.copy()

    # Backward (exclude first and last to avoid jarring transitions)
    for frame in reversed(frames[1:-1]):
        result.append(frame)

    return result


def hstack_images(images: list[Image.Image]) -> Image.Image:
    """Horizontal stack of images."""
    if not images:
        raise ValueError("No images to stack")

    widths, heights = zip(*(img.size for img in images))
    max_height = max(heights)
    total_width = sum(widths)

    result = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for img in images:
        result.paste(img, (x_offset, (max_height - img.height) // 2))
        x_offset += img.width

    return result


def vstack_images(images: list[Image.Image]) -> Image.Image:
    """Vertical stack of images."""
    if not images:
        raise ValueError("No images to stack")

    widths, heights = zip(*(img.size for img in images))
    max_width = max(widths)
    total_height = sum(heights)

    result = Image.new("RGB", (max_width, total_height))

    y_offset = 0
    for img in images:
        result.paste(img, ((max_width - img.width) // 2, y_offset))
        y_offset += img.height

    return result


def generate_metric_gif(
    visualizer: MetricVisualizer,
    metric_value: int,
    output_path: str,
    keyframes: int = 8,
    fps: int = 12,
    width: int = 400,
    height: int = 300,
):
    """Generate a GIF for a single metric."""
    print(f"  Generating {keyframes} keyframes...")

    # Generate keyframes
    keyframe_images = []
    for i in range(keyframes):
        frame = visualizer.generate_frame(metric_value, i, keyframes)
        frame = frame.resize((width, height), Image.LANCZOS)
        keyframe_images.append(frame)

    # Create ping-pong loop for seamless animation
    final_frames = create_ping_pong(keyframe_images)

    # Save as GIF
    final_frames[0].save(
        output_path,
        save_all=True,
        append_images=final_frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )

    print(f"  Saved: {output_path} ({len(final_frames)} frames)")


def create_combined_dashboard(
    frame_paths: list[str],
    output_path: str,
    fps: int = 12,
):
    """Combine individual metric GIFs into a 2x2 dashboard."""
    print("Creating combined dashboard...")

    # Load all frames from each GIF
    all_frame_lists = []
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
            all_frame_lists.append(frames)
            print(f"  Loaded {len(frames)} frames from {path}")
        except Exception as e:
            print(f"  Warning: Could not load {path}: {e}")
            # Create placeholder
            placeholder = Image.new("RGB", (400, 300), (30, 30, 40))
            all_frame_lists.append([placeholder])

    # Find shortest sequence
    min_frames = min(len(frames) for frames in all_frame_lists)
    print(f"  Using {min_frames} frames per metric")

    # Create combined frames
    combined_frames = []
    for i in range(min_frames):
        # Get frame from each metric (or last frame if shorter)
        metric_frames = []
        for frames in all_frame_lists:
            frame = frames[min(i, len(frames) - 1)]
            metric_frames.append(frame.resize((400, 300), Image.LANCZOS))

        # 2x2 grid
        row1 = hstack_images([metric_frames[0], metric_frames[1]])
        row2 = hstack_images([metric_frames[2], metric_frames[3]])
        dashboard = vstack_images([row1, row2])

        # Add title bar
        title_bar = Image.new("RGB", (dashboard.width, 40), (20, 20, 30))
        dashboard = vstack_images([title_bar, dashboard])

        combined_frames.append(dashboard)

    # Save combined dashboard
    combined_frames[0].save(
        output_path,
        save_all=True,
        append_images=combined_frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )

    print(f"  Saved: {output_path} ({len(combined_frames)} frames)")


# ============================================================================
# MAIN GENERATION
# ============================================================================
def main():
    """Generate all metric visualizations."""
    print("=" * 60)
    print("GitHub Metrics Dashboard Generator")
    print("Lightweight Particle Animation System")
    print("=" * 60)
    print(f"Metrics: ⭐ {stars} | 🍴 {forks} | 📋 {issues} | 👥 {contributors}")
    print(f"Activity: {prs_30d} PRs, {issues_30d} issues (30d)")
    print("=" * 60)

    width, height = 400, 300
    fps = 12
    keyframes = 10

    # Generate individual metric GIFs
    frame_paths = []

    # Stars
    print("\n🎯 Generating Stars visualization...")
    star_viz = StarVisualizer(width, height, Colors.STAR)
    frame_path = "assets/metric_stars.gif"
    generate_metric_gif(star_viz, stars, frame_path, keyframes, fps, width, height)
    frame_paths.append(frame_path)

    # Forks
    print("\n🍴 Generating Forks visualization...")
    fork_viz = ForkVisualizer(width, height, Colors.FORK)
    frame_path = "assets/metric_forks.gif"
    generate_metric_gif(fork_viz, forks, frame_path, keyframes, fps, width, height)
    frame_paths.append(frame_path)

    # Issues
    print("\n📋 Generating Issues visualization...")
    issue_viz = IssueVisualizer(width, height, Colors.ISSUE)
    frame_path = "assets/metric_issues.gif"
    generate_metric_gif(issue_viz, issues, frame_path, keyframes, fps, width, height)
    frame_paths.append(frame_path)

    # Contributors
    print("\n👥 Generating Contributors visualization...")
    contrib_viz = ContributorVisualizer(width, height, Colors.CONTRIBUTOR)
    frame_path = "assets/metric_contributors.gif"
    generate_metric_gif(
        contrib_viz, contributors, frame_path, keyframes, fps, width, height
    )
    frame_paths.append(frame_path)

    # Create combined dashboard
    print("\n🎨 Creating combined dashboard...")
    create_combined_dashboard(frame_paths, "assets/metrics_dashboard.gif", fps=fps)

    print("\n" + "=" * 60)
    print("✅ Generation complete!")
    print(f"   Output: assets/metrics_dashboard.gif")
    print(f"   FPS: {fps}, Keyframes: {keyframes}, Loop: infinite")
    print("=" * 60)


if __name__ == "__main__":
    main()
