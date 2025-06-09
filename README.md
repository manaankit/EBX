# Instagram Reel Generator for Crown Carnival

An AI-powered application that automatically generates Instagram Reels for Crown Carnival jewelry products. The app scrapes product information, generates engaging content using AI, and creates professional video content optimized for Instagram.

## 🌟 Features

- **Automated Product Selection**: Randomly selects products from Crown Carnival's catalog
- **AI-Powered Content Generation**: Creates engaging scripts and captions using OpenAI GPT
- **Professional Video Creation**: Generates high-quality videos with effects and animations
- **Instagram Optimization**: Creates content in the perfect 9:16 aspect ratio for Instagram Reels
- **Advanced Visual Effects**: Includes transitions, animations, particle effects, and more
- **Batch Processing**: Generate multiple reels at once
- **Customizable Templates**: Multiple video styles and themes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- FFmpeg (for video processing)
- Chrome browser (for web scraping)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd instagram-reel-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

4. Run the application:
```bash
python instagram_reel_generator.py
```

## 📁 Project Structure

```
instagram-reel-generator/
├── instagram_reel_generator.py  # Main application
├── advanced_scraper.py          # Web scraping functionality
├── video_effects.py             # Video effects and animations
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── generated_reels/             # Output directory (created automatically)
```

## 🎬 How It Works

1. **Product Selection**: The app randomly selects a product from Crown Carnival's catalog
2. **Content Generation**: AI generates an engaging script with hook, showcase, features, and call-to-action
3. **Video Creation**: Creates a professional video with:
   - Eye-catching hook (3 seconds)
   - Product showcase with effects (5 seconds)
   - Features highlight (4 seconds)
   - Call-to-action with animations (3 seconds)
4. **Output**: Generates MP4 video file and Instagram-ready caption

## 🛠️ Configuration

Edit `config.py` to customize:

- Video dimensions and quality
- AI model settings
- Visual themes and colors
- Hashtag preferences
- Music suggestions

## 📱 Instagram Reel Specifications

The generated videos are optimized for Instagram Reels:

- **Aspect Ratio**: 9:16 (1080x1920)
- **Duration**: 15 seconds
- **Frame Rate**: 30 FPS
- **Format**: MP4
- **Audio**: Ready for background music overlay

## 🎨 Video Effects

The app includes various professional effects:

- **Zoom and Pan**: Dynamic camera movements
- **Transitions**: Smooth slide and wipe transitions
- **Text Animations**: Fade, slide, typewriter, and bounce effects
- **Particle Effects**: Sparkles and animated elements
- **Gradient Backgrounds**: Animated color gradients
- **Product Showcase**: Professional product presentation

## 🤖 AI Features

- **Script Generation**: Creates engaging, trend-aware content
- **Hashtag Optimization**: Generates relevant hashtags for maximum reach
- **Music Suggestions**: Recommends appropriate background music
- **Caption Creation**: Writes complete Instagram captions

## 📊 Sample Output

Each generation creates:

- **Video File**: High-quality MP4 ready for Instagram
- **Caption**: Complete Instagram post caption with hashtags
- **Metadata**: Product information and generation details
- **JSON Data**: Structured data for further processing

## 🔧 Advanced Usage

### Batch Generation

Generate multiple reels at once:

```python
from instagram_reel_generator import InstagramReelGenerator

generator = InstagramReelGenerator("your-openai-api-key")
results = generator.batch_generate(count=5)
```

### Custom Product Data

Use your own product data:

```python
from instagram_reel_generator import Product, InstagramReelGenerator

custom_product = Product(
    name="Custom Crown",
    price="$299.99",
    description="Beautiful custom crown",
    image_urls=["image1.jpg"],
    category="crowns",
    url="https://example.com",
    features=["Feature 1", "Feature 2"]
)

generator = InstagramReelGenerator("your-openai-api-key")
result = generator.generate_reel_for_product(custom_product)
```

### Custom Video Effects

Create custom effects:

```python
from video_effects import VideoEffects

effects = VideoEffects()
custom_clip = effects.create_zoom_effect(your_clip, zoom_factor=1.5)
```

## 🎯 Best Practices

1. **Content Quality**: Ensure product images are high-resolution
2. **Brand Consistency**: Customize colors and fonts to match brand
3. **Trending Elements**: Update hashtags and music suggestions regularly
4. **A/B Testing**: Generate multiple versions to test performance
5. **Scheduling**: Use Instagram's scheduling tools for optimal posting times

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Errors**: Verify your API key and quota
2. **Video Export Issues**: Ensure FFmpeg is properly installed
3. **Scraping Problems**: Check internet connection and website availability
4. **Memory Issues**: Reduce video quality or batch size for large operations

### Error Handling

The app includes comprehensive error handling:
- Fallback content when scraping fails
- Default templates when AI generation fails
- Graceful degradation for missing dependencies

## 🚀 Deployment

### Local Development
```bash
python instagram_reel_generator.py
```

### Production Deployment
- Use environment variables for API keys
- Set up proper logging
- Configure output directory permissions
- Consider using Docker for consistent environments

## 📈 Performance Optimization

- **Caching**: Product data is cached to reduce API calls
- **Parallel Processing**: Batch operations use multiprocessing
- **Memory Management**: Large video files are processed in chunks
- **Quality Settings**: Adjustable quality settings for different use cases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- MoviePy for video processing
- Beautiful Soup for web scraping
- Pillow for image processing
- Crown Carnival for inspiration

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the configuration options

---

**Note**: This application is designed for educational and demonstration purposes. Always respect website terms of service and rate limits when scraping content. Ensure you have proper rights to use any images or content in your generated videos.

