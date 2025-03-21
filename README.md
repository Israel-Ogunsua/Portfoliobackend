### **Expected Inputs for Each API Endpoint**

---

## **1️⃣ User Authentication APIs**

### **📌 `POST /api/register` (User Registration)**

**🔹 Expected JSON Input:**

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword123"
}
```

**🔹 Validation Rules:**

- `username` → **Required**, string.
- `email` → **Required**, valid email.
- `password` → **Required**, string (hashed before saving).

---

### **📌 `POST /api/login` (User Login)**

**🔹 Expected JSON Input:**

```json
{
  "email": "johndoe@example.com",
  "password": "securepassword123"
}
```

**🔹 Validation Rules:**

- `email` → **Required**, must exist in the database.
- `password` → **Required**, must match the hashed password.

**🔹 Successful Response:**

```json
{
  "access_token": "JWT-TOKEN-HERE"
}
```

(Use this **JWT token** for protected routes.)

---

## **2️⃣ Programming Skills API**

### **📌 `POST /api/programming-skills` (Add Skill)**

**🔹 Expected JSON Input:**

```json
{
  "name": "Python",
  "level": "Advanced",
  "category": "Backend/AI"
}
```

**🔹 Validation Rules:**

- `name` → **Required**, string.
- `level` → **Required**, options: `Beginner`, `Intermediate`, `Advanced`, `Expert`.
- `category` → **Required**, string (e.g., `Frontend`, `Backend`, `Database`, etc.).

---

## **3️⃣ Work Experience API**

### **📌 `POST /api/work-experiences` (Add Work Experience)**

**🔹 Expected JSON Input:**

```json
{
  "title": "Software Engineer",
  "company": "Google",
  "location": "Remote",
  "date": "2020-06-01 - 2023-08-15",
  "description": "Developed scalable web applications using Python and React."
}
```

**🔹 Validation Rules:**

- `title` → **Required**, string.
- `company` → **Required**, string.
- `location` → **Required**, string.
- `date` → **Required**, valid date range or `Ongoing`.
- `description` → **Required**, string.

---

## **4️⃣ Education API**

### **📌 `POST /api/education` (Add Education)**

**🔹 Expected JSON Input:**

```json
{
  "degree": "B.S in Computer Science",
  "institution": "Harvard University",
  "period": "2018 - 2022",
  "location": "Cambridge, MA",
  "gpa": "3.9"
}
```

**🔹 Validation Rules:**

- `degree` → **Required**, string.
- `institution` → **Required**, string.
- `period` → **Required**, string (e.g., `YYYY - YYYY`).
- `location` → **Required**, string.
- `gpa` → **Optional**, numeric (e.g., `3.5`).

---

## **5️⃣ Certifications API**

### **📌 `POST /api/certifications` (Add Certification)**

**🔹 Expected JSON Input:**

```json
{
  "name": "AWS Solutions Architect",
  "issuer": "Amazon Web Services",
  "date": "2022-03-10",
  "expiry": "2024-03-10",
  "credential_id": "AWS-12345"
}
```

**🔹 Validation Rules:**

- `name` → **Required**, string.
- `issuer` → **Required**, string.
- `date` → **Required**, valid date.
- `expiry` → **Optional**, valid date.
- `credential_id` → **Optional**, string.

---

## **6️⃣ Projects API**

### **📌 `POST /api/projects` (Add Project)**

**🔹 Expected JSON Input:**

```json
{
  "title": "AI-Powered Image Generator",
  "description": "A deep-learning model that generates high-quality images.",
  "image": "https://example.com/image.png",
  "technologies": ["Python", "TensorFlow", "React"],
  "github": "https://github.com/yourrepo",
  "demo": "https://demo.example.com",
  "category": "AI"
}
```

**🔹 Validation Rules:**

- `title` → **Required**, string.
- `description` → **Required**, string.
- `image` → **Optional**, valid URL.
- `technologies` → **Required**, array of strings.
- `github` → **Optional**, valid URL.
- `demo` → **Optional**, valid URL.
- `category` → **Required**, string.

---

## **7️⃣ Blog Posts API**

### **📌 `POST /api/blogposts` (Add Blog Post)**

**🔹 Expected JSON Input:**

```json
{
  "title": " Future of Artificial Intelligence",
  "content": "Artificial Intelligence (AI) is reshaping industries worldwide. From self-driving cars to automated healthcare solutions, AI continues to revolutionize our daily lives...",
  "date": "2025-02-01",
  "category": "Technology",
  "tags": "AI, Machine Learning, Future Tech",
  "read_time": "7 min read",
  "image": "https://example.com/images/ai-future.jpg",
  "author_name": "John Doe",
  "author_avatar": "https://example.com/images/john-avatar.jpg",
  "featured": true,
  "views": 4523,
  "likes": 320,
  "comments": 45
}
```
