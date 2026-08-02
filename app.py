from flask import Flask, render_template, request, redirect, flash, send_from_directory, session
import datetime
import os
import PyPDF2

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Set upload folder for PDFs
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create static/images folder for article images
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# ===== TEAM PASSWORD =====
TEAM_PASSWORD = "slate2026"  # Change this to your team password!

articles = []

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
        'email': 'skumar@nyit.edu'
    },
    {
        'id': 'inaya-syed',
        'name': 'Inaya Syed',
        'role': 'Managing Editor',
        'bio': 'Inaya is a mechanical engineering student who found her passion in journalism. As Managing Editor, she oversees the editorial process and ensures every article meets the highest standards. She founded the Pre-Dental Society and is committed to helping students find their voice.',
        'major': 'Mechanical Engineering',
        'year': 'Senior',
        'image': '👩‍💻',
        'email': 'isyed@nyit.edu'
    },
    {
        'id': 'kevin-horton',
        'name': 'Prof. Kevin Horton',
        'role': 'Faculty Advisor',
        'bio': 'Professor Horton has been the Faculty Advisor for The Campus Slate since 2024. With over 25 years of experience running The Gold Coast Gazette, he brings a wealth of knowledge and expertise. He is passionate about mentoring young journalists and helping them find their voice.',
        'major': 'Communication Arts',
        'year': 'Faculty',
        'image': '👨‍🏫',
        'email': 'khorton@nyit.edu'
    },
    {
        'id': 'sadia-ferdous',
        'name': 'Sadia Ferdous',
        'role': 'Webmaster/Digital Editor',
        'bio': 'Sadia is a Computer Science student who built this very website! As Webmaster, she manages the digital presence of The Campus Slate and creates the online experience for readers. She is passionate about coding and storytelling.',
        'major': 'Computer Science',
        'year': 'Junior',
        'image': '👩‍💻',
        'email': 'sferdous@nyit.edu'
    },
    {
        'id': 'brayan-crespo',
        'name': 'Brayan Crespo',
        'role': 'Layout & Design Editor',
        'bio': 'Brayan is the creative force behind the visual design of The Campus Slate. He ensures every issue is visually stunning and professionally laid out. His design skills bring the publication to life.',
        'major': 'Graphic Design',
        'year': 'Senior',
        'image': '🎨',
        'email': 'bcrespo@nyit.edu'
    },
    {
        'id': 'ashley-alexander',
        'name': 'Ashley Alexander',
        'role': 'Video Journalism Editor',
        'bio': 'Ashley is a Life Sciences student who brings stories to life through video. As Video Journalism Editor, she creates compelling visual content and manages the Slate\'s YouTube channel. She is passionate about public health education.',
        'major': 'Life Sciences (BS/DO)',
        'year': 'Senior',
        'image': '🎥',
        'email': 'aalexander@nyit.edu'
    },
    {
        'id': 'beste-tatlican',
        'name': 'Beste Tatlican',
        'role': 'Former Editor-in-Chief',
        'bio': 'Beste led The Campus Slate through its rejuvenation as Editor-in-Chief. She was instrumental in bringing the publication back to life and launching its video journalism division. She is now pursuing a career in medicine.',
        'major': 'BS/DO Program',
        'year': 'Alumna',
        'image': '👩‍⚕️',
        'email': 'btatlican@nyit.edu'
    },
    {
        'id': 'mia-mancia',
        'name': 'Mia Mancia',
        'role': 'Staff Writer',
        'bio': 'Mia is a dedicated writer who covers campus life and student experiences. She is passionate about sharing the stories of first-generation students and helping others feel seen and heard.',
        'major': 'Communication Arts',
        'year': 'Sophomore',
        'image': '✍️',
        'email': 'mmancia@nyit.edu'
    },
    {
        'id': 'camille-floyd',
        'name': 'Camille Floyd',
        'role': 'Staff Writer',
        'bio': 'Camille joined The Campus Slate with a passion for storytelling and community engagement. She covers a wide range of topics from campus events to student profiles.',
        'major': 'English',
        'year': 'Junior',
        'image': '📝',
        'email': 'cfloyd@nyit.edu'
    },
    {
        'id': 'daniel-galvin-gusmano',
        'name': 'Daniel Galvin Gusmano',
        'role': 'Staff Writer',
        'bio': 'Daniel is a science writer who covers research and innovation at NYIT. He has a talent for making complex topics accessible and engaging for all readers.',
        'major': 'Biology',
        'year': 'Senior',
        'image': '🔬',
        'email': 'dgusmano@nyit.edu'
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

# ===== ROUTES =====

@app.route("/")
def home():
    return render_template("home.html", articles=articles, datetime=datetime, logged_in=is_logged_in())

@app.route("/about")
def about():
    return render_template("about.html", staff=staff, logged_in=is_logged_in())

@app.route("/sections")
def sections():
    return render_template("sections.html", logged_in=is_logged_in())

@app.route("/archives")
def archives():
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

# ===== LOGIN ROUTES =====

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

# ===== TEAM UPLOAD ROUTES (Protected) =====

@app.route("/team-upload", methods=['GET', 'POST'])
@login_required
def team_upload():
    if request.method == 'POST':
        # Check if it's an article or PDF
        content_type = request.form.get('content_type', 'article')
        
        if content_type == 'article':
            title = request.form['title']
            content = request.form['content']
            author = request.form['author']
            article_date = request.form.get('article_date', datetime.datetime.now().strftime("%Y-%m-%d"))
            section = request.form.get('section', '')
            
            try:
                date_obj = datetime.datetime.strptime(article_date, "%Y-%m-%d")
                display_date = date_obj.strftime("%B %d, %Y")
            except:
                display_date = datetime.datetime.now().strftime("%B %d, %Y")
            
            image_filename = None
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file and image_file.filename != '':
                    if not os.path.exists('static/images'):
                        os.makedirs('static/images')
                    image_filename = f"article_{len(articles)}_{image_file.filename}"
                    image_path = os.path.join('static/images', image_filename)
                    image_file.save(image_path)
            
            article = {
                'title': title,
                'content': content,
                'author': author,
                'date': display_date,
                'section': section,
                'image': image_filename,
                'is_pdf': False
            }
            articles.append(article)
            flash('✅ Article published successfully!')
            
        elif content_type == 'pdf':
            if 'file' not in request.files:
                flash('No file selected')
                return redirect('/team-upload')
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected')
                return redirect('/team-upload')
            
            if file and file.filename.endswith('.pdf'):
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                issue_name = request.form.get('issue_name', filename.replace('.pdf', ''))
                
                article = {
                    'title': f"📄 {issue_name}",
                    'content': 'Click "Read Full Issue" to view the complete PDF.',
                    'author': 'The Campus Slate',
                    'date': datetime.datetime.now().strftime("%B %d, %Y"),
                    'section': 'Archives',
                    'image': None,
                    'is_pdf': True,
                    'pdf_file': filename
                }
                articles.append(article)
                flash(f'✅ Successfully uploaded: {filename}')
            else:
                flash('❌ Please upload a PDF file')
                return redirect('/team-upload')
        
        return redirect('/')
    
    return render_template("team_upload.html", logged_in=is_logged_in())

@app.route("/delete/<int:index>")
@login_required
def delete(index):
    if index < len(articles):
        articles.pop(index)
        flash('🗑️ Article deleted successfully.')
    return redirect('/')

@app.route("/view-pdf/<filename>")
def view_pdf(filename):
    return render_template("view_pdf.html", filename=filename, logged_in=is_logged_in())

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)