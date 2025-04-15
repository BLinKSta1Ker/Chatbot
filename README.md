# Chatbot

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![OpenAI](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)
![VSCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![License](https://img.shields.io/badge/MIT-green?style=for-the-badge)

## 🧠 Chatbot API (Flask + OpenAI + MongoDB + Redis)

A secure, rate-limited, JWT-authenticated chatbot API built with Flask. Supports OpenAI integration for conversational AI, user authentication, admin analytics, and chat history management.

## 🚀 Features

- **User Authentication**
  - Register/Login with JWT
  - Secure password hashing
  - Token blacklisting on logout
  - Rate-limited endpoints

- **Admin Capabilities**
  - View total users and total chat messages
  - List all users
  - Delete specific users

- **AI Chatbot**
  - Integrates with OpenAI’s GPT-4o-mini
  - Maintains short-term context using Redis
  - Persists 30-day chat history in MongoDB

- **Security**
  - JWT-based access control
  - Rate limiting to prevent abuse
  - Input sanitization with `bleach`
  - Token revocation via Redis

## 🗂 Project Structure

```
Chatbot/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── admin.py            # Admin routes
│   ├── auth.py             # Auth routes
│   ├── chatbot.py          # AI chat logic
│   ├── config.py           # Environment/config manager
│   ├── database.py         # Redis and MongoDB connections
│   ├── routes.py           # Chat routes
│   └── utils.py            # Input sanitization
├── models/
│   └── conversation.py     # Chat history handlers
├── .env                    # Environment variables
├── .gitignore              # Ignored files
├── error.log               # Error logging
├── readme.md               # You are here
├── requirements.txt        # Python dependencies
└── run.py                  # Entry point
```

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/BLinKSta1Ker/Chatbot.git
cd chatbot
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install:

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key
MONGO_URI=mongodb://localhost:27017
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET_KEY=supersecret
```

### 4. Run the App

```bash
python run.py
```

The app will be accessible at `http://127.0.0.1:5000/`.

## 📬 API Endpoints

### 🔐 Auth

| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| POST   | `/register`        | Register user             |
| POST   | `/login`           | Login & get JWT           |
| POST   | `/logout`          | Revoke token              |
| POST   | `/register_admin`  | Register an admin user    |

### 🤖 Chat

| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| POST   | `/chat`            | Send a message to chatbot |
| GET    | `/history`         | Get last 30 days of history |

### 👑 Admin

| Method | Endpoint      | Description               |
|--------|---------------|---------------------------|
| GET    | `/admin/stats`| View user/chat stats      |
| GET    | `/admin/users`| List all users            |
| DELETE | `/admin/delete_user` | Delete user by ID     |

> **Note:** All chat and admin routes require a valid JWT token in the `Authorization` header.

## 🛡 Security Measures

- Passwords hashed with Werkzeug
- JWT token expiration and blacklist
- Brute-force protection via `Flask-Limiter`
- Input sanitization using `bleach`

## 🧹 Maintenance

- Chat messages older than 30 days are auto-deleted on startup via `delete_old_messages()`.

## 📖 License

This project is licensed under the MIT License.