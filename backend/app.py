from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
CORS(app)

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Warning: Gemini API not configured - {e}")
    model = None


@app.route('/')
def index():
    print(f"Template folder: {app.template_folder}")
    print("Looking for: landing.html")
    return render_template('landing.html')


@app.route('/role-selection')
def role_selection():
    return render_template('role_selection.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/alerts')
def alerts():
    return render_template('alerts.html')


@app.route('/mobile')
def mobile():
    return render_template('mobile.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/analyze', methods=['POST'])
def analyze_market():
    try:
        data = request.get_json()

        # Extract user inputs
        user_role = data.get('role', '')
        product = data.get('product', '')
        market = data.get('market', '')
        quantity = data.get('quantity', '')

        if not all([user_role, product, market]):
            return jsonify({'error': 'Missing required fields'}), 400

        if model is None:
            # Fallback response when Gemini is not available
            return jsonify({
                'recommendation': 'Wait for better prices',
                'best_market': market,
                'trend': 'Stable',
                'reasoning': 'AI service not available. Please check API configuration.',
                'confidence': 'Low'
            })

        # Create tailored prompt based on user role
        role_specific_prompts = {
            'farmer': 'As a farmer in Ethiopia, you want to maximize your selling price.',
            'trader': 'As a trader in Ethiopia, you want to buy low and sell efficiently.',
            'business': 'As a small business owner in Ethiopia, you want to reduce costs and avoid price spikes.',
            'consumer': 'As a consumer in Ethiopia, you want to buy essentials at the lowest cost.'
        }

        prompt = f"""
        You are an AI market analyst for Ethiopian markets. {role_specific_prompts.get(user_role, '')}
        
        Market Analysis Request:
        - Product: {product}
        - Market/Location: {market}
        - Quantity: {quantity}
        - User Role: {user_role}
        
        Provide market intelligence in JSON format with these exact keys:
        - recommendation: Clear action (e.g., "Sell Now", "Wait 3-5 days", "Buy Now", "Hold")
        - best_market: Specific market recommendation
        - trend: Price trend for next 7 days (Rising/Falling/Stable)
        - reasoning: Brief explanation (2-3 sentences max)
        - confidence: Confidence level (High/Medium/Low)
        
        Consider Ethiopian market conditions, seasonal factors, and typical supply/demand patterns.
        Be practical and actionable. Keep responses concise.
        """

        response = model.generate_content(prompt)

        # Parse the response
        try:
            result_text = response.text
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                import json
                result = json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                result = {
                    'recommendation': 'Wait for better information',
                    'best_market': market,
                    'trend': 'Stable',
                    'reasoning': result_text[:200] + '...' if len(result_text) > 200 else result_text,
                    'confidence': 'Medium'
                }
        except Exception as parse_error:
            result = {
                'recommendation': 'Consult local market',
                'best_market': market,
                'trend': 'Uncertain',
                'reasoning': f'Analysis error: {str(parse_error)}',
                'confidence': 'Low'
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
