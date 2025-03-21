from flask import  jsonify, request
from flask_cors import CORS
from main import db, bcrypt,app, create_access_token ,api
from main.model import  User, ProgrammingSkill, WorkExperience, Education, Certification, Project, BlogPost
from flask_jwt_extended import create_access_token, current_user, jwt_required,get_jwt_identity, decode_token, get_jwt
from flask_restx import Api, Resource, ValidationError, fields
from marshmallow import Schema, ValidationError, fields as ma_fields

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}) 

# Marshmallow Schemas for Validation
class UserSchema(Schema):
    username = ma_fields.Str(required=True)
    email = ma_fields.Email(required=True)
    password = ma_fields.Str(required=True, load_only=True)

user_schema = UserSchema()

# Define API Models for Swagger

# Define API Models for Swagger
auth_model = api.model('Auth', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

skill_model = api.model('ProgrammingSkill', {
    'name': fields.String(required=True, description='Skill name'),
    'level': fields.String(required=True, description='Skill level'),
    'category': fields.String(required=True, description='Skill category')
})

work_experience_model = api.model('WorkExperience', {
    'title': fields.String(required=True, description='Job title'),
    'company': fields.String(required=True, description='Company name'),
    'location': fields.String(required=True, description='Location'),
    'date': fields.String(required=True, description='Employment period'),
    'description': fields.String(required=True, description='Job description')
})

project_model = api.model('Project', {
    'title': fields.String(required=True, description='Project title'),
    'description': fields.String(required=True, description='Project description'),
    'technologies': fields.List(fields.String, required=True, description='Technologies used'),
    'category': fields.String(required=True, description='Project category')
})

education_model = api.model('Education', {
    'degree': fields.String(required=True, description='Degree name'),
    'institution': fields.String(required=True, description='Institution name'),
    'period': fields.String(required=True, description='Study period'),
    'location': fields.String(required=True, description='Location'),
    'gpa': fields.Float(description='GPA (optional)'),
    'description': fields.String(description='Additional details (optional)')
})

certification_model = api.model('Certification', {
    'name': fields.String(required=True, description='Certification name'),
    'issuer': fields.String(required=True, description='Issued by'),
    'date': fields.String(required=True, description='Issued date'),
    'expiry': fields.String(description='Expiration date (optional)'),
    'credential_id': fields.String(description='Credential ID (optional)')
})

blogpost_model = api.model('BlogPost', {
    'title': fields.String(required=True, description='Blog post title'),
    'content': fields.String(required=True, description='Blog content'),
    'date': fields.String(required=True, description='Publication date'),
    'category': fields.String(required=True, description='Category'),
    'tags': fields.List(fields.String, description='Tags (optional)'),
    'read_time': fields.String(description='Estimated read time (optional)')
})

# Authentication Endpoints
@api.route('/api/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = request.get_json()
        try:
            user_schema.load(data)  # Validate input
        except ValidationError as err:
            return {'errors': err.messages}, 400
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

@api.route('/api/login')
class Login(Resource):
    @api.expect(auth_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=str(user.id))  # Ensure identity is a string
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

@api.route('/api/check-token')
class CheckToken(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            if not isinstance(current_user, str):
                return {'valid': False, 'error': 'Invalid token format (subject must be a string)'}, 401

            token = request.headers.get('Authorization', None).split()[1]
            decoded_token = decode_token(token)

            return {
                'valid': True,
                'user_id': current_user,
                'exp': decoded_token['exp']
            }, 200
        except Exception as e:
            return {'valid': False, 'error': str(e)}, 401
               
@api.route('/api/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        try:
            token = request.headers.get('Authorization', None)
            if not token:
                return {'message': 'Token missing!'}, 401
            
            print(f"Received Token: {token}")  # Debugging
            
            current_user_id = get_jwt_identity()
            return {'message': 'Access granted!', 'user_id': current_user_id}, 200
        except Exception as e:
            return {'error': str(e)}, 401

# -----------------------
# ✅ Education API
# -----------------------
@api.route('/api/education')
class EducationResource(Resource):
    @jwt_required()
    @api.expect(education_model)
    def post(self):
        """Add an Education record"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_education = Education(
            degree=data['degree'], 
            institution=data['institution'], 
            period=data['period'], 
            location=data['location'], 
            gpa=data.get('gpa'), 
            description=data.get('description', ''), 
            user_id=current_user_id
        )
        db.session.add(new_education)
        db.session.commit()
        return {'message': 'Education record added successfully'}, 201

  
    def get(self):
        """Retrieve all Education records"""
        education_records = Education.query.all()
        return jsonify([{
            'id': edu.id, 
            'degree': edu.degree, 
            'institution': edu.institution, 
            'period': edu.period, 
            'location': edu.location, 
            'gpa': edu.gpa, 
            'description': edu.description
        } for edu in education_records])

    @jwt_required()
    def put(self):
        """Update an existing Education record"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        education = Education.query.get(data['id'])
        if education:
            education.degree = data['degree']
            education.institution = data['institution']
            education.period = data['period']
            education.location = data['location']
            education.gpa = data.get('gpa')
            education.description = data.get('description', '')
            db.session.commit()
            return {'message': 'Education record updated successfully'}
        return {'message': 'Education record not found'}, 404

    @jwt_required()
    def delete(self):
        """Delete an Education record"""
        current_user_id = get_jwt_identity()
        education_id = request.args.get('id')
        education = Education.query.get(education_id)
        if education and education.user_id == current_user_id:
            db.session.delete(education)
            db.session.commit()
            return {'message': 'Education record deleted successfully'}
        return {'message': 'Education record not found'}, 404

# -----------------------
# ✅ Certification API
# -----------------------
@api.route('/api/certifications')
class CertificationResource(Resource):
    @jwt_required()
    @api.expect(certification_model)
    def post(self):
        """Add a Certification"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_certification = Certification(
            name=data['name'], 
            issuer=data['issuer'], 
            date=data['date'], 
            expiry=data.get('expiry'), 
            credential_id=data.get('credential_id'), 
            user_id=current_user_id
        )
        db.session.add(new_certification)
        db.session.commit()
        return {'message': 'Certification added successfully'}, 201

    def get(self):
        """Retrieve all Certifications"""
        
        certifications = Certification.query.all()
        return jsonify([{
            'id': cert.id, 
            'name': cert.name, 
            'issuer': cert.issuer, 
            'date': cert.date, 
            'expiry': cert.expiry, 
            'credential_id': cert.credential_id
        } for cert in certifications])

    @jwt_required()
    def put(self):
        """Update an existing Certification"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        certification = Certification.query.get(data['id'])
        if certification:
            certification.name = data['name']
            certification.issuer = data['issuer']
            certification.date = data['date']
            certification.expiry = data.get('expiry')
            certification.credential_id = data.get('credential_id')
            db.session.commit()
            return {'message': 'Certification updated successfully'}
        return {'message': 'Certification not found'}, 404

    @jwt_required()
    def delete(self):
        """Delete a Certification"""
        current_user_id = get_jwt_identity()
        cert_id = request.args.get('id')
        certification = Certification.query.get(cert_id)
        if certification and certification.user_id == current_user_id:
            db.session.delete(certification)
            db.session.commit()
            return {'message': 'Certification deleted successfully'}
        return {'message': 'Certification not found'}, 404

# -----------------------
@api.route('/api/blogposts')
class BlogPostResource(Resource):
    @jwt_required()
    @api.expect(blogpost_model)
    def post(self):
        """Add a Blog Post"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_blogpost = BlogPost(
              title=data['title'],
              content=data['content'],
              date=data['date'],
              category=data.get('category', "Uncategorized"),
              tags=data.get('tags', ""),
              read_time=data.get('read_time', "5 min read"),
              image=data.get('image', ""),
              author_name=data.get('author_name', "Unknown Author"),
              author_avatar=data.get('author_avatar', ""),
              featured=data.get('featured', False),
              views=data.get('views', 0),
              likes=data.get('likes', 0),
              comments=data.get('comments', 0),
              user_id=current_user_id
        )
        db.session.add(new_blogpost)
        db.session.commit()
        return {'message': 'Blog post added successfully'}, 201

 
    def get(self):
        """Get all Blog Posts for the authenticated user"""
        posts = BlogPost.query.all()
        return jsonify([
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'date': post.date,
                'category': post.category,
                'tags': post.tags,
                'read_time': post.read_time,
                'image': post.image,
                'author_name': post.author_name,
                'author_avatar': post.author_avatar,
                'featured': post.featured,
                'views': post.views,
                'likes': post.likes,
                'comments': post.comments
            } for post in posts
        ])

    @jwt_required()
    @api.expect(blogpost_model)
    def put(self):
        """Update an existing Blog Post"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        post = BlogPost.query.filter_by(id=data['id']).first()
        
        if not post:
            return {'message': 'Blog post not found or unauthorized'}, 404

        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.date = data.get('date', post.date)
        post.category = data.get('category', post.category)
        post.tags = data.get('tags', post.tags)
        post.read_time = data.get('read_time', post.read_time)
        post.image = data.get('image', post.image)
        post.author_name = data.get('author_name', post.author_name)
        post.author_avatar = data.get('author_avatar', post.author_avatar)
        post.featured = data.get('featured', post.featured)
        post.views = data.get('views', post.views)
        post.likes = data.get('likes', post.likes)
        post.comments = data.get('comments', post.comments)

        db.session.commit()
        return {'message': 'Blog post updated successfully'}, 200

# -----------------------
# ✅ Work Experience API
# -----------------------
@api.route('/api/work-experiences')
class WorkExperienceResource(Resource):
    @jwt_required()
    @api.expect(work_experience_model)
    def post(self):
        """Add a Work Experience record"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_experience = WorkExperience(
            title=data['title'], 
            company=data['company'], 
            location=data['location'], 
            date=data['date'], 
            description=data['description'], 
            achievements= data['achievements'],
            icon=data['icon'],
            color=data['color'],
            user_id=current_user_id
        )
        db.session.add(new_experience)
        db.session.commit()
        return {'message': 'Work experience added successfully'}, 201

   
    def get(self):
        """Retrieve all Work Experience records"""
        experiences = WorkExperience.query.all()
        return jsonify([{
            'id': exp.id, 
            'title': exp.title, 
            'company': exp.company, 
            'location': exp.location, 
            'date': exp.date, 
            'description': exp.description,
            'achievements': exp.achievements,
            'icon': exp.icon,
            'color': exp.color
        } for exp in experiences])

    @jwt_required()
    @api.expect(work_experience_model) 
    def put(self):
        """Update a Work Experience record"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        print(data)
        experience = WorkExperience.query.get(data['id'])
        print(experience)
        if experience:
            experience.title = data['title']
            experience.company = data['company']
            experience.location = data['location']
            experience.date = data['date']
            experience.description = data['description']
            experience.achievements = data['achievements']
            experience.icon = data['icon']
            experience.color = data['color']
            
            db.session.commit()
            return {'message': 'Work experience updated successfully'}
        return {'message': 'Work experience not found' + data}, 404

    @jwt_required()
    def delete(self):
        """Delete a Work Experience record"""
        current_user_id = get_jwt_identity()
        experience_id = request.args.get('id')
        experience = WorkExperience.query.get(experience_id)
        if experience and experience.user_id == current_user_id:
            db.session.delete(experience)
            db.session.commit()
            return {'message': 'Work experience deleted successfully'}
        return {'message': 'Work experience not found'}, 404

# -----------------------
# ✅ Projects API
# -----------------------
@api.route('/api/projects')
class ProjectResource(Resource):
    @jwt_required()  # Ensure this is directly above the function definition
    @api.expect(project_model)
    def post(self):
        """Add a Project"""
        jwt_data = get_jwt()  # This will work now
        current_user_id = get_jwt_identity()  # Get the current user's identity
        
        data = request.get_json()

        new_project = Project(
            title=data['title'],
            description=data['description'],
            long_description=data.get('long_description', ""),
            image=data.get('image', ""),
            technologies=",".join(data.get('technologies', [])),  # Convert list to string if needed
            purpose=data.get('purpose', ""),
            approach=data.get('approach', ""),
            contribution=data.get('contribution', ""),
            results=data.get('results', ""),
            github=data.get('github', ""),
            demo=data.get('demo', ""),
            category=data.get('category', "General"),
            features=data.get('features', []),
            screenshots=data.get('screenshots', []),
            tech_stack = data.get('tech_stack', []),
            user_id=current_user_id,  # Assign project to authenticated user
        )

        db.session.add(new_project)
        db.session.commit()

        return {'message': 'Project added successfully'}, 201
    def get(self, project_id=None):
        """Retrieve projects (all or by ID)"""

        if project_id:  # Fetch a single project by ID
            print("Received request for project ID:", project_id)  # Debugging output

            project = Project.query.get(project_id)
            if not project:
                print("Project not found!")  # Debugging output
                return jsonify({'error': 'Project not found'}), 404

            # Return a single project in JSON format
            return jsonify({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'long_description': project.long_description if project.long_description else "",
                'image': project.image,
                'technologies': project.technologies if isinstance(project.technologies, list) else project.technologies.split(',') if project.technologies else [],
                'purpose': project.purpose if project.purpose else "",
                'approach': project.approach if project.approach else "",
                'contribution': project.contribution if project.contribution else "",
                'results': project.results if project.results else "",
                'github': project.github if project.github else "",
                'demo': project.demo if project.demo else "",
                'category': project.category if project.category else "",
                'features': project.features if project.features else [],
                'screenshots': project.screenshots if project.screenshots else [],
                'tech_stack': project.tech_stack ,
                'user_id': project.user_id
            }), 200

        # If no project_id is provided, return ALL projects
        projects = Project.query.all()
        
        return jsonify([
            {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'long_description': project.long_description or "",
                'image': project.image,
                'technologies': (project.technologies if isinstance(project.technologies, list) 
                            else project.technologies.split(',') if project.technologies else []),
                'purpose': project.purpose or "",
                'approach': project.approach or "",
                'contribution': project.contribution or "",
                'results': project.results or "",
                'github': project.github or "",
                'demo': project.demo or "",
                'category': project.category or "",
                'features': project.features or [],
                'screenshots': project.screenshots or [],
                'tech_stack': project.tech_stack or [],
                'user_id': project.user_id
            } for project in projects  # Fixed variable name from 'proj' to 'project'
        ])

# Update route

    @jwt_required()
    @api.expect()
    def put(self):
        """Update a Project"""
        data = request.get_json()
        project = Project.query.get(data['id'])
        if project :
            project.title = data['title']
            project.description = data['description']
            project.image = data.get('image', project.image)
            project.technologies = data.get('technologies', project.technologies)
            project.purpose = data.get('purpose', project.purpose)
            project.approach = data.get('approach', project.approach)
            project.contribution = data.get('contribution', project.contribution)
            project.results = data.get('results', project.results)
            project.github = data.get('github', project.github)
            project.demo = data.get('demo', project.demo)
            project.category = data.get('category', project.category)

            db.session.commit()
            return jsonify({'message': 'Project updated successfully'}), 200
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    @jwt_required()
    def delete(self):
        """Delete a Project"""
        project_id = request.args.get('id')
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully'})
        return jsonify({'message': 'Project not found'}), 404

api.add_resource(ProjectResource, '/api/projects', '/api/projects/<int:project_id>')


# -----------------------
# ✅ Programming Skills API
# -----------------------
@api.route('/api/programming-skills')
class ProgrammingSkillsResource(Resource):
    @jwt_required()
    @api.expect(skill_model)
    def post(self):
        """Add a Programming Skill"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        new_skill = ProgrammingSkill(
            name=data['name'], 
            level=data['level'], 
            category=data['category'], 
            user_id=current_user_id
        )
        db.session.add(new_skill)
        db.session.commit()
        return {'message': 'Programming skill added successfully'}, 201
    def get(self):
        """Retrieve all Programming Skills"""
        skills = ProgrammingSkill.query.all()
        return jsonify([{
            'id': skill.id, 
            'name': skill.name, 
            'level': skill.level, 
            'category': skill.category
        } for skill in skills])

    @jwt_required()
    def put(self):
        """Update a Programming Skill"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        skill = ProgrammingSkill.query.get(data['id'])
        if skill:
            skill.name = data['name']
            skill.level = data['level']
            skill.category = data['category']
            db.session.commit()
            return {'message': 'Programming skill updated successfully'}
        return {'message': 'Programming skill not found'}, 404

    @jwt_required()
    def delete(self):
        """Delete a Programming Skill"""
        current_user_id = get_jwt_identity()
        skill_id = request.args.get('id')
        skill = ProgrammingSkill.query.get(skill_id)
        if skill and skill.user_id == current_user_id:
            db.session.delete(skill)
            db.session.commit()
            return {'message': 'Programming skill deleted successfully'}
        return {'message': 'Programming skill not found'}, 404