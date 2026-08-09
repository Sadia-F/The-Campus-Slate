from flask import Flask, render_template, request, redirect, flash, send_from_directory, session
import datetime
import os
import PyPDF2
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ===== SUPABASE SETUP =====
SUPABASE_URL = 'https://ymsqoqgblsuelwspssxab.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inltc3FvcWdibHN1ZWx3c3BzeGFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU3MDU5MDAsImV4cCI6MjEwMTI4MTkwMH0.ErRiLjxfqq0xlaQB0afuEAfvDhiS_uLAcRjyz2p8rig'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== TEAM PASSWORD =====
TEAM_PASSWORD = "slate2026"

# ===== STAFF DATA =====
staff = [
    {
        'id': 'sameer-kumar',
        'name': 'Sameer Kumar',
        'role': 'Editor-in-Chief',
        'bio': 'Sameer is a dedicated journalism student who has been with The Campus Slate for over 3 years.',
        'major': 'Communication Arts',
        'year': 'Senior',
        'image': '👤',
        'email': 'skumar@nyit.edu'
    },
    {
        'id': 'inaya-syed',
        'name': 'Inaya Syed',
        'role': 'Managing Editor',
        'bio': 'Inaya is a mechanical engineering student who found her passion in journalism.',
        'major': 'Mechanical Engineering',
        'year': 'Senior',
        'image': '👩‍💻',
        'email': 'isyed@nyit.edu'
    },
    {
        'id': 'kevin-horton',
        'name': 'Prof. Kevin Horton',
        'role': 'Faculty Advisor',
        'bio': 'Professor Horton has been the Faculty Advisor for The Campus Slate since 2024.',
        'major': 'Communication Arts',
        'year': 'Faculty',
        'image': '👨‍🏫',
        'email': 'khorton@nyit.edu'
    },
    {
        'id': 'sadia-ferdous',
        'name': 'Sadia Ferdous',
        'role': 'Webmaster/Digital Editor',
        'bio': 'Sadia is a Computer Science student who built this very website!',
        'major': 'Computer Science',
        'year': 'Junior',
        'image': '👩‍💻',
        'email': 'sferdous@nyit.edu'
    }
]

# ===== LOGIN HELPER FUNCTIONS =====

def is_logged_in():
    return session.get('logged_in', False)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('🔒 Please log in to access this page.')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# ===== UPLOAD HELPER FUNCTIONS =====

def upload_to_supabase(file, folder='articles'):
    """Upload a file to Supabase Storage and return the public URL"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        
        response = supabase.storage.from_(folder).upload(
            filename,
            file.read(),
            {'content-type': file.content_type}
        )
        
        public_url = supabase.storage.from_(folder).get_public_url(filename)
        return public_url
    except Exception as e:
        print(f"Upload error: {e}")
        return None

# ===== ROUTES =====

@app.route("/")
def home():
    try:
        response = supabase.table('articles').select('*').order('date', desc=True).execute()
        articles = response.data if response.data else []
    except:
        articles = []
    return render_template("home.html", articles=articles, datetime=datetime, logged_in=is_logged_in())

@app.route("/about")
def about():
    return render_template("about.html", staff=staff, logged_in=is_logged_in())

@app.route("/sections")
def sections():
    return render_template("sections.html", logged_in=is_logged_in())

@app.route("/archives")
def archives():
    try:
        response = supabase.table('articles').select('*').eq('is_pdf', True).order('date', desc=True).execute()
        articles = response.data if response.data else []
    except:
        articles = []
    return render_template("archives.html", articles=articles, logged_in=is_logged_in())

@app.route("/staff")
def staff_page():
    return render_template("staff.html", staff=staff, logged_in=is_logged_in())

@app.route("/staff/<staff_id>")
def staff_detail(staff_id):
    person = None
    for s in staff:
        if s['id'] == staff_id:
            person = s
            break
    if person:
        return render_template("staff_detail.html", person=person, logged_in=is_logged_in())
    else:
        return redirect('/staff')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == TEAM_PASSWORD:
            session['logged_in'] = True
            flash('✅ Welcome back! You are now logged in.')
            return redirect('/')
        else:
            flash('❌ Incorrect password. Please try again.')
            return redirect('/login')
    return render_template("login.html", logged_in=is_logged_in())

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('👋 You have been logged out.')
    return redirect('/')

@app.route("/team-upload", methods=['GET', 'POST'])
@login_required
def team_upload():
    if request.method == 'POST':
        content_type = request.form.get('content_type', 'article')
        
        if content_type == 'article':
            title = request.form['title']
            content = request.form['content']
            author = request.form['author']
            article_date = request.form.get('article_date', datetime.datetime.now().strftime("%Y-%m-%d"))
            section = request.form.get('section', '')
            
            try:
                date_obj = datetime.datetime.strptime(article_date, "%Y-%m-%d")
                display_date = date_obj.strftime("%Y-%m-%d")
            except:
                display_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            image_url = None
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file and image_file.filename != '':
                    image_url = upload_to_supabase(image_file, 'article-images')
            
            article_data = {
                'title': title,
                'content': content,
                'author': author,
                'date': display_date,
                'section': section,
                'image_url': image_url,
                'is_pdf': False
            }
            
            try:
                supabase.table('articles').insert(article_data).execute()
                flash('✅ Article published successfully!')
            except Exception as e:
                flash(f'❌ Error saving article: {str(e)}')
            
            return redirect('/')
            
        elif content_type == 'pdf':
            if 'file' not in request.files:
                flash('No file selected')
                return redirect('/team-upload')
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected')
                return redirect('/team-upload')
            
            if file and file.filename.endswith('.pdf'):
                pdf_url = upload_to_supabase(file, 'pdf-issues')
                
                if pdf_url:
                    issue_name = request.form.get('issue_name', file.filename.replace('.pdf', ''))
                    
                    article_data = {
                        'title': f"📄 {issue_name}",
                        'content': 'Click "Read Full Issue" to view the complete PDF.',
                        'author': 'The Campus Slate',
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'section': 'Archives',
                        'pdf_url': pdf_url,
                        'is_pdf': True
                    }
                    
                    try:
                        supabase.table('articles').insert(article_data).execute()
                        flash(f'✅ Successfully uploaded: {file.filename}')
                    except Exception as e:
                        flash(f'❌ Error saving PDF: {str(e)}')
                else:
                    flash('❌ Error uploading PDF to storage')
            else:
                flash('❌ Please upload a PDF file')
            
            return redirect('/')
    
    return render_template("team_upload.html", logged_in=is_logged_in())

@app.route("/delete/<int:index>")
@login_required
def delete(index):
    try:
        response = supabase.table('articles').select('*').order('date', desc=True).execute()
        articles = response.data if response.data else []
        
        if index < len(articles):
            article_id = articles[index]['id']
            supabase.table('articles').delete().eq('id', article_id).execute()
            flash('🗑️ Article deleted successfully.')
        else:
            flash('❌ Article not found.')
    except Exception as e:
        flash(f'❌ Error deleting article: {str(e)}')
    
    return redirect('/')

@app.route("/view-pdf/<path:pdf_url>")
def view_pdf(pdf_url):
    return render_template("view_pdf.html", pdf_url=pdf_url, logged_in=is_logged_in())

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)