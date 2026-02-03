#!/usr/bin/env python3
"""
GitHub Metrics Dashboard GIF Generator

Generates a smooth, particle-based scientific/technological dashboard visualization
for GitHub repository metrics using AnimateDiff for GIF generation.

Optimized for GitHub Actions with CPU rendering.
"""

import json
import os
from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFont
from diffusers import AnimateDiffPipeline, LCMScheduler, MotionAdapter
from diffusers.utils import export_to_gif

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

# Save metrics data for reference
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


def create_particle_prompt(
    metric_name: str, metric_value: int, frame_num: int, total_frames: int
) -> tuple[str, str]:
    """
    Create a prompt for particle-based scientific visualization with smooth animation.

    The prompt engineering focuses on:
    - Particle effects with subtle motion
    - Scientific/technological aesthetic
    - Clean, modern dashboard style
    - Consistent visual language across frames for smooth looping
    """

    # Base style keywords for particle scientific visualization
    base_style = (
        "particle visualization, data particles, digital particles, "
        "scientific dashboard, tech metrics, modern UI, "
        "glowing particles, neon particles, light particles, "
        "smooth gradient, futuristic interface, holographic display, "
        "minimalist tech, clean design, professional data visualization, "
        "8k resolution, high detail, cinematic lighting"
    )

    # Negative prompt to avoid common artifacts
    negative_prompt = (
        "ugly, blurry, low quality, distorted, warped, "
        "text overlay, numbers, labels, clutter, noise, "
        "grayscale, dull, flat, cartoon, anime, sketch, "
        "bad anatomy, deformed, extra limbs, mutation"
    )

    # Frame-specific animation hint for smooth looping
    frame_phase = frame_num / total_frames
    if frame_phase < 0.25:
        animation_hint = "gentle particle emergence, subtle pulse"
    elif frame_phase < 0.5:
        animation_hint = "smooth particle flow, steady glow"
    elif frame_phase < 0.75:
        animation_hint = "continuous particle motion, stable shimmer"
    else:
        animation_hint = "gentle particle convergence, smooth fade"

    # Metric-specific visualization
    metric_descriptions = {
        "stars": f"celestial star particles representing {metric_value} stars",
        "forks": f"branching network particles showing {metric_value} repository forks",
        "issues": f"data point particles illustrating {metric_value} open issues",
        "commits": f"timeline particles displaying {metric_value} total commits",
        "contributors": f"network node particles showing {metric_value} contributors",
        "activity": f"activity pulse particles for {metric_value} recent events",
    }

    prompt = (
        f"{metric_descriptions.get(metric_name, f'data particles for {metric_name}')}, "
        f"{base_style}, {animation_hint}, "
        "particle density, distributed particles, balanced composition, "
        "soft particle edges, ambient glow, depth of field, "
        "cyberpunk aesthetics, technological elegance"
    )

    return prompt, negative_prompt


def create_overlay_image(
    metrics: dict, frame_num: int, total_frames: int
) -> Image.Image:
    """
    Create a clean overlay image with metric labels.
    This provides consistent text that can be composited over the generated frames.
    """
    width, height = 800, 400
    bg = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)

    # Semi-transparent dark overlay for text readability
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 100))
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # Note: In a production environment, you would load a .ttf font
    # For now, we'll create a placeholder visual indicator
    # The particle visualization itself will carry the meaning

    return bg


def generate_particle_gif(
    metrics: dict, output_filename: str = "metrics_dashboard.gif"
):
    """
    Generate a smooth GIF visualization using AnimateDiff with particle effects.

    Optimized for GitHub Actions CPU rendering:
    - 8 frames for smooth loop (not too many for CPU)
    - Low inference steps (6-8) for speed
    - Attention slicing for memory efficiency
    - Motion adapter for animation
    """

    print("Loading AnimateDiff pipeline with motion adapter...")

    # Load motion adapter for animation
    adapter = MotionAdapter.from_pretrained("wangfuyun/AnimateLCM")

    # Use a realistics model compatible with AnimateDiff
    pipe = AnimateDiffPipeline.from_pretrained(
        "emilianJR/epiCRealism", motion_adapter=adapter, torch_dtype=torch.float32
    )

    # Use LCM scheduler for fast inference
    pipe.scheduler = LCMScheduler.from_config(
        pipe.scheduler.config, beta_schedule="linear"
    )

    # Load LCM LoRA for speed
    pipe.load_lora_weights(
        "wangfuyun/AnimateLCM",
        weight_name="sd15_lora_beta.safetensors",
        adapter_name="lcm-lora",
    )

    # Set adapters
    pipe.set_adapters(["lcm-lora"], [1.0])

    # Enable optimizations for CPU
    pipe.enable_attention_slicing()
    pipe.enable_model_cpu_offload()

    # GIF settings - optimized for GitHub Actions
    num_frames = 8  # Balanced between smoothness and render time
    fps = 8  # Frames per second for smooth playback

    print(f"Generating {num_frames} frames for smooth loop...")

    # Generate frames for each metric category
    all_frames = []
    metric_categories = [
        ("stars", stars, "⭐ Stars"),
        ("forks", forks, "🍴 Forks"),
        ("issues", issues, "📋 Issues"),
        ("contributors", contributors, "👥 Contributors"),
    ]

    for metric_name, metric_value, display_name in metric_categories:
        print(f"Processing {metric_name}: {metric_value}")

        metric_frames = []
        for frame_num in range(num_frames):
            prompt, negative_prompt = create_particle_prompt(
                metric_name, metric_value, frame_num, num_frames
            )

            # Generate frame with low inference steps for speed
            output = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_frames=1,  # Generate one frame at a time
                guidance_scale=1.5,
                num_inference_steps=6,  # Low for speed
                generator=torch.Generator("cpu").manual_seed(frame_num * 42),
                height=400,
                width=800,
            )

            frame = output.images[0]
            metric_frames.append(frame)

        # Resize frames to consistent size and create grid
        metric_frames = [f.resize((400, 200), Image.LANCZOS) for f in metric_frames]
        all_frames.extend(metric_frames)

    # Create a combined dashboard layout
    print("Creating combined dashboard visualization...")
    dashboard_frames = []

    for frame_idx in range(num_frames):
        # Create 2x2 grid for 4 metrics
        frame_images = []
        for metric_idx in range(4):
            frame_images.append(all_frames[metric_idx * num_frames + frame_idx])

        # Combine into 2x2 grid
        row1 = Image.hstack([frame_images[0], frame_images[1]])
        row2 = Image.hstack([frame_images[2], frame_images[3]])
        dashboard = Image.vstack([row1, row2])

        # Add subtle title bar
        title_bar = Image.new("RGB", (dashboard.width, 40), (20, 20, 30))
        dashboard = Image.vstack([title_bar, dashboard])

        dashboard_frames.append(dashboard)

    # Export to GIF
    print(f"Exporting to {output_filename}...")
    export_to_gif(
        dashboard_frames,
        output_filename,
        fps=fps,
        loop=0,  # Infinite loop
    )

    print(f"✅ GIF generated successfully: {output_filename}")
    print(f"   - Frames: {len(dashboard_frames)}")
    print(f"   - FPS: {fps}")
    print(f"   - Loop: infinite")

    return output_filename


def create_fallback_static_images(metrics: dict):
    """
    Create fallback static images if AnimateDiff is not available.
    Uses simple particle-like visualization with PIL.
    """

    print("Creating fallback static particle visualizations...")

    metric_categories = [
        ("stars", stars, "⭐"),
        ("forks", forks, "🍴"),
        ("issues", issues, "📋"),
        ("contributors", contributors, "👥"),
    ]

    for i, (metric_name, metric_value, icon) in enumerate(metric_categories):
        # Create a clean visualization
        width, height = 800, 400

        # Dark background
        img = Image.new("RGB", (width, height), color=(15, 15, 25))
        draw = ImageDraw.Draw(img)

        # Draw particle-like circles
        import random

        random.seed(42 + i)  # Consistent for each metric

        for _ in range(50):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            r = random.randint(2, 8)

            # Glowing effect
            for glow_r in range(r, r + 15):
                alpha = int(255 * (1 - (glow_r - r) / 15))
                color = (100, 200, 255 if i % 2 == 0 else 255, 200, 100)
                draw.ellipse(
                    [x - glow_r, y - glow_r, x + glow_r, y + glow_r],
                    fill=color[:3] + (alpha,),
                )

        # Add metric value prominently
        draw.text(
            (width // 2, height // 2),
            f"{metric_value}",
            fill=(255, 255, 255),
            anchor="mm",
        )

        # Save
        img.save(f"assets/metric_{i + 1}.png")
        print(f"  Saved: assets/metric_{i + 1}.png")

    # Also create a combined static image
    combined = Image.new("RGB", (1600, 800))
    for i in range(4):
        img = Image.open(f"assets/metric_{i + 1}.png")
        x = (i % 2) * 800
        y = (i // 2) * 400
        combined.paste(img, (x, y))
    combined.save("assets/metrics_dashboard.png")
    print("Saved: assets/metrics_dashboard.png")


def main():
    """Main entry point."""

    print("=" * 60)
    print("GitHub Metrics Dashboard Generator")
    print("=" * 60)
    print(f"Metrics: stars={stars}, forks={forks}, issues={issues}")
    print(f"         commits={commits}, contributors={contributors}")
    print(f"         PRs (30d)={prs_30d}, Issues (30d)={issues_30d}")
    print("=" * 60)

    metrics = {
        "stars": stars,
        "forks": forks,
        "issues": issues,
        "commits": commits,
        "contributors": contributors,
        "prs_30d": prs_30d,
        "issues_30d": issues_30d,
    }

    # Try to generate animated GIF
    try:
        gif_path = generate_particle_gif(metrics, "assets/metrics_dashboard.gif")
        print(f"\n✅ Success! Generated: {gif_path}")

        # Also save prompts used
        prompts_info = []
        for metric_name in ["stars", "forks", "issues", "contributors"]:
            metric_value = metrics.get(metric_name, 0)
            prompt, negative_prompt = create_particle_prompt(
                metric_name, metric_value, 0, 8
            )
            prompts_info.append(
                {
                    "metric": metric_name,
                    "value": metric_value,
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                }
            )

        with open("prompts.json", "w") as f:
            json.dump(prompts_info, f, indent=2)

    except Exception as e:
        print(f"\n❌ AnimateDiff failed: {e}")
        print("Using fallback static image generation...")

        create_fallback_static_images(metrics)

        # Create a simple placeholder GIF from static images
        try:
            from PIL import Image as PILImage

            frames = []
            for i in range(4):
                img = PILImage.open(f"assets/metric_{i + 1}.png")
                frames.append(img.copy())
                img.close()

            # Add some variation by slightly rotating each frame
            varied_frames = []
            for i, frame in enumerate(frames):
                varied_frames.append(frame)
                # Add frame with slight brightness variation
                from PIL import ImageEnhance

                enhancer = ImageEnhance.Brightness(frame)
                varied = enhancer.enhance(0.95 + (i * 0.02))
                varied_frames.append(varied)

            varied_frames[0].save(
                "assets/metrics_dashboard.gif",
                save_all=True,
                append_images=varied_frames[1:],
                duration=200,
                loop=0,
            )
            print("✅ Created fallback GIF from static images")

        except Exception as gif_error:
            print(f"⚠️  Could not create fallback GIF: {gif_error}")
            print("   Static images available in assets/")

    print("\n" + "=" * 60)
    print("Generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
