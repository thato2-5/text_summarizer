from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from models import db, User, Summary
from auth import auth_bp
from utils import summarizer
from datetime import datetime, timedelta
import json
from collections import defaultdict

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    total_summaries = Summary.query.filter_by(user_id=current_user.id).count()
    
    # Recent summaries
    recent_summaries = Summary.query.filter_by(user_id=current_user.id)\
        .order_by(Summary.created_at.desc()).limit(5).all()
    
    # Weekly statistics
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_summaries = Summary.query.filter(
        Summary.user_id == current_user.id,
        Summary.created_at >= week_ago
    ).all()
    
    # Prepare analytics data
    daily_counts = defaultdict(int)
    for summary in weekly_summaries:
        date_str = summary.created_at.strftime('%Y-%m-%d')
        daily_counts[date_str] += 1
    
    analytics_data = {
        'labels': list(daily_counts.keys()),
        'data': list(daily_counts.values())
    }
    
    return render_template('dashboard.html',
                         total_summaries=total_summaries,
                         recent_summaries=recent_summaries,
                         analytics_data=json.dumps(analytics_data))

@app.route('/summarize', methods=['POST'])
@login_required
def summarize_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        method = data.get('method', 'lsa')
        sentences_count = data.get('sentences_count')
        language = data.get('language', 'english')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text.split()) < 10:
            return jsonify({'error': 'Text must be at least 10 words long'}), 400
        
        # Generate summary
        summary, summary_length, original_length, compression_ratio = summarizer.summarize(
            text, method, sentences_count, language
        )
        
        # Analyze sentiment
        sentiment = summarizer.analyze_sentiment(text)
        
        # Get text statistics
        stats = summarizer.get_text_stats(text)
        
        # Save to database
        title = text[:100] + '...' if len(text) > 100 else text
        new_summary = Summary(
            original_text=text,
            summary_text=summary,
            summary_length=summary_length,
            original_length=original_length,
            compression_ratio=compression_ratio,
            user_id=current_user.id,
            title=title,
            language=language
        )
        
        db.session.add(new_summary)
        db.session.commit()
        
        return jsonify({
            'summary': summary,
            'stats': {
                'original_length': original_length,
                'summary_length': summary_length,
                'compression_ratio': round(compression_ratio, 2),
                'sentiment': round(sentiment, 3)
            },
            'text_stats': stats,
            'summary_id': new_summary.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
@login_required
def history():
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Filtering
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    min_length = request.args.get('min_length', type=int)
    max_length = request.args.get('max_length', type=int)
    
    query = Summary.query.filter_by(user_id=current_user.id)
    
    if date_from:
        query = query.filter(Summary.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Summary.created_at <= datetime.strptime(date_to, '%Y-%m-%d'))
    if min_length:
        query = query.filter(Summary.original_length >= min_length)
    if max_length:
        query = query.filter(Summary.original_length <= max_length)
    
    summaries = query.order_by(Summary.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('history.html', summaries=summaries)

@app.route('/summary/<int:summary_id>')
@login_required
def view_summary(summary_id):
    summary = Summary.query.filter_by(id=summary_id, user_id=current_user.id).first_or_404()
    return render_template('summary.html', summary=summary)

@app.route('/api/analytics')
@login_required
def get_analytics():
    # Get time range parameter (week, month, year)
    time_range = request.args.get('range', 'week')
    
    if time_range == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    elif time_range == 'year':
        start_date = datetime.utcnow() - timedelta(days=365)
    else:  # week
        start_date = datetime.utcnow() - timedelta(days=7)
    
    summaries = Summary.query.filter(
        Summary.user_id == current_user.id,
        Summary.created_at >= start_date
    ).all()
    
    # Prepare data for charts
    daily_counts = defaultdict(int)
    method_counts = defaultdict(int)
    length_ranges = defaultdict(int)
    
    for summary in summaries:
        # Daily counts
        date_str = summary.created_at.strftime('%Y-%m-%d')
        daily_counts[date_str] += 1
        
        # Method usage (though we only have one method now, structure for future)
        method_counts['standard'] += 1
        
        # Length ranges
        if summary.original_length < 100:
            length_ranges['<100'] += 1
        elif summary.original_length < 500:
            length_ranges['100-500'] += 1
        elif summary.original_length < 1000:
            length_ranges['500-1000'] += 1
        else:
            length_ranges['>1000'] += 1
    
    return jsonify({
        'daily_counts': {
            'labels': list(daily_counts.keys()),
            'data': list(daily_counts.values())
        },
        'method_usage': {
            'labels': list(method_counts.keys()),
            'data': list(method_counts.values())
        },
        'length_ranges': {
            'labels': list(length_ranges.keys()),
            'data': list(length_ranges.values())
        }
    })

@app.route('/delete_summary/<int:summary_id>', methods=['POST'])
@login_required
def delete_summary(summary_id):
    summary = Summary.query.filter_by(id=summary_id, user_id=current_user.id).first_or_404()
    db.session.delete(summary)
    db.session.commit()
    flash('Summary deleted successfully!', 'success')
    return redirect(url_for('history'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

