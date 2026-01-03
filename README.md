<div align="center">

# PeerPals 🎓
**Structured Mentoring. Student-Centric Design.**

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

</div>

---
## 💡 The Problem
Most universities have mentoring programs, but they lack **structure** and fail to account for **student social anxiety**. PeerPals bridges this gap by providing a digital framework that puts student comfort first.

## 🎭 Interaction Paradigms
- **🕵️ Anonymous Mode:** Students can discuss queries freely without disclosing their identity, removing the barrier of overthinking or judgment.
- **🤝 Normal Mode:** Open, transparent discussion for standard academic and professional mentoring.

---

## 🛠️ Tech Stack
* **Frontend:** `React.js` (JavaScript, CSS)
* **Backend:** `Django` (Python)
* **Database:** `MySQL`
* **Authentication:** `JWT` (Stateless Token-based Auth)

---

## 🚀 Key Features

### 🔑 Advanced Access Control
- **Role-Based Dashboards:** Distinct interfaces for **Students**, **Mentors**, and **Admins**.
- **Secure Sessions:** JWT access tokens ensure data privacy across all roles.

### 📅 Session Management
- **Smart Calendar:** Visualized session tracking for both parties.
- **Mentor Autonomy:** Mentors set specific dates to conduct sessions for their assigned students.

### 🛡️ System Guardrails (Rate Limiting)
- **Anti-Spam:** Students cannot make multiple requests simultaneously, they must wait for a mentor’s response.
- **Usage Quotas:** Monthly limits on total sessions to ensure fair resource distribution.

---

## 📥 Installation

### 🖥️ Frontend Setup
```bash
cd frontend
npm install
npm start
```
### ⚙️ Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
👨‍💻 Admin Capabilities
User Management: Onboard new students and faculty mentors.
Oversight: Monitor all booked sessions and their current statuses in real-time.

---

## 🌐 Deployment & Security 

Before moving to a production environment, ensure the following security configurations are met:

### 1. Environment Variables
To keep sensitive data secure, move your database credentials and secret keys out of the source code.

* **Disable Debug Mode:** Set `DEBUG = False` in `settings.py`.
* **Secure Passwords:** Use environment variables for the database password and Secret Key.

**Example `settings.py` update:**
```python
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'peerpals_db',
        'USER': 'admin',
        'PASSWORD': os.environ.get('DB_PASSWORD'), # Retrieved from environment
        'HOST': 'localhost',
        'PORT': '3306',
    }
}