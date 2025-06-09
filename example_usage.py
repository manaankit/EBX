#!/usr/bin/env python3
"""
Example usage of the Instagram Reel Generator
Demonstrates various ways to use the application
"""

import os
import time
from instagram_reel_generator import InstagramReelGenerator, Product
from advanced_scraper import AdvancedWebScraper
from video_effects import VideoEffects, InstagramReelComposer
from config import Config

def example_basic_generation():
    """Basic example: Generate a single reel"""
    print("🎬 Example 1: Basic Reel Generation")
    print("=" * 40)
    
    # Set up API key (replace with your actual key)
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    if api_key == "your-api-key-here":
        print("⚠️  Please set your OpenAI API key in environment variables")
        print("   export OPENAI_API_KEY='your-actual-api-key'")
        return
    
    try:
        # Initialize generator
        generator = InstagramReelGenerator(api_key)
        
        # Generate a single reel
        print("🔄 Generating reel...")
        result = generator.generate_reel()
        
        # Display results
        print("\n✅ Reel generated successfully!")
        print(f"📹 Video: {result['video_path']}")
        print(f"🏷️  Product: {result['product_name']}")
        print(f"💰 Price: {result['product_price']}")
        print(f"🎵 Music: {result['music_suggestion']}")
        
        print("\n📱 Instagram Caption:")
        print("-" * 30)
        print(result['caption'])
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_batch_generation():
    """Example: Generate multiple reels"""
    print("\n🎬 Example 2: Batch Reel Generation")
    print("=" * 40)
    
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    if api_key == "your-api-key-here":
        print("⚠️  Please set your OpenAI API key")
        return
    
    try:
        generator = InstagramReelGenerator(api_key)
        
        # Generate 3 reels
        print("🔄 Generating 3 reels...")
        results = generator.batch_generate(count=3)
        
        print(f"\n✅ Generated {len(results)} reels!")
        
        for i, result in enumerate(results, 1):
            print(f"\n📹 Reel {i}:")
            print(f"   Product: {result['product_name']}")
            print(f"   Video: {result['video_path']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_custom_product():
    """Example: Generate reel for custom product"""
    print("\n🎬 Example 3: Custom Product Reel")
    print("=" * 40)
    
    # Create custom product
    custom_product = Product(
        name="Emerald Queen Crown",
        price="$449.99",
        description="Stunning emerald crown with gold accents, perfect for royal occasions.",
        image_urls=["https://example.com/emerald-crown.jpg"],
        category="crowns",
        url="https://crowncarnival.shop/emerald-queen-crown",
        features=[
            "Genuine Emerald Stones",
            "24k Gold Plating", 
            "Handcrafted Design",
            "Royal Collection",
            "Certificate of Authenticity"
        ]
    )
    
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    if api_key == "your-api-key-here":
        print("⚠️  Please set your OpenAI API key")
        return
    
    try:
        generator = InstagramReelGenerator(api_key)
        
        print("🔄 Generating reel for custom product...")
        
        # Generate script for custom product
        script = generator.ai_generator.generate_reel_script(custom_product)
        
        # Create video
        video_path = generator.video_generator.create_video_reel(custom_product, script)
        
        print("✅ Custom product reel generated!")
        print(f"📹 Video: {video_path}")
        print(f"🏷️  Product: {custom_product.name}")
        print(f"💰 Price: {custom_product.price}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_advanced_scraping():
    """Example: Advanced web scraping"""
    print("\n🎬 Example 4: Advanced Web Scraping")
    print("=" * 40)
    
    try:
        # Initialize advanced scraper
        scraper = AdvancedWebScraper(headless=True)
        
        print("🔄 Scraping Crown Carnival products...")
        products = scraper.scrape_crown_carnival()
        
        print(f"✅ Found {len(products)} products!")
        
        for i, product in enumerate(products[:3], 1):  # Show first 3
            print(f"\n📦 Product {i}:")
            print(f"   Name: {product.name}")
            print(f"   Price: {product.price}")
            print(f"   Category: {product.category}")
            print(f"   Features: {len(product.features)} features")
            print(f"   Images: {len(product.images)} images")
            print(f"   Rating: {product.rating or 'N/A'}")
            
        scraper.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_video_effects():
    """Example: Custom video effects"""
    print("\n🎬 Example 5: Custom Video Effects")
    print("=" * 40)
    
    try:
        # Initialize video effects
        effects = VideoEffects()
        composer = InstagramReelComposer()
        
        print("🔄 Creating video with custom effects...")
        
        # Sample product data
        product_data = {
            "name": "Diamond Princess Tiara",
            "price": "$599.99",
            "features": [
                "Real Diamonds",
                "Platinum Setting",
                "Royal Design",
                "Lifetime Warranty"
            ]
        }
        
        script_data = {
            "hook": "✨ Royal Elegance Awaits!",
            "showcase": "Discover the Diamond Princess Tiara",
            "features": "Premium materials and craftsmanship",
            "cta": "Shop Now - Limited Edition!"
        }
        
        # Create effects
        print("   Creating gradient background...")
        bg_colors = [(20, 20, 40), (60, 40, 80), (100, 60, 120)]
        background = effects.create_gradient_background(bg_colors, 5.0)
        
        print("   Creating text animations...")
        text_clip = effects.create_text_animation(
            "Diamond Princess Tiara\n$599.99",
            font_size=70,
            color=(255, 215, 0),
            animation_type="bounce",
            duration=5.0
        )
        
        print("   Creating particle effects...")
        particles = effects.create_particle_effect(5.0, particle_count=60)
        
        print("✅ Video effects created successfully!")
        print("   (In a real scenario, these would be combined into a video file)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_configuration():
    """Example: Configuration management"""
    print("\n🎬 Example 6: Configuration Management")
    print("=" * 40)
    
    print("⚙️  Current Configuration:")
    print(f"   Video Size: {Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}")
    print(f"   Video FPS: {Config.VIDEO_FPS}")
    print(f"   Duration: {Config.VIDEO_DURATION}s")
    print(f"   AI Model: {Config.AI_MODEL}")
    print(f"   Max Tokens: {Config.MAX_TOKENS}")
    print(f"   Output Dir: {Config.OUTPUT_DIR}")
    
    print("\n🎨 Available Templates:")
    for template, settings in Config.VIDEO_TEMPLATES.items():
        print(f"   {template.title()}:")
        print(f"     Background: RGB{settings['background_color']}")
        print(f"     Text Color: RGB{settings['text_color']}")
        print(f"     Font Size: {settings['font_size']}px")
    
    print("\n🎵 Music Suggestions by Category:")
    for category, suggestions in Config.MUSIC_SUGGESTIONS.items():
        print(f"   {category.title()}: {', '.join(suggestions)}")

def example_error_handling():
    """Example: Error handling and fallbacks"""
    print("\n🎬 Example 7: Error Handling")
    print("=" * 40)
    
    try:
        # Test with invalid API key
        print("🔄 Testing with invalid API key...")
        generator = InstagramReelGenerator("invalid-api-key")
        
        # This should use fallback content
        result = generator.generate_reel()
        
        print("✅ Fallback content generated successfully!")
        print(f"   Product: {result['product_name']}")
        
    except Exception as e:
        print(f"✅ Error handled gracefully: {e}")
    
    print("\n🔄 Testing configuration validation...")
    from config import validate_config
    
    errors = validate_config()
    if errors:
        print("⚠️  Configuration issues found:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Configuration is valid!")

def main():
    """Run all examples"""
    print("🚀 Instagram Reel Generator - Example Usage")
    print("=" * 50)
    
    examples = [
        example_basic_generation,
        example_batch_generation,
        example_custom_product,
        example_advanced_scraping,
        example_video_effects,
        example_configuration,
        example_error_handling
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
            if i < len(examples):
                print("\n" + "⏳ " + "."*20)
                time.sleep(1)  # Brief pause between examples
        except Exception as e:
            print(f"❌ Example {i} failed: {e}")
            continue
    
    print("\n🎉 All examples completed!")
    print("\n💡 Next Steps:")
    print("   1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("   2. Run: python instagram_reel_generator.py")
    print("   3. Or use CLI: python cli.py generate --count 5")
    print("   4. Check generated_reels/ directory for output")

if __name__ == "__main__":
    main()

