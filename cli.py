#!/usr/bin/env python3
"""
Command Line Interface for Instagram Reel Generator
Provides easy-to-use commands for generating Instagram Reels
"""

import argparse
import sys
import os
import json
from typing import Optional
from instagram_reel_generator import InstagramReelGenerator
from config import Config, validate_config

def setup_args():
    """Setup command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate AI-powered Instagram Reels for Crown Carnival products",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate                    # Generate a single reel
  %(prog)s generate --count 5          # Generate 5 reels
  %(prog)s generate --output ./reels   # Custom output directory
  %(prog)s batch --count 10            # Batch generate 10 reels
  %(prog)s config --check              # Check configuration
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate Instagram Reels')
    generate_parser.add_argument(
        '--count', '-c', 
        type=int, 
        default=1, 
        help='Number of reels to generate (default: 1)'
    )
    generate_parser.add_argument(
        '--output', '-o', 
        type=str, 
        help='Output directory (default: generated_reels)'
    )
    generate_parser.add_argument(
        '--api-key', 
        type=str, 
        help='OpenAI API key (overrides environment variable)'
    )
    generate_parser.add_argument(
        '--template', 
        choices=['luxury', 'elegant', 'modern'], 
        default='luxury',
        help='Video template style (default: luxury)'
    )
    generate_parser.add_argument(
        '--duration', 
        type=int, 
        default=15,
        help='Video duration in seconds (default: 15)'
    )
    generate_parser.add_argument(
        '--quality', 
        choices=['low', 'medium', 'high'], 
        default='high',
        help='Video quality (default: high)'
    )
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch generate multiple reels')
    batch_parser.add_argument(
        '--count', '-c', 
        type=int, 
        required=True,
        help='Number of reels to generate'
    )
    batch_parser.add_argument(
        '--output', '-o', 
        type=str, 
        help='Output directory (default: generated_reels)'
    )
    batch_parser.add_argument(
        '--parallel', '-p', 
        action='store_true',
        help='Enable parallel processing'
    )
    batch_parser.add_argument(
        '--delay', 
        type=int, 
        default=2,
        help='Delay between generations in seconds (default: 2)'
    )
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument(
        '--check', 
        action='store_true',
        help='Check configuration validity'
    )
    config_parser.add_argument(
        '--show', 
        action='store_true',
        help='Show current configuration'
    )
    config_parser.add_argument(
        '--setup', 
        action='store_true',
        help='Interactive configuration setup'
    )
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    info_parser.add_argument(
        '--dependencies', 
        action='store_true',
        help='Check dependencies'
    )
    info_parser.add_argument(
        '--version', 
        action='store_true',
        help='Show version information'
    )
    
    return parser

def check_dependencies():
    """Check if all required dependencies are available"""
    dependencies = {
        'requests': 'Web scraping',
        'beautifulsoup4': 'HTML parsing',
        'openai': 'AI content generation',
        'moviepy': 'Video processing',
        'PIL': 'Image processing',
        'numpy': 'Numerical operations',
        'selenium': 'Advanced web scraping'
    }
    
    missing = []
    available = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep.replace('-', '_'))
            available.append(f"✅ {dep} - {description}")
        except ImportError:
            missing.append(f"❌ {dep} - {description}")
    
    print("📦 Dependency Check:")
    print("=" * 50)
    
    if available:
        print("\n🟢 Available:")
        for dep in available:
            print(f"  {dep}")
    
    if missing:
        print("\n🔴 Missing:")
        for dep in missing:
            print(f"  {dep}")
        print(f"\n💡 Install missing dependencies with:")
        print(f"   pip install {' '.join([dep.split(' -')[0] for dep in missing])}")
        return False
    
    print("\n✅ All dependencies are available!")
    return True

def interactive_setup():
    """Interactive configuration setup"""
    print("🔧 Instagram Reel Generator Setup")
    print("=" * 40)
    
    # OpenAI API Key
    api_key = input("\n🤖 Enter your OpenAI API key: ").strip()
    if not api_key:
        print("❌ OpenAI API key is required!")
        return False
    
    # Output directory
    output_dir = input(f"\n📁 Output directory (default: {Config.OUTPUT_DIR}): ").strip()
    if not output_dir:
        output_dir = Config.OUTPUT_DIR
    
    # Video quality
    quality = input("\n🎬 Video quality [low/medium/high] (default: high): ").strip().lower()
    if quality not in ['low', 'medium', 'high']:
        quality = 'high'
    
    # Create .env file
    env_content = f"""# Instagram Reel Generator Configuration
OPENAI_API_KEY={api_key}
OUTPUT_DIR={output_dir}
VIDEO_QUALITY={quality}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ Configuration saved to .env file!")
        print("🚀 You're ready to generate Instagram Reels!")
        return True
    except Exception as e:
        print(f"\n❌ Error saving configuration: {e}")
        return False

def show_config():
    """Show current configuration"""
    print("⚙️  Current Configuration:")
    print("=" * 30)
    
    config_items = [
        ("OpenAI API Key", "✅ Set" if Config.OPENAI_API_KEY else "❌ Not set"),
        ("Crown Carnival URL", Config.CROWN_CARNIVAL_URL),
        ("Video Dimensions", f"{Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}"),
        ("Video FPS", Config.VIDEO_FPS),
        ("Video Duration", f"{Config.VIDEO_DURATION}s"),
        ("Output Directory", Config.OUTPUT_DIR),
        ("AI Model", Config.AI_MODEL),
        ("Max Tokens", Config.MAX_TOKENS),
        ("Temperature", Config.TEMPERATURE),
    ]
    
    for key, value in config_items:
        print(f"  {key}: {value}")

def generate_reels(args):
    """Generate Instagram Reels"""
    print("🎬 Instagram Reel Generator")
    print("=" * 30)
    
    # Validate configuration
    errors = validate_config()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # Override API key if provided
    api_key = args.api_key or Config.OPENAI_API_KEY
    if not api_key:
        print("❌ OpenAI API key is required!")
        print("   Set OPENAI_API_KEY environment variable or use --api-key")
        return False
    
    # Override output directory if provided
    if args.output:
        Config.OUTPUT_DIR = args.output
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    try:
        # Initialize generator
        generator = InstagramReelGenerator(api_key)
        
        print(f"🎯 Generating {args.count} reel(s)...")
        print(f"📁 Output directory: {Config.OUTPUT_DIR}")
        print(f"🎨 Template: {args.template}")
        print(f"⏱️  Duration: {args.duration}s")
        print(f"🎥 Quality: {args.quality}")
        
        results = []
        
        for i in range(args.count):
            print(f"\n🔄 Generating reel {i+1}/{args.count}...")
            
            try:
                result = generator.generate_reel()
                results.append(result)
                
                print(f"✅ Reel {i+1} completed!")
                print(f"   📹 Video: {result['video_path']}")
                print(f"   🏷️  Product: {result['product_name']}")
                print(f"   💰 Price: {result['product_price']}")
                
            except Exception as e:
                print(f"❌ Error generating reel {i+1}: {e}")
                continue
        
        # Summary
        print(f"\n🎉 Generation Complete!")
        print(f"   ✅ Successfully generated: {len(results)} reels")
        print(f"   ❌ Failed: {args.count - len(results)} reels")
        
        if results:
            print(f"\n📊 Results saved in: {Config.OUTPUT_DIR}")
            
            # Save summary
            summary_file = os.path.join(Config.OUTPUT_DIR, "generation_summary.json")
            with open(summary_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Summary saved to: {summary_file}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return False

def main():
    """Main CLI function"""
    parser = setup_args()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle commands
    if args.command == 'generate' or args.command == 'batch':
        success = generate_reels(args)
        return 0 if success else 1
        
    elif args.command == 'config':
        if args.check:
            errors = validate_config()
            if errors:
                print("❌ Configuration errors:")
                for error in errors:
                    print(f"  - {error}")
                return 1
            else:
                print("✅ Configuration is valid!")
                return 0
                
        elif args.show:
            show_config()
            return 0
            
        elif args.setup:
            success = interactive_setup()
            return 0 if success else 1
            
        else:
            print("Use --check, --show, or --setup with config command")
            return 1
    
    elif args.command == 'info':
        if args.dependencies:
            success = check_dependencies()
            return 0 if success else 1
            
        elif args.version:
            print("Instagram Reel Generator v1.0.0")
            print("Built for Crown Carnival product promotion")
            return 0
            
        else:
            check_dependencies()
            print()
            show_config()
            return 0
    
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

