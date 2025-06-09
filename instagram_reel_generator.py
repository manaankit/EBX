#!/usr/bin/env python3
"""
Instagram Reel Generator for Crown Carnival Products
Generates AI-powered video content and images for Instagram Reels
using randomly selected products from Crown Carnival shop.
"""

import requests
import random
import json
import os
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
import openai
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

@dataclass
class Product:
    """Product data structure"""
    name: str
    price: str
    description: str
    image_urls: List[str]
    category: str
    url: str
    features: List[str]

class CrownCarnivalScraper:
    """Scraper for Crown Carnival products"""
    
    def __init__(self):
        self.base_url = "https://crowncarnival.shop"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_product_categories(self) -> List[str]:
        """Get available product categories"""
        categories = [
            "crowns", "tiaras", "headpieces", "necklaces", 
            "bracelets", "rings", "accessories", "jewelry"
        ]
        return categories
    
    def scrape_products(self, limit: int = 50) -> List[Product]:
        """Scrape products from Crown Carnival"""
        products = []
        
        # Sample product data based on the crown/jewelry theme
        sample_products = [
            {
                "name": "Royal Diamond Crown",
                "price": "$299.99",
                "description": "Exquisite royal crown featuring brilliant diamonds and gold plating. Perfect for special occasions and photoshoots.",
                "image_urls": ["https://example.com/crown1.jpg"],
                "category": "crowns",
                "features": ["18k Gold Plated", "Genuine Crystals", "Adjustable Size", "Luxury Gift Box"]
            },
            {
                "name": "Vintage Pearl Tiara",
                "price": "$189.99", 
                "description": "Elegant vintage-style tiara with lustrous pearls and silver detailing. Timeless beauty for weddings and formal events.",
                "image_urls": ["https://example.com/tiara1.jpg"],
                "category": "tiaras",
                "features": ["Sterling Silver", "Freshwater Pearls", "Vintage Design", "Bridal Collection"]
            },
            {
                "name": "Crystal Star Headpiece",
                "price": "$149.99",
                "description": "Stunning star-shaped headpiece with sparkling crystals. Perfect for festivals, parties, and Instagram photos.",
                "image_urls": ["https://example.com/headpiece1.jpg"],
                "category": "headpieces",
                "features": ["Swarovski Crystals", "Flexible Band", "Star Design", "Festival Ready"]
            },
            {
                "name": "Golden Empress Necklace",
                "price": "$229.99",
                "description": "Majestic golden necklace fit for an empress. Bold statement piece with intricate detailing.",
                "image_urls": ["https://example.com/necklace1.jpg"],
                "category": "necklaces",
                "features": ["24k Gold Plated", "Statement Piece", "Adjustable Chain", "Royal Design"]
            },
            {
                "name": "Sapphire Crown Bracelet",
                "price": "$179.99",
                "description": "Luxurious bracelet featuring sapphire-colored stones in a crown pattern. Elegant and eye-catching.",
                "image_urls": ["https://example.com/bracelet1.jpg"],
                "category": "bracelets",
                "features": ["Sapphire Stones", "Crown Pattern", "Adjustable Fit", "Gift Ready"]
            }
        ]
        
        for product_data in sample_products[:limit]:
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                description=product_data["description"],
                image_urls=product_data["image_urls"],
                category=product_data["category"],
                url=f"{self.base_url}/products/{product_data['name'].lower().replace(' ', '-')}",
                features=product_data["features"]
            )
            products.append(product)
            
        return products
    
    def get_random_product(self) -> Optional[Product]:
        """Get a random product from the catalog"""
        products = self.scrape_products()
        return random.choice(products) if products else None

class AIContentGenerator:
    """AI-powered content generator for Instagram Reels"""
    
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        
    def generate_reel_script(self, product: Product) -> Dict[str, str]:
        """Generate Instagram Reel script for a product"""
        prompt = f"""
        Create an engaging Instagram Reel script for this luxury jewelry product:
        
        Product: {product.name}
        Price: {product.price}
        Description: {product.description}
        Features: {', '.join(product.features)}
        Category: {product.category}
        
        Generate a script with:
        1. Hook (first 3 seconds)
        2. Product showcase (5-7 seconds)
        3. Features highlight (3-5 seconds)
        4. Call to action (2-3 seconds)
        
        Make it trendy, engaging, and suitable for luxury jewelry audience.
        Include trending hashtags and music suggestions.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            script_content = response.choices[0].message.content
            
            # Parse the response into structured format
            return {
                "hook": self._extract_section(script_content, "Hook"),
                "showcase": self._extract_section(script_content, "Product showcase"),
                "features": self._extract_section(script_content, "Features"),
                "cta": self._extract_section(script_content, "Call to action"),
                "hashtags": self._extract_hashtags(script_content),
                "music_suggestion": self._extract_music(script_content)
            }
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._get_fallback_script(product)
    
    def _extract_section(self, content: str, section: str) -> str:
        """Extract specific section from generated content"""
        pattern = rf"{section}[:\-\s]*([^\n]+(?:\n(?!\d\.)[^\n]+)*)"
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else f"Discover the amazing {section.lower()}"
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        hashtags = re.findall(r'#\w+', content)
        if not hashtags:
            hashtags = ["#luxury", "#jewelry", "#crown", "#fashion", "#style", "#elegant"]
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _extract_music(self, content: str) -> str:
        """Extract music suggestion from content"""
        music_pattern = r"music[:\-\s]*([^\n]+)"
        match = re.search(music_pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else "Trending luxury/fashion music"
    
    def _get_fallback_script(self, product: Product) -> Dict[str, str]:
        """Fallback script when AI generation fails"""
        return {
            "hook": f"✨ Introducing the stunning {product.name}!",
            "showcase": f"Look at this gorgeous {product.category} - {product.description}",
            "features": f"Features: {', '.join(product.features)}",
            "cta": f"Get yours now for {product.price}! Link in bio 👆",
            "hashtags": ["#luxury", "#jewelry", "#crown", "#fashion", "#style"],
            "music_suggestion": "Elegant classical or trending fashion music"
        }

class VideoGenerator:
    """Generate video content for Instagram Reels"""
    
    def __init__(self):
        self.output_dir = "generated_reels"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_product_images(self, product: Product, script: Dict[str, str]) -> List[str]:
        """Create product showcase images"""
        images = []
        
        # Create text overlay images for different sections
        sections = [
            ("hook", script["hook"], (255, 215, 0)),  # Gold
            ("showcase", f"{product.name}\n{product.price}", (255, 255, 255)),  # White
            ("features", "\n".join(product.features), (200, 200, 255)),  # Light blue
            ("cta", script["cta"], (255, 100, 100))  # Light red
        ]
        
        for section_name, text, color in sections:
            img_path = self._create_text_image(text, color, section_name)
            images.append(img_path)
            
        return images
    
    def _create_text_image(self, text: str, color: Tuple[int, int, int], filename: str) -> str:
        """Create an image with text overlay"""
        # Create a 1080x1920 image (Instagram Reel dimensions)
        img = Image.new('RGB', (1080, 1920), color=(20, 20, 40))  # Dark background
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 60)
            title_font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
        
        # Add gradient background effect
        for y in range(1920):
            gradient_color = (
                int(20 + (y / 1920) * 30),
                int(20 + (y / 1920) * 30),
                int(40 + (y / 1920) * 60)
            )
            draw.line([(0, y), (1080, y)], fill=gradient_color)
        
        # Add decorative elements
        self._add_decorative_elements(draw, img.size)
        
        # Add text with word wrapping
        lines = self._wrap_text(text, font, 900)  # Max width 900px
        total_height = len(lines) * 80
        start_y = (1920 - total_height) // 2
        
        for i, line in enumerate(lines):
            # Get text size for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1080 - text_width) // 2
            y = start_y + i * 80
            
            # Add text shadow
            draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
            # Add main text
            draw.text((x, y), line, font=font, fill=color)
        
        # Save image
        img_path = os.path.join(self.output_dir, f"{filename}_{int(time.time())}.png")
        img.save(img_path)
        return img_path
    
    def _add_decorative_elements(self, draw: ImageDraw.Draw, size: Tuple[int, int]):
        """Add decorative elements to the image"""
        width, height = size
        
        # Add some sparkle effects
        for _ in range(20):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            star_size = random.randint(10, 30)
            
            # Draw a simple star shape
            points = []
            for i in range(10):
                angle = i * 36 * 3.14159 / 180
                if i % 2 == 0:
                    radius = star_size
                else:
                    radius = star_size // 2
                px = x + radius * np.cos(angle)
                py = y + radius * np.sin(angle)
                points.append((px, py))
            
            draw.polygon(points, fill=(255, 215, 0, 100))  # Gold sparkles
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Word is too long, add anyway
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def create_video_reel(self, product: Product, script: Dict[str, str]) -> str:
        """Create a complete video reel"""
        # Create images for each section
        images = self.create_product_images(product, script)
        
        # Create video clips from images
        clips = []
        durations = [3, 5, 4, 3]  # Duration for each section
        
        for i, (img_path, duration) in enumerate(zip(images, durations)):
            # Create clip from image
            clip = ImageClip(img_path, duration=duration)
            
            # Add zoom effect
            clip = clip.resize(lambda t: 1 + 0.1 * t / duration)
            
            # Add fade transitions
            if i > 0:
                clip = clip.fadein(0.5)
            if i < len(images) - 1:
                clip = clip.fadeout(0.5)
                
            clips.append(clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add background music placeholder (you would add actual audio here)
        # audio = AudioFileClip("background_music.mp3").subclip(0, final_video.duration)
        # final_video = final_video.set_audio(audio)
        
        # Export video
        output_path = os.path.join(self.output_dir, f"reel_{product.name.replace(' ', '_')}_{int(time.time())}.mp4")
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac' if final_video.audio else None
        )
        
        # Clean up
        final_video.close()
        for clip in clips:
            clip.close()
        
        return output_path

class InstagramReelGenerator:
    """Main class for generating Instagram Reels"""
    
    def __init__(self, openai_api_key: str):
        self.scraper = CrownCarnivalScraper()
        self.ai_generator = AIContentGenerator(openai_api_key)
        self.video_generator = VideoGenerator()
        
    def generate_reel(self) -> Dict[str, str]:
        """Generate a complete Instagram Reel"""
        print("🔍 Selecting random product from Crown Carnival...")
        product = self.scraper.get_random_product()
        
        if not product:
            raise Exception("No products found!")
        
        print(f"✨ Selected product: {product.name}")
        print(f"💰 Price: {product.price}")
        print(f"📝 Description: {product.description}")
        
        print("\n🤖 Generating AI script...")
        script = self.ai_generator.generate_reel_script(product)
        
        print("\n🎬 Creating video reel...")
        video_path = self.video_generator.create_video_reel(product, script)
        
        # Generate caption for Instagram
        caption = self._generate_instagram_caption(product, script)
        
        result = {
            "product_name": product.name,
            "product_price": product.price,
            "product_url": product.url,
            "video_path": video_path,
            "caption": caption,
            "hashtags": " ".join(script["hashtags"]),
            "music_suggestion": script["music_suggestion"]
        }
        
        print(f"\n✅ Reel generated successfully!")
        print(f"📹 Video saved to: {video_path}")
        print(f"📱 Ready for Instagram upload!")
        
        return result
    
    def _generate_instagram_caption(self, product: Product, script: Dict[str, str]) -> str:
        """Generate Instagram caption"""
        caption = f"""✨ {script['hook']}

{script['showcase']}

🔥 Key Features:
{chr(10).join([f"• {feature}" for feature in product.features])}

{script['cta']}

{' '.join(script['hashtags'])}

#CrownCarnival #LuxuryJewelry #InstagramReel #Fashion #Style"""
        
        return caption
    
    def batch_generate(self, count: int = 5) -> List[Dict[str, str]]:
        """Generate multiple reels"""
        results = []
        for i in range(count):
            print(f"\n{'='*50}")
            print(f"Generating Reel {i+1}/{count}")
            print(f"{'='*50}")
            
            try:
                result = self.generate_reel()
                results.append(result)
                time.sleep(2)  # Brief pause between generations
            except Exception as e:
                print(f"Error generating reel {i+1}: {e}")
                continue
                
        return results

def main():
    """Main function to run the Instagram Reel Generator"""
    print("🎬 Crown Carnival Instagram Reel Generator")
    print("=" * 50)
    
    # Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    
    if OPENAI_API_KEY == "your-openai-api-key-here":
        print("⚠️  Warning: Using placeholder OpenAI API key")
        print("   Set OPENAI_API_KEY environment variable for AI features")
    
    try:
        # Initialize generator
        generator = InstagramReelGenerator(OPENAI_API_KEY)
        
        # Generate a single reel
        result = generator.generate_reel()
        
        # Print results
        print("\n" + "="*50)
        print("📊 GENERATION RESULTS")
        print("="*50)
        print(f"Product: {result['product_name']}")
        print(f"Price: {result['product_price']}")
        print(f"Video: {result['video_path']}")
        print(f"Music: {result['music_suggestion']}")
        print("\n📱 Instagram Caption:")
        print("-" * 30)
        print(result['caption'])
        
        # Save results to JSON
        results_file = os.path.join("generated_reels", f"reel_data_{int(time.time())}.json")
        with open(results_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

