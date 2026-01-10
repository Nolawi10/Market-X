from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import json
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
CORS(app)

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        'app_name': 'Market X',
        'tagline': 'Smart Market Decisions for Everyone',
        'farmer_mode': 'Farmer Mode',
        'trader_mode': 'Trader Mode',
        'business_mode': 'Business Mode',
        'consumer_mode': 'Consumer Mode',
        'cooperative_mode': 'Cooperative Mode',
        'government_mode': 'Government Mode',
        'product': 'Product / Crop',
        'market': 'Market / Location',
        'quantity': 'Quantity',
        'analyze_market': 'Analyze Market',
        'market_insights': 'Market Insights',
        'ai_recommendation': 'AI Recommendation',
        'estimated_price': 'Estimated Price',
        'trend': '7-Day Trend',
        'best_market': 'Best Market',
        'confidence': 'Confidence',
        'current_market_price': 'Current market price',
        'per_animal': 'per animal',
        'per_kg': 'per kg',
        'select_product': 'Select product...',
        'select_market': 'Select market...',
        'enter_quantity': 'Enter quantity',
        'cereal_crops': 'Cereal Crops',
        'cash_crops': 'Cash Crops',
        'legumes': 'Legumes',
        'produce': 'Produce',
        'livestock': 'Livestock'
    },
    'am': {
        'app_name': 'ማርኬት X',
        'tagline': 'ለሁሉም ሰው ብልሃት ገበያቶች',
        'farmer_mode': 'ገበሬ ሁነታ',
        'trader_mode': 'ነጋዴ ሁነታ',
        'business_mode': 'ቢዝነስ ሁነታ',
        'consumer_mode': 'ደንቀኛ ሁነታ',
        'cooperative_mode': 'ኮኦፐሬቲቭ ሁነታ',
        'government_mode': 'መንግስትኛ ሁነታ',
        'product': 'እቃዎች / እርሻሎች',
        'market': 'ገበያቶች / አካባቢ',
        'quantity': 'እልከም',
        'analyze_market': 'ገበያ ትንተን',
        'market_insights': 'የገበያ እይታዎች',
        'ai_recommendation': 'AI አስተያዪ',
        'estimated_price': 'የተገመተ ዋጋ',
        'trend': '7-ቀን አዝምድ',
        'best_market': 'ምርጡ ገበይ',
        'confidence': 'የታማኛነት ደረጃ',
        'current_market_price': 'የአሁኑ ገበያ ዋጋ',
        'per_animal': 'ለእያኛ እንስሳት',
        'per_kg': 'ለኪሎግራም',
        'select_product': 'እቃ ይምረጡ...',
        'select_market': 'ገበይ ይምረጡ...',
        'enter_quantity': 'እልከም ያስገቡ',
        'cereal_crops': 'የምግብር እርሻሎች',
        'cash_crops': 'የገንዘብ እርሻሎች',
        'legumes': 'ባቄላዎች',
        'produce': 'እርሻሎች',
        'livestock': 'እንስሳት'
    }
}


def get_translation(key, lang='en'):
    """Get translation for a key in specified language"""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))


def translate_text_with_gemini(text, target_lang):
    """Translate text using Gemini API"""
    if not model or target_lang == 'en':
        return text

    try:
        lang_map = {'am': 'Amharic', 'en': 'English'}
        target_language = lang_map.get(target_lang, 'English')

        prompt = f"Translate the following text to {target_language}. Only return the translated text, no explanations:\n\n{text}"

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails


# Configure Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables")
        model = None
    else:
        genai.configure(api_key=api_key)
        # Use the most basic model name that should work
        try:
            model = genai.GenerativeModel('gemini-pro-latest')
            print("Using model: gemini-pro-latest")
        except:
            try:
                model = genai.GenerativeModel('gemini-pro')
                print("Using model: gemini-pro")
            except:
                try:
                    model = genai.GenerativeModel('text-bison-001')
                    print("Using model: text-bison-001")
                except:
                    model = None
                    print("Could not initialize any Gemini model")

        if model:
            print("Gemini API configured successfully")
except Exception as e:
    print(f"Warning: Gemini API not configured - {e}")
    model = None

# Simple user database (in production, use a real database)
users = {}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Landing page"""
    return render_template('landing.html')


@app.route('/set-language', methods=['POST'])
def set_language():
    """Set language preference"""
    lang = request.form.get('language', 'en')
    if lang in ['en', 'am']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))


@app.route('/translate-text', methods=['POST'])
def translate_text():
    """Translate text using Gemini API"""
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    translated = translate_text_with_gemini(text, target_lang)
    return jsonify({'translated_text': translated})


@app.route('/auth')
def auth():
    """Authentication page"""
    lang = session.get('language', 'en')
    return render_template('auth.html', lang=lang, translations=TRANSLATIONS[lang])


@app.route('/login', methods=['POST'])
def login():
    """Handle login"""
    email = request.form.get('email')
    password = request.form.get('password')

    # Simple validation (in production, use proper authentication)
    if email and password:
        user_id = str(hash(email))  # Simple user identification
        users[user_id] = {
            'email': email,
            'role': None  # Will be set after role selection
        }
        session['user_id'] = user_id
        flash('Login successful! Please select your role.', 'success')
        return redirect(url_for('role_selection'))
    else:
        flash('Please enter valid email and password', 'error')
        return redirect(url_for('auth'))


@app.route('/signup', methods=['POST'])
def signup():
    """Handle signup"""
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([email, password, confirm_password]):
        flash('Please fill all fields', 'error')
        return redirect(url_for('auth'))

    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('auth'))

    # Create new user
    user_id = str(hash(email))
    users[user_id] = {
        'email': email,
        'role': None
    }
    session['user_id'] = user_id
    flash('Account created successfully! Please select your role.', 'success')
    return redirect(url_for('role_selection'))


@app.route('/role-selection')
@login_required
def role_selection():
    """Role selection page"""
    return render_template('role_selection.html')


@app.route('/set-role', methods=['POST'])
@login_required
def set_role():
    """Set user role"""
    role = request.form.get('role')
    if role in ['farmer', 'trader', 'business', 'consumer', 'cooperative', 'government']:
        user_id = session['user_id']
        if user_id in users:
            users[user_id]['role'] = role
            session['user_role'] = role
            flash(f'Role set as {role}', 'success')
            return redirect(url_for('dashboard'))

    flash('Please select a valid role', 'error')
    return redirect(url_for('role_selection'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user_role = session.get('user_role', 'farmer')
    lang = session.get('language', 'en')
    return render_template('dashboard.html', user_role=user_role, lang=lang, translations=TRANSLATIONS[lang])


@app.route('/analysis')
@login_required
def analysis():
    """Analysis page"""
    user_role = session.get('user_role', 'farmer')
    return render_template('analysis.html', user_role=user_role)


@app.route('/alerts')
@login_required
def alerts():
    """Alerts page"""
    user_role = session.get('user_role', 'farmer')
    return render_template('alerts.html', user_role=user_role)


@app.route('/mobile')
@login_required
def mobile():
    """Mobile access page"""
    return render_template('mobile.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))


@app.route('/analyze', methods=['POST'])
@login_required
def analyze_market():
    """Analyze market data and return AI recommendations"""
    try:
        data = request.get_json()

        # Extract user inputs
        user_role = data.get('role', session.get('user_role', 'farmer'))
        product = data.get('product', '')
        market = data.get('market', '')
        quantity = data.get('quantity', '')

        if not all([user_role, product, market]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Smart fallback analysis (works without Gemini API)
        result = generate_smart_fallback(user_role, product, market, quantity)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


def generate_smart_fallback(user_role, product, market, quantity):
    """Generate intelligent market analysis without AI"""

    # Product-specific price ranges (ETB per kg for crops, ETB per animal for livestock)
    price_ranges = {
        'teff': {'min': 45, 'max': 85, 'avg': 65},
        'coffee': {'min': 120, 'max': 280, 'avg': 200},
        'maize': {'min': 15, 'max': 35, 'avg': 25},
        'wheat': {'min': 20, 'max': 40, 'avg': 30},
        'sorghum': {'min': 18, 'max': 38, 'avg': 28},
        'beans': {'min': 25, 'max': 55, 'avg': 40},
        'lentils': {'min': 30, 'max': 60, 'avg': 45},
        'vegetables': {'min': 8, 'max': 25, 'avg': 15},
        'fruits': {'min': 12, 'max': 40, 'avg': 25},
        'livestock': {'min': 3000, 'max': 8000, 'avg': 5500},
        # Average cow/ox price in ETB
        'cattle': {'min': 15000, 'max': 35000, 'avg': 25000},
        # Average goat price in ETB
        'goats': {'min': 2500, 'max': 6000, 'avg': 4000},
        # Average sheep price in ETB
        'sheep': {'min': 2000, 'max': 5000, 'avg': 3200},
        # Average chicken price in ETB
        'chickens': {'min': 300, 'max': 800, 'avg': 500},
        # Average camel price in ETB
        'camels': {'min': 25000, 'max': 60000, 'avg': 40000},
        # Average bee colony with honey in ETB
        'bees_honey': {'min': 800, 'max': 2000, 'avg': 1200}
    }

    # Market-specific multipliers
    market_multipliers = {
        'addis-ababa': 1.2,
        'mekelle': 1.1,
        'gondar': 1.0,
        'bahirdar': 1.05,
        'hawassa': 0.95,
        'jimma': 0.9,
        'dire-dawa': 1.15,
        'adama': 1.0,
        'shashemene': 0.85,
        'local': 0.8
    }

    # Get base price for product
    product_info = price_ranges.get(
        product.lower(), {'min': 20, 'max': 50, 'avg': 35, 'category': 'general', 'seasonality': 'standard market patterns', 'demand': 'moderate demand', 'perishability': 'standard', 'storage': 'standard storage requirements'})
    base_price = product_info['avg']

    # Apply market multiplier
    multiplier = market_multipliers.get(market.lower(), 1.0)
    estimated_price = int(base_price * multiplier)

    # Create market_info structure for detailed insights
    market_info = {
        'multiplier': multiplier,
        'characteristics': f"{market.title()} market",
        'infrastructure': 'standard infrastructure',
        'buyer_types': 'general buyers',
        'price_sensitivity': 'moderate price sensitivity',
        'competition': 'moderate competition'
    }

    # Role-specific recommendations
    role_recommendations = {
        'farmer': {
            'recommendation': 'Sell Immediately' if multiplier >= 1.15 else 'Sell This Week' if multiplier >= 1.05 else 'Wait 2-3 Weeks' if multiplier >= 0.95 else 'Hold for Better Prices',
            'reasoning': f"As a farmer, {market.title()} offers {'excellent prices' if multiplier >= 1.15 else 'good prices' if multiplier >= 1.05 else 'fair prices' if multiplier >= 0.95 else 'below average prices'} for your {product}. Consider seasonal factors and market competition."
        },
        'trader': {
            'recommendation': 'Buy Now - Bulk Discount Available' if multiplier <= 0.9 else 'Buy and Hold for Price Increase' if multiplier <= 1.0 else 'Wait for Better Supply' if multiplier <= 1.1 else 'Seek Alternative Markets',
            'reasoning': f"As a trader, {market.title()} presents {'excellent buying opportunity' if multiplier <= 0.9 else 'good opportunity' if multiplier <= 1.0 else 'moderate opportunity' if multiplier <= 1.1 else 'challenging conditions'} for {product}. Consider transport costs and market competition."
        },
        'business': {
            'recommendation': 'Bulk Purchase Now' if multiplier <= 0.85 else 'Negotiate Volume Discount' if multiplier <= 0.95 else 'Standard Purchase' if multiplier <= 1.05 else 'Seek Alternatives or Reduce Usage',
            'reasoning': f"For your business, {market.title()} offers {'cost-effective procurement' if multiplier <= 0.85 else 'reasonable pricing' if multiplier <= 0.95 else 'market rates' if multiplier <= 1.05 else 'premium pricing'} for {product}. Consider supply chain reliability and quality consistency."
        },
        'consumer': {
            'recommendation': 'Buy Now - Good Value' if multiplier <= 0.85 else 'Standard Purchase' if multiplier <= 0.95 else 'Wait for Sales or Alternatives' if multiplier <= 1.05 else 'Consider Substitutes or Reduce Consumption',
            'reasoning': f"As a consumer, {product} prices in {market.title()} are {'excellent value' if multiplier <= 0.85 else 'fair' if multiplier <= 0.95 else 'above average' if multiplier <= 1.05 else 'expensive'}. Consider quality vs price and seasonal availability."
        },
        'cooperative': {
            'recommendation': 'Organize Group Sale Immediately' if multiplier >= 1.15 else 'Coordinate Group Sale This Week' if multiplier >= 1.05 else 'Pool Resources for Better Timing' if multiplier >= 0.95 else 'Collective Bargaining for Future Sale',
            'reasoning': f"Your cooperative can leverage collective bargaining power in {market.title()}. Current conditions {'favor immediate group action' if multiplier >= 1.15 else 'support coordinated selling' if multiplier >= 1.05 else 'require strategic timing' if multiplier >= 0.95 else 'suggest waiting for better conditions'} for {product}."
        },
        'government': {
            'recommendation': 'Monitor Market Stability' if multiplier <= 1.1 else 'Investigate Price Volatility' if multiplier <= 1.2 else 'Implement Market Intervention Measures',
            'reasoning': f"Market analysis for {product} in {market.title()} shows {'stable conditions' if multiplier <= 1.1 else 'moderate volatility' if multiplier <= 1.2 else 'high volatility'}. Monitor supply chain factors and market efficiency impacts."
        }
    }

    # Enhanced trend analysis based on market and product
    if multiplier >= 1.15:
        trend = 'Rising Rapidly'
        confidence = 'High'
    elif multiplier >= 1.05:
        trend = 'Rising'
        confidence = 'High'
    elif multiplier <= 0.85:
        trend = 'Falling'
        confidence = 'Medium'
    elif multiplier <= 0.95:
        trend = 'Stable to Falling'
        confidence = 'Medium'
    else:
        trend = 'Stable'
        confidence = 'High'

    # Get role-specific recommendation
    role_info = role_recommendations.get(
        user_role, role_recommendations['farmer'])
    recommendation = role_info['recommendation']

    # Find best alternative market
    best_market = max(market_multipliers.keys(),
                      key=lambda k: market_multipliers[k])

    return {
        'recommendation': role_info['recommendation'],
        'best_market': best_market.replace('-', ' ').title(),
        'trend': trend,
        'reasoning': role_info['reasoning'],
        'confidence': confidence,
        'estimated_price': f'{estimated_price} ETB/kg' if product.lower() not in ['cattle', 'goats', 'sheep', 'chickens', 'camels', 'bees_honey'] else f'{estimated_price} ETB per animal',
        'detailed_insights': {
            'price_forecast': generate_price_forecast(product, market, multiplier, product_info),
            'market_analysis': generate_market_analysis(market, market_info, multiplier),
            'risk_assessment': generate_risk_assessment(multiplier, product_info, market_info),
            'opportunity_score': calculate_opportunity_score(multiplier, product_info, market_info),
            'seasonal_impact': analyze_seasonal_impact(product, product_info),
            'competitor_analysis': generate_competitor_analysis(market, market_info),
            'economic_indicators': generate_economic_indicators(multiplier, product_info),
            'action_timeline': generate_action_timeline(recommendation, multiplier)
        }
    }


def generate_price_forecast(product, market, multiplier, product_info):
    """Generate detailed price forecast"""
    base_price = product_info['avg']  # Direct access to avg price

    # Calculate 30-day forecast
    if multiplier >= 1.15:
        forecast_trend = "Strong upward trajectory expected"
        next_week = int(base_price * multiplier * 1.05)
        next_month = int(base_price * multiplier * 1.12)
    elif multiplier >= 1.05:
        forecast_trend = "Moderate growth projected"
        next_week = int(base_price * multiplier * 1.02)
        next_month = int(base_price * multiplier * 1.06)
    elif multiplier <= 0.85:
        forecast_trend = "Declining trend anticipated"
        next_week = int(base_price * multiplier * 0.95)
        next_month = int(base_price * multiplier * 0.88)
    else:
        forecast_trend = "Stable prices expected"
        next_week = int(base_price * multiplier)
        next_month = int(base_price * multiplier)

    return {
        'current_price': int(base_price * multiplier),
        'next_week': next_week,
        'next_month': next_month,
        'trend': forecast_trend,
        'volatility': 'High' if multiplier >= 1.15 or multiplier <= 0.85 else 'Medium' if multiplier >= 1.1 or multiplier <= 0.9 else 'Low'
    }


def generate_market_analysis(market, market_info, multiplier):
    """Generate detailed market analysis"""
    return {
        'market_strength': 'Strong' if multiplier >= 1.1 else 'Moderate' if multiplier >= 0.95 else 'Weak',
        'buyer_behavior': 'Aggressive purchasing' if multiplier >= 1.1 else 'Selective buying' if multiplier >= 0.95 else 'Cautious approach',
        'supply_level': 'Limited supply' if multiplier >= 1.1 else 'Adequate supply' if multiplier >= 0.95 else 'Excess supply',
        'market_competition': 'High competition' if market_info['multiplier'] >= 1.1 else 'Moderate competition' if market_info['multiplier'] >= 0.95 else 'Low competition',
        'infrastructure_quality': market_info['infrastructure'],
        'market_reach': market_info['characteristics']
    }


def generate_risk_assessment(multiplier, product_info, market_info):
    """Generate comprehensive risk assessment"""
    risk_factors = []
    risk_level = 'Low'

    if multiplier >= 1.15:
        risk_factors.append("Price correction risk due to rapid increase")
        risk_level = 'Medium'
    elif multiplier <= 0.85:
        risk_factors.append("Market oversupply risk")
        risk_level = 'High'

    if product_info.get('perishability') == 'highly perishable':
        risk_factors.append("High perishability risk")
        risk_level = 'High' if risk_level != 'High' else 'Very High'

    if market_info['multiplier'] < 1.0:
        risk_factors.append("Limited market access")

    return {
        'overall_risk': risk_level,
        'risk_factors': risk_factors,
        'mitigation_strategies': [
            "Diversify market outlets",
            "Monitor price trends daily",
            "Consider storage options",
            "Build buyer relationships"
        ],
        'market_stability': 'Stable' if 0.9 <= multiplier <= 1.1 else 'Unstable'
    }


def calculate_opportunity_score(multiplier, product_info, market_info):
    """Calculate market opportunity score (0-100)"""
    base_score = 50

    # Price momentum score
    if multiplier >= 1.15:
        price_score = 25
    elif multiplier >= 1.05:
        price_score = 15
    elif multiplier <= 0.85:
        price_score = -10
    else:
        price_score = 0

    # Market quality score
    market_score = 10 if market_info['multiplier'] >= 1.1 else 5 if market_info['multiplier'] >= 0.95 else -5

    # Product demand score
    demand_score = 10 if product_info.get(
        'demand') == 'high demand' else 5 if product_info.get('demand') == 'stable demand' else 0

    total_score = base_score + price_score + market_score + demand_score
    return max(0, min(100, total_score))


def analyze_seasonal_impact(product, product_info):
    """Analyze seasonal impact on product"""
    seasonal_factors = product_info.get(
        'seasonality', 'Standard market patterns')

    return {
        'current_season': 'Peak season' if 'peak' in seasonal_factors.lower() else 'Growing season' if 'season' in seasonal_factors.lower() else 'Off-season',
        'seasonal_trend': seasonal_factors,
        'best_timing': product_info.get('seasonality', 'Year-round availability'),
        'storage_impact': product_info.get('storage', 'Standard storage requirements')
    }


def generate_competitor_analysis(market, market_info):
    """Generate competitor analysis"""
    competition_level = market_info['competition']

    return {
        'competition_intensity': competition_level,
        'market_saturation': 'High' if 'high' in competition_level.lower() else 'Medium' if 'moderate' in competition_level.lower() else 'Low',
        'competitive_advantage': [
            "Quality differentiation",
            "Supply reliability",
            "Price competitiveness",
            "Market relationships"
        ],
        'barriers_to_entry': 'Low' if market_info['multiplier'] < 1.0 else 'Medium' if market_info['multiplier'] < 1.1 else 'High'
    }


def generate_economic_indicators(multiplier, product_info):
    """Generate economic indicators"""
    return {
        'market_health': 'Excellent' if multiplier >= 1.15 else 'Good' if multiplier >= 1.05 else 'Fair' if multiplier >= 0.95 else 'Poor',
        'inflation_pressure': 'High' if multiplier >= 1.1 else 'Moderate' if multiplier >= 0.95 else 'Low',
        'demand_growth': 'Strong' if multiplier >= 1.1 else 'Moderate' if multiplier >= 0.95 else 'Weak',
        'market_efficiency': 85 if multiplier >= 0.95 else 70,
        'price_elasticity': 'Inelastic' if product_info.get('category') == 'cereal' else 'Elastic'
    }


def generate_action_timeline(recommendation, multiplier):
    """Generate detailed action timeline"""
    if 'Immediately' in recommendation:
        return {
            'urgent_actions': ['Execute sale today', 'Contact buyers', 'Finalize logistics'],
            'short_term': ['Monitor market reaction', 'Plan next transaction'],
            'medium_term': ['Evaluate performance', 'Adjust strategy'],
            'optimal_window': '24-48 hours'
        }
    elif 'This Week' in recommendation:
        return {
            'urgent_actions': ['Prepare for sale', 'Identify buyers', 'Quality check'],
            'short_term': ['Execute within 3-5 days', 'Monitor price changes'],
            'medium_term': ['Plan next cycle', 'Build relationships'],
            'optimal_window': '3-7 days'
        }
    elif 'Wait' in recommendation:
        return {
            'urgent_actions': ['Monitor market trends', 'Prepare storage', 'Research alternatives'],
            'short_term': ['Weekly price review', 'Market research'],
            'medium_term': ['Strategic planning', 'Market expansion'],
            'optimal_window': '2-4 weeks'
        }
    else:
        return {
            'urgent_actions': ['Market analysis', 'Risk assessment', 'Strategic planning'],
            'short_term': ['Trend monitoring', 'Opportunity identification'],
            'medium_term': ['Long-term positioning', 'Market development'],
            'optimal_window': '4-8 weeks'
        }


@app.route('/api/status')
def api_status():
    """Check API status"""
    return jsonify({
        'gemini_api': model is not None,
        'users_count': len(users),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("Starting Market X Flask server...")
    print("Gemini API Status:", "Connected" if model else "Not Connected")
    print("Templates folder:", app.template_folder)

    # Check if templates folder exists
    if os.path.exists('templates'):
        print("Available templates:", os.listdir('templates'))
    else:
        print("Warning: Templates folder not found")

    print("Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
