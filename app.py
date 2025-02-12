from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from datetime import datetime
from utils.image_generator import generate_project_image


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key")

# Initialize database
db.init_app(app)


@app.route('/')
def index():
    from models import Experience, Education, Skill, Project, Certification

    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    education = Education.query.order_by(
        Education.graduation_year.desc()).all()
    skills = Skill.query.order_by(Skill.proficiency.desc()).all()
    projects = Project.query.order_by(Project.created_at.desc()).all()

    # Generate images for projects that don't have one
    for project in projects:
        if not project.image_url:
            image_url = generate_project_image(project.description)
            if image_url:
                project.image_url = image_url
                db.session.commit()

    certifications = Certification.query.order_by(
        Certification.year.desc()).all()

    return render_template('index.html',
                           experiences=experiences,
                           education=education,
                           skills=skills,
                           projects=projects,
                           certifications=certifications)


# API routes for data management
@app.route('/api/experience', methods=['POST'])
def add_experience():
    from models import Experience
    data = request.get_json()

    experience = Experience(
        title=data['title'],
        company=data['company'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
        if data.get('end_date') else None,
        description=data.get('description', ''))

    db.session.add(experience)
    db.session.commit()
    return jsonify({'message': 'Experience added successfully'}), 201


@app.route('/api/skill', methods=['POST'])
def add_skill():
    from models import Skill
    data = request.get_json()

    skill = Skill(name=data['name'], proficiency=data['proficiency'])

    db.session.add(skill)
    db.session.commit()
    return jsonify({'message': 'Skill added successfully'}), 201


with app.app_context():
    import models
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    experiences = [{
        'title':
        'Machine Learning with Python | Lead Score Case Study',
        'company':
        'Coincent',
        'view_url':
        'https://sreekar.tiiny.site/',
        'start_date':
        datetime(2023, 8, 1),
        'end_date':
        datetime(2023, 9, 1),
        'description':
        'Completed internship program in Coincent as a Machine Learning with Python. Participated in an online internship program where, I exclusively performed EDA for the dataset and Identified variables highly related to target variable. The analysis is done for X Education and to find ways to get more industry professionals to join their courses. The basic data provided gave us a lot of information about how the potential customers visit the site, the time they spend there, how they reached the site and the conversion rate. Tools: Pandas, Numpy, Matplotlib, Sklearn, RFE'
    }]

    education = [{
        'degree': 'Bachelor of Technology CSE and AI(ML)',
        'institution': 'Presidency University, Bangalore',
        'graduation_year': '2020 - 2024',
        'score': 'CGPA - 7.67/10'
    }, {
        'degree': 'Higher Secondary Certificate',
        'institution': 'Pinegrove Junior College, Hyderabad',
        'graduation_year': '2018 - 2020',
        'score': 'Score - 89.5%'
    }, {
        'degree': 'Secondary School Leaving Certificate',
        'institution': 'Sri Chaitanya EM School, Andhra Pradesh',
        'graduation_year': '2017 - 2018',
        'score': 'CGPA - 9.8/10'
    }]

    skills = [{
        'name': 'Salesforce Administration',
        'proficiency': 90
    }, {
        'name': 'Salesforce Development',
        'proficiency': 85
    }, {
        'name': 'Java',
        'proficiency': 80
    }, {
        'name': 'SQL',
        'proficiency': 75
    }, {
        'name': 'Web Development',
        'proficiency': 85
    }, {
        'name': 'AI & Machine Learning',
        'proficiency': 80
    }]

    projects = [{
        'title':
        'Salesforce Administrator & Developer Experience',
        'technologies':
        'Salesforce, Apex, Lightning Web Components (LWC)',
        'description':
        'Developed and managed Salesforce applications using Apex and Lightning Web Components (LWC). Implemented record and object-based data fetching using Apex Object Controller. Configured and customized Salesforce objects, fields, validation rules, workflows, and automation processes. Designed and optimized reports and dashboards for business insights. Integrated third-party applications and automated data processing using REST API. Ensured system performance optimization and resolved user issues efficiently.',
        'link':
        'https://sgts-b0-dev-ed.develop.lightning.force.com/lightning/n/Getig_Technology'
        '#',
        'image_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__'
    }, {
        'title':
        'Salesforce | Recruitment Management App',
        'technologies':
        'Salesforce, Apex, Lightning Components',
        'description':
        'Developed a Salesforce recruitment management app including custom objects, workflows, and Lightning Components to streamline the hiring process and enhance efficiency. Integrated third-party APIs and automated job postings and candidate tracking while designing dynamic reports and dashboards for real-time recruitment metrics and performance insights.',
        'link':
        'https://sgts-b0-dev-ed.develop.lightning.force.com/lightning/page/home'
        '#',
        'image_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__'
    }, {
        'title':
        'Web Application | Denafy',
        'technologies':
        'HTML, CSS, JavaScript',
        'description':
        'Created a dynamic Pet website that helps customers to log in their credentials and find their selective favourite song based on criteria. Used HTML, CSS, JavaScript to build the web application, worked as a team lead in this project. Included new features to add more like dogs in cart.',
        'link':
        'https://github.com/sreekar-2002/Web-Application-Denafy'
        '#',
        'image_url':
        'https://3iology.com/dist/assets/img/webapplication.png'
    }, {
        'title':
        'Deep Learning with Application | Classification of Arrhythmia',
        'technologies':
        'Deep Learning, ECG, Python',
        'description':
        'Created a website to get the patient history by using Deep Learning with 2-D ECG Spectral Image Representation falls within the intersection of healthcare, cardiology and artificial intelligence(AI). Developed a user-interactive application to diagnose diseases using spectral image input. Published a paper on Deep Learning-Based Arrhythmia Classification in the International Research Journal of Modernization in Engineering Technology and Science (IRJMETS).',
        'link':
        'https://github.com/sreekar-2002/Deep-Learning-with-Application-Classification-of-Arrhythmia',
        'image_url':
        'https://www.claysys.com/app/uploads/2023/02/Deep-Learning-Applications.png'
    }]

    certifications = [{
        'name':
        'Salesforce Administrator',
        'issuer':
        'Salesforce',
        'year':
        2024,
        'logo_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__',
        'view_url':
        "https://drive.google.com/file/d/1TdjzaWeDsHJLI2Kyr8MwlbIrVxK0l7mS/view?usp=drivesdk"
    }, {
        'name':
        'Salesforce Platform Developer 1',
        'issuer':
        'Salesforce',
        'year':
        2024,
        'logo_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__',
        "view_url":
        "https://drive.google.com/file/d/1zmPT9AMhb2WeON1xfbmz1KlYAsbO_8E9/view?usp=drivesdk "
    }, {
        'name':
        'Salesforce AI Specialist',
        'issuer':
        'Salesforce',
        'year':
        2024,
        'logo_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__',
        "view_url":
        "https://drive.google.com/file/d/1uCWWNJeWFiGGkTkUeJfh1GBeLs1TPfT-/view?usp=drivesdk"
    }, {
        'name':
        'Salesforce AI Associate',
        'issuer':
        'Salesforce',
        'year':
        2024,
        'logo_url':
        'https://media-hosting.imagekit.io//7dec42b1c6e04684/Salesforce Logo.jpg?Expires=1833878650&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=Gw33CEwQgrku7ddhyHozT0fRaJ1NugQRJRumF4mVt6ImdkbFXtM-9ky4v~MY3loxi~UjQlVtjmMuxtpmYLRrzcChnqR76Y8iHDHZpt1cYmqXAdumdWQmpVFP7UURC7O-KHzIiXvpmu0SubRicQDyb5p-Y45v1xh-yCjQlD7XG9fbOBdxUrTSYg8wSK1OH4sn79YbcyxgN~2t1ezON221icxzyOiY-O4~RI~fymmmHAI8Jom006qsA7zTU3Dy1-KWKL2H4VC-PcG7PfJ5pGoNkzZx3lrB5dG2kHYoxVdCFjKPClMuEwNGgyC3JQipqc29cyJUZZE80OUK3JhFpNetQw__',
        "view_url":
        "https://drive.google.com/file/d/13QYuOjOgER0i8HPRahXzBb28ggH5kJQf/view?usp=drivesdk"
    }, {
        'name':
        'Web Developer',
        'issuer':
        'Synergy',
        'year':
        2024,
        'logo_url':
        'https://cdn-icons-png.flaticon.com/512/1336/1336494.png',
        "view_url":
        "https://drive.google.com/file/d/1N3KyBjDlilthYUJU2Yg7PgUzR_VemXwP/view?usp=drivesdk "
    }, {
        'name':
        'Machine Learning with Python',
        'issuer':
        'Coincent',
        'year':
        2023,
        'logo_url':
        'https://cdn-icons-png.flaticon.com/512/2103/2103832.png',
        "view_url":
        "https://drive.google.com/file/d/1sGXPVmNErmCYX4azKj0A1ZH0_dnsJdUU/view?usp=drivesdk"
    }]

    return render_template('index.html',
                           experiences=experiences,
                           education=education,
                           skills=skills,
                           projects=projects,
                           certifications=certifications)
