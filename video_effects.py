"""
Advanced video effects and transitions for Instagram Reels
Creates professional-looking video content with animations and effects
"""

import numpy as np
from moviepy.editor import *
from moviepy.video.fx import resize, fadein, fadeout
from moviepy.video.tools.drawing import color_gradient
import random
from typing import List, Tuple, Dict, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math

class VideoEffects:
    """Advanced video effects for Instagram Reels"""
    
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        
    def create_zoom_effect(self, clip: VideoClip, zoom_factor: float = 1.2, duration: float = None) -> VideoClip:
        """Create smooth zoom effect"""
        if duration is None:
            duration = clip.duration
            
        def zoom_function(t):
            progress = t / duration
            current_zoom = 1 + (zoom_factor - 1) * progress
            return current_zoom
            
        return clip.resize(zoom_function)
    
    def create_pan_effect(self, clip: VideoClip, direction: str = "right", distance: float = 0.1) -> VideoClip:
        """Create panning effect"""
        def pan_function(t):
            progress = t / clip.duration
            
            if direction == "right":
                x_offset = -distance * progress * self.width
                y_offset = 0
            elif direction == "left":
                x_offset = distance * progress * self.width
                y_offset = 0
            elif direction == "up":
                x_offset = 0
                y_offset = distance * progress * self.height
            elif direction == "down":
                x_offset = 0
                y_offset = -distance * progress * self.height
            else:
                x_offset = y_offset = 0
                
            return (x_offset, y_offset)
        
        return clip.set_position(pan_function)
    
    def create_slide_transition(self, clip1: VideoClip, clip2: VideoClip, direction: str = "left", duration: float = 0.5) -> VideoClip:
        """Create slide transition between clips"""
        
        if direction == "left":
            clip1_end = clip1.set_position(lambda t: (-t/duration * self.width, 0))
            clip2_start = clip2.set_position(lambda t: (self.width - t/duration * self.width, 0))
        elif direction == "right":
            clip1_end = clip1.set_position(lambda t: (t/duration * self.width, 0))
            clip2_start = clip2.set_position(lambda t: (-self.width + t/duration * self.width, 0))
        elif direction == "up":
            clip1_end = clip1.set_position(lambda t: (0, -t/duration * self.height))
            clip2_start = clip2.set_position(lambda t: (0, self.height - t/duration * self.height))
        else:  # down
            clip1_end = clip1.set_position(lambda t: (0, t/duration * self.height))
            clip2_start = clip2.set_position(lambda t: (0, -self.height + t/duration * self.height))
        
        # Create transition clips
        transition_clip1 = clip1_end.subclip(clip1.duration - duration, clip1.duration)
        transition_clip2 = clip2_start.subclip(0, duration)
        
        # Composite the transition
        transition = CompositeVideoClip([transition_clip1, transition_clip2], size=(self.width, self.height))
        
        # Combine with main clips
        main_clip1 = clip1.subclip(0, clip1.duration - duration)
        main_clip2 = clip2.subclip(duration, clip2.duration)
        
        return concatenate_videoclips([main_clip1, transition, main_clip2])
    
    def create_text_animation(self, text: str, font_size: int = 60, color: Tuple[int, int, int] = (255, 255, 255),
                            animation_type: str = "fade_in", duration: float = 3.0) -> VideoClip:
        """Create animated text clip"""
        
        # Create text clip
        txt_clip = TextClip(text, fontsize=font_size, color=color, font='Arial-Bold')
        txt_clip = txt_clip.set_duration(duration)
        
        if animation_type == "fade_in":
            txt_clip = txt_clip.fadein(0.5)
        elif animation_type == "slide_up":
            txt_clip = txt_clip.set_position(lambda t: ('center', self.height - (t/duration) * (self.height/2)))
        elif animation_type == "typewriter":
            # Simulate typewriter effect by revealing text progressively
            def make_frame(t):
                progress = min(t / duration, 1.0)
                chars_to_show = int(len(text) * progress)
                partial_text = text[:chars_to_show]
                
                if chars_to_show < len(text):
                    partial_text += "_"  # Cursor effect
                
                partial_clip = TextClip(partial_text, fontsize=font_size, color=color, font='Arial-Bold')
                return partial_clip.get_frame(0)
            
            txt_clip = VideoClip(make_frame, duration=duration)
        elif animation_type == "bounce":
            def bounce_position(t):
                bounce = abs(math.sin(t * 4 * math.pi)) * 50
                return ('center', 'center' if isinstance('center', str) else self.height//2 - bounce)
            txt_clip = txt_clip.set_position(bounce_position)
        
        return txt_clip
    
    def create_particle_effect(self, duration: float = 3.0, particle_count: int = 50) -> VideoClip:
        """Create particle/sparkle effect"""
        
        def make_frame(t):
            # Create blank frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Add particles
            for i in range(particle_count):
                # Seed random with time and particle index for consistent animation
                np.random.seed(int(t * 1000) + i)
                
                # Particle properties
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
                size = np.random.randint(2, 8)
                
                # Sparkle effect - particles appear and disappear
                alpha = abs(math.sin(t * 2 + i)) * 255
                
                # Draw particle (simple circle)
                if 0 <= x < self.width and 0 <= y < self.height:
                    for dx in range(-size, size+1):
                        for dy in range(-size, size+1):
                            if dx*dx + dy*dy <= size*size:
                                px, py = x + dx, y + dy
                                if 0 <= px < self.width and 0 <= py < self.height:
                                    frame[py, px] = [255, 215, 0]  # Gold color
            
            return frame
        
        return VideoClip(make_frame, duration=duration)
    
    def create_gradient_background(self, colors: List[Tuple[int, int, int]], duration: float = 3.0, 
                                 direction: str = "vertical") -> VideoClip:
        """Create animated gradient background"""
        
        def make_frame(t):
            # Create gradient
            if direction == "vertical":
                gradient = np.linspace(0, 1, self.height).reshape(-1, 1)
                gradient = np.repeat(gradient, self.width, axis=1)
            else:  # horizontal
                gradient = np.linspace(0, 1, self.width).reshape(1, -1)
                gradient = np.repeat(gradient, self.height, axis=0)
            
            # Animate between colors
            color_progress = (math.sin(t * 2) + 1) / 2  # Oscillate between 0 and 1
            
            if len(colors) >= 2:
                color1 = np.array(colors[0])
                color2 = np.array(colors[1])
                current_color1 = color1 * (1 - color_progress) + color2 * color_progress
                
                if len(colors) >= 3:
                    color3 = np.array(colors[2])
                    current_color2 = color2 * (1 - color_progress) + color3 * color_progress
                else:
                    current_color2 = color2
            else:
                current_color1 = current_color2 = np.array(colors[0])
            
            # Apply gradient
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for i in range(3):  # RGB channels
                frame[:, :, i] = (current_color1[i] * (1 - gradient) + current_color2[i] * gradient).astype(np.uint8)
            
            return frame
        
        return VideoClip(make_frame, duration=duration)
    
    def create_logo_animation(self, logo_path: str, animation_type: str = "fade_scale", duration: float = 2.0) -> VideoClip:
        """Create animated logo/watermark"""
        
        try:
            logo_clip = ImageClip(logo_path, duration=duration)
            
            # Resize logo to appropriate size
            logo_clip = logo_clip.resize(height=100)  # 100px height
            
            if animation_type == "fade_scale":
                def scale_function(t):
                    progress = t / duration
                    return 0.5 + 0.5 * progress  # Scale from 50% to 100%
                
                logo_clip = logo_clip.resize(scale_function).fadein(0.5)
                
            elif animation_type == "slide_in":
                logo_clip = logo_clip.set_position(lambda t: (self.width - 150, 50))  # Top right
                
            elif animation_type == "rotate":
                def rotate_function(t):
                    return t * 360 / duration  # Full rotation over duration
                
                logo_clip = logo_clip.rotate(rotate_function)
            
            # Position logo (default: bottom right)
            logo_clip = logo_clip.set_position((self.width - logo_clip.w - 20, self.height - logo_clip.h - 20))
            
            return logo_clip
            
        except Exception as e:
            print(f"Error creating logo animation: {e}")
            # Return empty clip if logo fails
            return ColorClip(size=(1, 1), color=(0, 0, 0), duration=duration).set_opacity(0)
    
    def create_product_showcase_effect(self, image_path: str, duration: float = 4.0) -> VideoClip:
        """Create product showcase with multiple effects"""
        
        try:
            # Load and prepare image
            img_clip = ImageClip(image_path, duration=duration)
            
            # Resize to fit screen while maintaining aspect ratio
            img_clip = img_clip.resize(height=self.height * 0.8)
            
            # Center the image
            img_clip = img_clip.set_position('center')
            
            # Add zoom effect
            img_clip = self.create_zoom_effect(img_clip, zoom_factor=1.1, duration=duration)
            
            # Add subtle rotation
            def rotate_function(t):
                return math.sin(t * 2) * 2  # Gentle oscillation
            
            img_clip = img_clip.rotate(rotate_function)
            
            # Add fade in/out
            img_clip = img_clip.fadein(0.5).fadeout(0.5)
            
            # Create background
            bg_colors = [(20, 20, 40), (40, 20, 60), (60, 40, 80)]
            background = self.create_gradient_background(bg_colors, duration)
            
            # Add particle effect
            particles = self.create_particle_effect(duration, particle_count=30)
            particles = particles.set_opacity(0.3)
            
            # Composite everything
            final_clip = CompositeVideoClip([
                background,
                particles,
                img_clip
            ], size=(self.width, self.height))
            
            return final_clip
            
        except Exception as e:
            print(f"Error creating product showcase: {e}")
            # Return gradient background as fallback
            return self.create_gradient_background([(20, 20, 40), (40, 20, 60)], duration)
    
    def create_call_to_action_effect(self, text: str, duration: float = 3.0) -> VideoClip:
        """Create animated call-to-action"""
        
        # Create main text
        main_text = self.create_text_animation(
            text, 
            font_size=70, 
            color=(255, 255, 255),
            animation_type="bounce",
            duration=duration
        )
        
        # Create background pulse effect
        def pulse_function(t):
            pulse = (math.sin(t * 4) + 1) / 2  # Pulse between 0 and 1
            return (255, int(100 + 155 * pulse), int(100 + 155 * pulse))  # Red to pink
        
        def make_bg_frame(t):
            color = pulse_function(t)
            frame = np.full((self.height, self.width, 3), color, dtype=np.uint8)
            return frame
        
        background = VideoClip(make_bg_frame, duration=duration)
        
        # Add decorative elements
        def make_decoration_frame(t):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Add animated border
            border_width = int(10 + 5 * math.sin(t * 3))
            frame[:border_width, :] = [255, 215, 0]  # Top border
            frame[-border_width:, :] = [255, 215, 0]  # Bottom border
            frame[:, :border_width] = [255, 215, 0]  # Left border
            frame[:, -border_width:] = [255, 215, 0]  # Right border
            
            return frame
        
        decoration = VideoClip(make_decoration_frame, duration=duration)
        decoration = decoration.set_opacity(0.7)
        
        # Composite all elements
        cta_clip = CompositeVideoClip([
            background,
            decoration,
            main_text.set_position('center')
        ], size=(self.width, self.height))
        
        return cta_clip
    
    def create_transition_wipe(self, direction: str = "right", duration: float = 0.5, color: Tuple[int, int, int] = (0, 0, 0)) -> VideoClip:
        """Create wipe transition effect"""
        
        def make_frame(t):
            progress = t / duration
            frame = np.full((self.height, self.width, 3), color, dtype=np.uint8)
            
            if direction == "right":
                wipe_pos = int(progress * self.width)
                frame[:, wipe_pos:] = [0, 0, 0, 0]  # Transparent
            elif direction == "left":
                wipe_pos = int((1 - progress) * self.width)
                frame[:, :wipe_pos] = [0, 0, 0, 0]
            elif direction == "down":
                wipe_pos = int(progress * self.height)
                frame[wipe_pos:, :] = [0, 0, 0, 0]
            elif direction == "up":
                wipe_pos = int((1 - progress) * self.height)
                frame[:wipe_pos, :] = [0, 0, 0, 0]
            
            return frame
        
        return VideoClip(make_frame, duration=duration)

class InstagramReelComposer:
    """Compose complete Instagram Reels with effects"""
    
    def __init__(self):
        self.effects = VideoEffects()
        self.width = 1080
        self.height = 1920
    
    def create_complete_reel(self, product_data: Dict, script_data: Dict, images: List[str]) -> VideoClip:
        """Create a complete Instagram Reel with all effects"""
        
        clips = []
        
        # 1. Hook section (3 seconds)
        hook_clip = self._create_hook_section(script_data.get("hook", ""), 3.0)
        clips.append(hook_clip)
        
        # 2. Product showcase (5 seconds)
        if images:
            showcase_clip = self.effects.create_product_showcase_effect(images[0], 5.0)
        else:
            showcase_clip = self._create_text_section(product_data.get("name", ""), 5.0)
        clips.append(showcase_clip)
        
        # 3. Features highlight (4 seconds)
        features_text = "\n".join(product_data.get("features", [])[:3])  # Top 3 features
        features_clip = self._create_features_section(features_text, 4.0)
        clips.append(features_clip)
        
        # 4. Call to action (3 seconds)
        cta_clip = self.effects.create_call_to_action_effect(script_data.get("cta", "Shop Now!"), 3.0)
        clips.append(cta_clip)
        
        # Add transitions between clips
        final_clips = []
        for i, clip in enumerate(clips):
            final_clips.append(clip)
            
            # Add transition (except after last clip)
            if i < len(clips) - 1:
                transition = self.effects.create_transition_wipe("left", 0.3)
                final_clips.append(transition)
        
        # Concatenate all clips
        final_reel = concatenate_videoclips(final_clips, method="compose")
        
        # Add background music placeholder
        # In a real implementation, you would add actual audio here
        
        return final_reel
    
    def _create_hook_section(self, hook_text: str, duration: float) -> VideoClip:
        """Create engaging hook section"""
        
        # Create gradient background
        bg_colors = [(255, 100, 100), (255, 150, 150), (255, 200, 200)]
        background = self.effects.create_gradient_background(bg_colors, duration)
        
        # Create animated text
        text_clip = self.effects.create_text_animation(
            hook_text,
            font_size=80,
            color=(255, 255, 255),
            animation_type="slide_up",
            duration=duration
        )
        
        # Add particles
        particles = self.effects.create_particle_effect(duration, 40)
        particles = particles.set_opacity(0.4)
        
        # Composite
        hook_clip = CompositeVideoClip([
            background,
            particles,
            text_clip.set_position('center')
        ], size=(self.width, self.height))
        
        return hook_clip
    
    def _create_text_section(self, text: str, duration: float) -> VideoClip:
        """Create text-only section"""
        
        # Create background
        bg_colors = [(20, 20, 40), (40, 40, 80)]
        background = self.effects.create_gradient_background(bg_colors, duration)
        
        # Create text
        text_clip = self.effects.create_text_animation(
            text,
            font_size=60,
            color=(255, 215, 0),
            animation_type="fade_in",
            duration=duration
        )
        
        return CompositeVideoClip([
            background,
            text_clip.set_position('center')
        ], size=(self.width, self.height))
    
    def _create_features_section(self, features_text: str, duration: float) -> VideoClip:
        """Create features highlight section"""
        
        # Create background
        bg_colors = [(40, 20, 60), (80, 40, 120)]
        background = self.effects.create_gradient_background(bg_colors, duration)
        
        # Create text with typewriter effect
        text_clip = self.effects.create_text_animation(
            features_text,
            font_size=50,
            color=(255, 255, 255),
            animation_type="typewriter",
            duration=duration
        )
        
        return CompositeVideoClip([
            background,
            text_clip.set_position('center')
        ], size=(self.width, self.height))

# Usage example
if __name__ == "__main__":
    effects = VideoEffects()
    composer = InstagramReelComposer()
    
    # Example product data
    product_data = {
        "name": "Royal Diamond Crown",
        "features": ["18k Gold Plated", "Genuine Crystals", "Adjustable Size", "Luxury Gift Box"]
    }
    
    script_data = {
        "hook": "✨ Discover Royal Elegance!",
        "cta": "Shop Now - Link in Bio!"
    }
    
    # Create a sample reel
    reel = composer.create_complete_reel(product_data, script_data, [])
    
    # Export (in real usage)
    # reel.write_videofile("sample_reel.mp4", fps=30)

