from flask import Flask, render_template, request, redirect, flash, session
import datetime
import os
import PyPDF2
from supabase import create_client

app = Flask(__name__)
app.secret_key = 'campus-slate-secret-key-2026-08-09'

# ===== SUPABASE SETUP =====
SUPABASE_URL = 'https://ymsqoqgblsuelwspssxab.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inltc3FvcWdibHN1ZWx3c3BzeGFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU3MDU5MDAsImV4cCI6MjEwMTI4MTkwMH0.ErRiLjxfqq0xlaQB0afuEAfvDhiS_uLAcRjyz2p8rig'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== TEAM PASSWORD =====
TEAM_PASSWORD = "slate2026"

# ===== STAFF DATA =====
staff = [
    {
        'id': 'sameer-kumar',
        'name': 'Sameer Kumar',
        'role': 'Editor-in-Chief',
        'bio': 'Sameer is a dedicated journalism student who has been with The Campus Slate for over 3 years. As Editor-in-Chief, he leads the team with vision and enthusiasm, ensuring every issue reflects the diverse voices of NYIT. He is passionate about storytelling and believes in the power of student journalism to create change.',
        'major': 'Communication Arts',
        'year': 'Senior',
        'image': '👤',
        'email': 'skumar@nyit.edu',
        'articles_written': ['The Campus Slate: A New Era', 'Student Voices Matter', 'Not Just A Club, It\'s My Home Away From Home']
    },
    {
        'id': 'inaya-syed',
        'name': 'Inaya Syed',
        'role': 'Managing Editor',
        'bio': 'Inaya is a mechanical engineering student who found her passion in journalism. As Managing Editor, she oversees the editorial process and ensures every article meets the highest standards. She founded the Pre-Dental Society and is committed to helping students find their voice.',
        'major': 'Mechanical Engineering',
        'year': 'Senior',
        'image': '👩‍💻',
        'email': 'isyed@nyit.edu',
        'articles_written': ['New Startup Center: A NESTS Course Exclusive', '10 Tips to Save Money']
    },
    {
        'id': 'brayan-crespo',
        'name': 'Brayan Crespo',
        'role': 'Layout & Design Editor',
        'bio': 'Brayan is the creative force behind the visual design of The Campus Slate. He ensures every issue is visually stunning and professionally laid out. His design skills bring the publication to life.',
        'major': 'Graphic Design',
        'year': 'Senior',
        'image': '🎨',
        'email': 'bcrespo@nyit.edu',
        'articles_written': ['Designing the Future of Student Publications']
    },
    {
        'id': 'nawrin-sikder',
        'name': 'Nawrin Sikder',
        'role': 'Webmaster/Digital Editor',
        'bio': 'Nawrin is a Computer Science student who manages the digital presence of The Campus Slate. She ensures the website runs smoothly and content is accessible to all readers.',
        'major': 'Computer Science',
        'year': 'Junior',
        'image': '👩‍💻',
        'email': 'nsikder@nyit.edu',
        'articles_written': ['Digital Transformation at NYIT']
    },
    {
        'id': 'sadia-ferdous',
        'name': 'Sadia Ferdous',
        'role': 'Webmaster/Digital Editor',
        'bio': 'Sadia is a Computer Science student who built this very website! As Webmaster, she manages the digital presence of The Campus Slate and creates the online experience for readers. She is passionate about coding and storytelling.',
        'major': 'Computer Science',
        'year': 'Junior',
        'image': '👩‍💻',
        'email': 'sferdous@nyit.edu',
        'articles_written': ['The Badminton Club: Creating a Legacy at NYIT']
    },
    {
        'id': 'ashley-alexander',
        'name': 'Ashley Alexander',
        'role': 'Video Journalism Editor',
        'bio': 'Ashley is a Life Sciences student who brings stories to life through video. As Video Journalism Editor, she creates compelling visual content and manages the Slate\'s YouTube channel. She is passionate about public health education.',
        'major': 'Life Sciences (BS/DO)',
        'year': 'Senior',
        'image': '🎥',
        'email': 'aalexander@nyit.edu',
        'articles_written': ['The Death of the "Third Place"', '2025 Update on Cardiovascular Medicine']
    },
    {
        'id': 'beste-tatlican',
        'name': 'Beste Tatlican',
        'role': 'Former Editor-in-Chief',
        'bio': 'Beste led The Campus Slate through its rejuvenation as Editor-in-Chief. She was instrumental in bringing the publication back to life and launching its video journalism division. She is now pursuing a career in medicine.',
        'major': 'BS/DO Program',
        'year': 'Alumna',
        'image': '👩‍⚕️',
        'email': 'btatlican@nyit.edu',
        'articles_written': ['The Campus Slate: A New Chapter']
    },
    {
        'id': 'kevin-horton',
        'name': 'Prof. Kevin Horton',
        'role': 'Faculty Advisor',
        'bio': 'Professor Horton has been the Faculty Advisor for The Campus Slate since 2024. With over 25 years of experience running The Gold Coast Gazette, he brings a wealth of knowledge and expertise. He is passionate about mentoring young journalists and helping them find their voice.',
        'major': 'Communication Arts',
        'year': 'Faculty',
        'image': '👨‍🏫',
        'email': 'khorton@nyit.edu',
        'articles_written': ['Celebrating 60 Years of The Campus Slate']
    },
    {
        'id': 'mia-mancia',
        'name': 'Mia Mancia',
        'role': 'Staff Writer',
        'bio': 'Mia is a dedicated writer who covers campus life and student experiences. She is passionate about sharing the stories of first-generation students and helping others feel seen and heard.',
        'major': 'Communication Arts',
        'year': 'Sophomore',
        'image': '✍️',
        'email': 'mmancia@nyit.edu',
        'articles_written': ['The First Generation Student Experience', 'Latinx Heritage Month']
    },
    {
        'id': 'camille-floyd',
        'name': 'Camille Floyd',
        'role': 'Staff Writer',
        'bio': 'Camille joined The Campus Slate with a passion for storytelling and community engagement. She covers a wide range of topics from campus events to student profiles.',
        'major': 'English',
        'year': 'Junior',
        'image': '📝',
        'email': 'cfloyd@nyit.edu',
        'articles_written': ['Campus Voices: Student Spotlight']
    },
    {
        'id': 'daniel-galvin-gusmano',
        'name': 'Daniel Galvin Gusmano',
        'role': 'Staff Writer',
        'bio': 'Daniel is a science writer who covers research and innovation at NYIT. He has a talent for making complex topics accessible and engaging for all readers.',
        'major': 'Biology',
        'year': 'Senior',
        'image': '🔬',
        'email': 'dgusmano@nyit.edu',
        'articles_written': ['The First Annual Biomedical Data Science Center Retreat', '58th Annual MACUB Conference']
    }
]

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

def upload_to_supabase(file, folder='articles'):
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