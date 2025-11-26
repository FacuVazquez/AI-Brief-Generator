# AI Brief Generator

A minimal, production-minded AI feature that generates campaign briefs for influencer marketing. Built with Django, OpenAI, and clean frontend using HTML/CSS/jQuery.

## 📹 Demo

**Loom Video**: [Add your Loom link here - under 1 minute demo]

## 📋 Quick Reference

This README includes detailed notes on:
1. **Prompt Design Choices** → See [Implementation Details](#-implementation-details)
2. **Guardrails Implemented** → See [Guardrails](#guardrails-implemented)
3. **Token & Latency Measurement** → See [Metrics](#token-and-latency-measurement)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (optional - stub mode works without it)
export OPENAI_API_KEY="your-key-here"

# Run migrations
python3 manage.py migrate

# Start server
python3 manage.py runserver
```

Visit **http://localhost:8000** in your browser.

> **Note:** The app works without an OpenAI API key using intelligent stub responses for development/testing.

## 📁 Project Structure

```
ai_brief/
  ├── manage.py
  ├── requirements.txt
  ├── ai_brief/                 # Django project settings
  │   ├── settings.py
  │   └── urls.py
  ├── generator/                # Main app
  │   ├── views.py              # API endpoint
  │   ├── urls.py
  │   ├── services/
  │   │   └── llm.py            # OpenAI integration
  │   └── utils/
  │       ├── validation.py     # Input validation
  │       └── profanity.py      # Profanity filter
  └── static/                   # Frontend
      ├── index.html
      ├── styles.css
      └── app.js
```

## 🎯 Features

### Inputs
- **Brand Name** (text input)
- **Target Platform** (Instagram, TikTok, or UGC)
- **Campaign Goal** (Awareness, Conversions, or Content Assets)
- **Tone** (Professional, Friendly, or Playful)

### Outputs
- **Brief**: 4-6 sentence campaign description
- **Content Angles**: 3 specific content suggestions
- **Creator Criteria**: 3 creator selection criteria
- **Metrics**: Latency (ms) and token usage

## 🛡️ Implementation Details

### Prompt Design Choices

1. **System Prompt**: Concise, role-focused prompt defining the AI as a Collabstr campaign brief generator that always returns exactly 3 angles and 3 criteria
2. **User Prompt**: Minimal template using only the 4 input parameters (brand_name, platform, goal, tone)
3. **Model**: GPT-4o-mini for optimal balance of speed, cost, and quality
4. **Temperature**: Set to 0.3 for consistent, deterministic outputs while maintaining creativity
5. **Structured Output**: Uses OpenAI's tools/function calling (not regular chat) to guarantee valid JSON with required fields
6. **Token Limit**: Max 800 tokens to ensure complete responses without truncation

### Guardrails Implemented

1. **Server-Side Validation**:
   - Required field checks
   - Length validation (2-100 chars for brand name)
   - Allowlist validation for platform, goal, and tone

2. **Advanced Profanity Filter**:
   - Unicode normalization to catch fancy characters (𝒇𝒖𝒄𝒌 → fuck)
   - Punctuation removal to detect obfuscation (f.u.c.k → fuck)
   - Repeated letter reduction (fuuuuck → fuck)
   - L33t speak detection (sh1t → shit)
   - Safe word allowlist to prevent false positives (class, assistant, etc.)
   - Expanded profanity list with common variations

3. **Rate Limiting**:
   - Architected for easy addition of Django rate limiting
   - Single endpoint design for straightforward throttling

4. **Error Handling**:
   - Graceful degradation when API unavailable
   - Specific error messages for different failure modes
   - Logging for debugging and monitoring

5. **Security**:
   - CSRF exemption only on API endpoint (not entire app)
   - Input sanitization and validation
   - No user data persistence (stateless)

### Token and Latency Measurement

1. **Latency**: Measured using Python's `time.time()` before and after API call
   - Captures end-to-end LLM request time
   - Returned in milliseconds for precision

2. **Token Tracking**:
   - Input tokens: `response.usage.prompt_tokens`
   - Output tokens: `response.usage.completion_tokens`
   - Both values returned in API response for cost visibility

3. **Stub Mode**: When no API key is configured:
   - Simulates 500ms latency
   - Returns 0 for token counts
   - Generates contextual placeholder content

## 🎨 Frontend Design

- **Clean, minimal aesthetic** inspired by Collabstr
- **Gradient title** with Collabstr brand colors
- **Black button** with white text for strong CTA
- **Sans-serif typography** for modern look
- **Generous whitespace** and rounded corners
- **Smooth transitions** and loading states
- **Responsive design** for mobile and desktop
- **jQuery AJAX** for seamless form submission

## 🔧 Development

### Running Tests
```bash
# The app includes basic validation and can be tested manually
# Visit http://localhost:8000 and try various inputs
```

### Adding Rate Limiting
```python
# In settings.py, add django-ratelimit
# In views.py, add @ratelimit decorator to generate_brief
```

### Environment Variables
```bash
OPENAI_API_KEY=sk-...  # Optional, uses stub if not set
```

## 📝 Technical Notes

- **Development Time**: Completed as a focused vertical slice demo
- **Database**: SQLite (default Django setup, no custom migrations needed)
- **Code Style**: Clean, readable functions without excessive comments
- **Production Ready**: Architecture supports easy addition of Redis for rate limiting and environment-based configuration
- **API Key**: Optional - works with stub responses for development/testing without OpenAI key

---

**Built for Collabstr Full-Stack AI Developer Project**

