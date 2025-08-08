# SkillShareSpace

SkillShareSpace is a minimalist Django-based Question & Answer platform inspired by StackOverflow, designed for small communities.  
It supports user roles, content approval, flagging, and a simple moderation dashboard.

---

## 🚀 Features
1.**User Authentication**
  - Signup, Login, Logout using Django's built-in auth system.
2. **Questions & Answers**
  - Create, edit, delete your own posts.
  - Approval workflow — visible to public only after moderator approval.
  - View counts for questions.
3. **Moderation Dashboard**
  - View unapproved posts.
  - Approve/Dismiss flagged content.
  - Quick moderation actions.
4.**Flagging System**
  - Flag inappropriate questions or answers.
  - Moderators can review and take action.
5.**Search**
  - Simple keyword-based search for questions.
6. **UI**
  - Bootstrap-based minimal design.
  - Conditional moderator controls.


---

## 📸 Screenshots
## 📸 Screenshots

### Home Page 
![Home Page](SS_images/homepage.jpg)

### Not logged in users view
![Not logged in](SS_images/notloggedin.jpg)

### Login Page
![Login Page](SS_images/login_page.jpg)

### Signup Page
![Signup Page](SS_images/signup_page.jpg)

### Moderator Dashboard
![Moderator Dashboard](SS_images/moderator_dashboard.jpg)
![Moderator First Page](SS_images/moderator_firstpage.jpg)
![Approve Question](SS_images/approveqn.jpg)
![Unapproved Posts](SS_images/unapprove.jpg)
![Edit Moderation](SS_images/editm.jpg)
![Delete Moderation](SS_images/delete.jpg)

### Logged-in User View
![Logged-in User](SS_images/loggedin_user.jpg)
![Ask Question](SS_images/ask_qn.jpg)
![New Answer](SS_images/new_ans.jpg)
![User Q&A View](SS_images/user_qn_ans_view.jpg)
![Search](SS_images/search.jpg)
![Edit](SS_images/edit.jpg)
![Delete Question](SS_images/deleteqn.jpg)
![Delete Answer](SS_images/deleteans.jpg)


---

## ⚙️ Setup & Run Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/skillsharespace.git
cd skillsharespace
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations
```bash
python manage.py migrate
```

### 5️⃣ Create a superuser (for moderator role)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the development server
```bash
python manage.py runserver
```

### 7️⃣ Access the application
- Main site: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/admin/

---

## 👥 Roles & Credentials

**Regular User**
- Can create, edit, and delete their own questions/answers.
- Can flag inappropriate content.
- Can search and view only approved content.

**Moderator**
- Can approve or reject questions and answers.
- Can view and dismiss flagged content.
- Has access to the moderation dashboard.

**Example Test Credentials (if you load sample data)**
```
Moderator:  username: moderator1 | password: pass1234
User:       username: user1      | password: pass1234
```

---

## 🛠 Design Decisions

1. **Class-Based Views (CBVs)**
   - All views implemented as CBVs for cleaner, reusable, and organized code.

2. **Approval Workflow**
   - New posts are hidden from public view until approved by a moderator.
   - Implemented via a boolean `approved` field in models.

3. **Flagging System**
   - Built using a generic relation (`content_type` + `object_id`) so both questions and answers can be flagged.

4. **Minimal UI**
   - Used Bootstrap for simplicity, responsiveness, and consistent styling.

5. **Search**
   - Implemented with Django ORM filtering — no external dependencies required.

6. **View Count Tracking**
   - Each time a question is viewed, a counter is incremented in the detail view.

---

## 📜 License
MIT License — feel free to use and modify for your own projects.
