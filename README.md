# Market X

A smart market intelligence platform powered by AI, designed to help market participants make informed decisions through predictive analytics and personalized recommendations.

## Project Overview

Market X is a comprehensive market intelligence platform designed to help anyone who makes price-based decisions through predictive analytics and personalized recommendations. The platform uses Google Gemini AI to analyze limited market inputs and generate actionable advice.

## Key Features

- **Multi-Role Support**: Tailored insights for farmers, traders, businesses, and consumers
- **AI-Powered Analysis**: Uses Google Gemini API for market intelligence
- **Decision-Focused Output**: Clear recommendations instead of raw data
- **Responsive Design**: Works on all devices
- **Simple Interface**: Easy-to-use form-based input
- **SMS & Voice Access**: Planned accessibility features for all users

## Project Structure

```
market-x/
├── backend/
│   └── app.py              # Flask server with API endpoints
├── templates/
│   ├── landing.html        # Landing page with hero section
│   ├── role_selection.html # Role selection page
│   ├── dashboard.html      # Main dashboard with market analysis
│   ├── analysis.html       # Detailed analysis and reasoning
│   ├── alerts.html         # Market alerts and notifications
│   ├── mobile.html         # Mobile/SMS access demo
│   └── about.html          # About page with team information
├── static/
│   └── css/
│       └── style.css       # Shared CSS styles
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd market-x
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## Configuration

### Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Pages & Features

### 1. Landing Page (`/`)
- **Hero Section**: Compelling introduction with animated background
- **Feature Overview**: 6 key features with hover effects
- **Trust & Credibility**: Technology stack and MVP disclaimer
- **Footer**: Navigation and social links

### 2. Role Selection Page (`/role-selection`)
- **Purpose**: Personalize experience based on user type
- **Roles Available**:
  - 👨‍🌾 Farmers (Maximize selling price)
  - 🧑‍💼 Traders (Buy low, sell high)
  - 🏪 Businesses (Reduce costs)
  - 🏠 Consumers (Save money)
  - 👥 Cooperatives (Group benefits)
  - 🏛️ Government/NGO (Market monitoring)

### 3. Dashboard (`/dashboard`)
- **Market Input Panel**: Product, market, quantity inputs
- **Insight Cards**: Real-time AI analysis results
- **Trend Visualization**: Price projection charts
- **Role-Based Output**: Tailored recommendations

### 4. Analysis Page (`/analysis`)
- **Detailed Reasoning**: AI explanation of recommendations
- **Confidence Indicators**: Trust metrics
- **Risk Assessment**: Market volatility warnings
- **Action Steps**: Clear guidance

### 5. Alerts Page (`/alerts`)
- **Market Notifications**: Price spikes, supply changes
- **Color-Coded Cards**: Green (opportunity), Yellow (caution), Red (risk)
- **Filter Options**: By product, market, urgency
- **Notification Settings**: Customizable alerts

### 6. Mobile Access Page (`/mobile`)
- **SMS Demo**: Interactive phone mockup
- **Voice Access**: Future accessibility features
- **Inclusive Design**: Literacy-friendly interfaces
- **Impact Statistics**: Reach and accessibility metrics

### 7. About Page (`/about`)
- **Team Information**: 
  - 🧠 Nolawi Hailu - Lead Developer & System Architect
  - 🎨 Abenzer Fromsa - Frontend & UI Support
  - 💡 Biruk Genene - Product Ideation & Backend Support
- **Project Motivation**: Why we built Market X
- **Technology Stack**: System architecture overview
- **Collaboration Process**: How we worked together

## API Endpoints

### `GET /`
- **Purpose**: Serve landing page
- **Response**: HTML landing page

### `GET /role-selection`
- **Purpose**: Serve role selection page
- **Response**: HTML role selection page

### `GET /dashboard`
- **Purpose**: Serve main dashboard
- **Response**: HTML dashboard page

### `GET /analysis`
- **Purpose**: Serve detailed analysis page
- **Response**: HTML analysis page

### `GET /alerts`
- **Purpose**: Serve alerts page
- **Response**: HTML alerts page

### `GET /mobile`
- **Purpose**: Serve mobile access page
- **Response**: HTML mobile demo page

### `GET /about`
- **Purpose**: Serve about page
- **Response**: HTML about page

### `POST /analyze`
- **Purpose**: Analyze market data and return AI recommendations
- **Request Body**:
  ```json
  {
    "role": "farmer|trader|business|consumer",
    "product": "teff|coffee|maize|...",
    "market": "addis-ababa|mekelle|...",
    "quantity": "100 kg"
  }
  ```
- **Response**:
  ```json
  {
    "recommendation": "Sell Now",
    "best_market": "Addis Ababa",
    "trend": "Rising",
    "reasoning": "Market conditions indicate...",
    "confidence": "High"
  }
  ```

## Design System

### Colors
- **Primary**: #2c5f2d (Forest green)
- **Secondary**: #97bc62 (Sage green)
- **Accent**: #ff6b35 (Sunset orange)
- **Text Dark**: #2d3436
- **Text Light**: #636e72
- **Background Light**: #f8f9fa

### Typography
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Bold, 2.5rem (h1) to 1.3rem (h3)
- **Body**: 1rem, line-height 1.6
- **Buttons**: 1.1rem, font-weight 600

### Components
- **Cards**: 15px border radius, subtle shadows
- **Buttons**: 10px border radius, gradient backgrounds
- **Forms**: 10px border radius, focus states
- **Navigation**: Sticky, with scroll effects

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface and interactions |
| **Framework** | Bootstrap 5.3.0 | Responsive design and components |
| **Icons** | Font Awesome 6.4.0 | Iconography |
| **Backend** | Python 3.8+ | Server-side logic |
| **Framework** | Flask 2.3.3 | Web framework |
| **CORS** | Flask-CORS 4.0.0 | Cross-origin requests |
| **AI Engine** | Google Gemini API | Market analysis and reasoning |
| **Environment** | Python-dotenv | Configuration management |

## AI Integration

### Role-Specific Prompts
Each user role receives tailored AI prompts:
- **Farmers**: Focus on maximizing selling prices
- **Traders**: Emphasis on buy-low, sell-high strategies  
- **Businesses**: Cost reduction and price spike avoidance
- **Consumers**: Finding the lowest purchase prices

### Analysis Process
1. **Input Validation**: Check required fields
2. **Prompt Generation**: Create role-specific AI prompt
3. **API Call**: Send request to Gemini API
4. **Response Parsing**: Extract JSON from AI response
5. **Error Handling**: Graceful fallbacks for failures

## Responsive Design

### Breakpoints
- **Desktop**: >1024px
- **Tablet**: 768px-1024px
- **Mobile**: <768px
- **Small Mobile**: <480px

### Mobile Optimizations
- Collapsible navigation
- Stacked layouts
- Touch-friendly buttons
- Optimized font sizes

## Security & Privacy

### Data Protection
- No user data storage
- Environment variables for API keys
- Secure communication protocols
- Input validation and sanitization

### Ethical AI
- Transparent AI reasoning
- Confidence indicators
- Disclaimer about AI limitations
- User control over data

## Performance

### Optimization
- Lazy loading of images
- CSS animations instead of JavaScript
- Efficient DOM manipulation
- Minimal external dependencies

### Monitoring
- Error tracking
- Performance metrics
- User interaction analytics
- API response times

## MVP Limitations

### Current Scope
✅ **Included**:
- AI-powered market advice
- Decision recommendations
- Multi-user support
- Clean UI
- Mobile accessibility demo

❌ **Not Included (Yet)**:
- Real-time price feeds
- Historical datasets
- User accounts
- Payments or SMS integration
- Voice interface (planned)

### Future Roadmap
1. **Real Market Data**: Integration with Ethiopian market APIs
2. **SMS & Voice**: Full accessibility features
3. **User Accounts**: Personalization and history
4. **Mobile App**: Native iOS/Android applications
5. **Analytics**: Advanced market insights
6. **Cooperative Tools**: Group selling features

## Testing

### Manual Testing Checklist
- [ ] All pages load correctly
- [ ] Navigation works between pages
- [ ] Form submissions work
- [ ] AI analysis returns results
- [ ] Mobile responsive design
- [ ] Error handling works
- [ ] Loading states display
- [ ] Accessibility features work

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Use semantic HTML5
- Follow CSS naming conventions
- Comment complex logic
- Maintain responsive design
- Test accessibility

## Support

### Getting Help
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation
- Contact the development team

### Common Issues

**API Key Issues**:
- Ensure your Gemini API key is valid
- Check that `.env` file is in the correct location
- Verify the API key has proper permissions

**Server Issues**:
- Check if port 5000 is available
- Ensure all dependencies are installed
- Verify Python version compatibility

**Frontend Issues**:
- Clear browser cache
- Check browser console for errors
- Ensure JavaScript is enabled

## License

This project is open source and available under the [MIT License](LICENSE).

## Impact

Market X bridges the information gap in Ethiopian markets by:
- Helping farmers maximize income
- Enabling traders to make better purchasing decisions
- Assisting businesses in cost management
- Empowering consumers with price awareness

*Built for the Ethiopian market ecosystem with love*

---

## Metrics & Analytics

### Success Indicators
- User engagement rates
- Analysis completion rates
- User satisfaction scores
- Market accuracy feedback
- Accessibility adoption

### KPIs
- Daily active users
- Analysis requests per day
- Error rates below 5%
- Page load times under 3 seconds
- Mobile usage > 60%

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Status**: Hackathon MVP
