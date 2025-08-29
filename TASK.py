from fastapi import FastAPI, HTTPException
import mysql.connector
from passlib.context import CryptContext

app = FastAPI()

# Password hashing setup through passlib library
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# connection string
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Lithishnani555@",
    "database": "mydatabaase"
}

# Create table if not exists on one time
@app.on_event("startup")
def create_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(50),
            password VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Signup (register new user)
@app.post("/signup")
def signup(name: str, email: str, phone: str, password: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    hashed_password = pwd_context.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, hashed_password)
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        cursor.close()
        conn.close()

    return {"message": "User registered successfully!"}

# Login
@app.post("/login")
def login(email: str, password: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password. Please reset your password."
        )

    return {"message": f"Welcome back {user['name']}!"}

# Forgot password (reset)
@app.post("/forgot_password")
def forgot_password(email: str, new_password: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    hashed_password = pwd_context.hash(new_password)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Email not found")

    cursor.execute(
        "UPDATE users SET password=%s WHERE email=%s",
        (hashed_password, email)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Password reset successfully!"}
