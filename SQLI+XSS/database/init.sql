-- CodeShop Security Lab Database
-- Course Learning Platform

CREATE DATABASE IF NOT EXISTS toybox;
USE toybox;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table (Courses)
-- image_url format: "COLOR|TEXT" e.g. "#667eea,#764ba2|JS"
-- You can replace with actual image URLs like: "https://example.com/course-js.jpg"
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    age_range VARCHAR(20),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    reviewer_name VARCHAR(100),
    review_text TEXT,
    rating INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Users
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin369', 'admin@codeshop.dev', 'admin'),
('instructor', 'instructor369', 'instructor@codeshop.dev', 'moderator'),
('student', 'student369', 'student@example.com', 'user'),
('john_dev', 'john369', 'john@example.com', 'user'),
('sarah_coder', 'sarah369', 'sarah@example.com', 'user');

-- Courses (Products)
-- image_url format: "gradient_start,gradient_end|initials"
INSERT INTO products (name, description, price, category, age_range, image_url) VALUES
('JavaScript Mastery', 'Complete JavaScript course from basics to advanced. Learn ES6+, async/await, and build real projects.', 49.99, 'Frontend', 'Beginner', '#667eea,#764ba2|JS'),
('React Complete Guide', 'Master React, Redux, and Next.js. Build production-ready applications with modern patterns.', 79.99, 'Frontend', 'Intermediate', '#f093fb,#f5576c|RX'),
('Python for AI', 'Learn Python and machine learning fundamentals. Includes TensorFlow and PyTorch basics.', 99.99, 'Backend', 'Advanced', '#4facfe,#00f2fe|PY'),
('Node.js Backend Dev', 'Build scalable APIs with Node.js, Express, and MongoDB. Real-world project included.', 69.99, 'Backend', 'Intermediate', '#43e97b,#38f9d7|ND'),
('Flutter Mobile Apps', 'Create beautiful cross-platform mobile apps with Flutter and Dart programming.', 89.99, 'Mobile', 'Intermediate', '#fa709a,#fee140|FL'),
('React Native Pro', 'Build iOS and Android apps with React Native. Deploy to app stores.', 79.99, 'Mobile', 'Intermediate', '#a18cd1,#fbc2eb|RN'),
('Docker & Kubernetes', 'Master containerization and orchestration. Deploy like a pro.', 59.99, 'Tools', 'Advanced', '#667eea,#764ba2|DK'),
('Git & GitHub Essentials', 'Version control mastery. Collaboration, branching, and CI/CD basics.', 29.99, 'Tools', 'Beginner', '#f5af19,#f12711|GH'),
('TypeScript Deep Dive', 'Advanced TypeScript patterns. Generics, decorators, and type utilities.', 49.99, 'Frontend', 'Advanced', '#3494e6,#ec6ead|TS'),
('SQL & Database Design', 'Relational databases, SQL mastery, and database optimization techniques.', 39.99, 'Backend', 'Beginner', '#11998e,#38ef7d|DB'),
('Vue.js Essentials', 'Learn Vue 3, Composition API, and Vuex. Build reactive web applications.', 59.99, 'Frontend', 'Beginner', '#00b09b,#96c93d|VU'),
('AWS Cloud Practitioner', 'Cloud computing fundamentals. Prepare for AWS certification exam.', 69.99, 'Tools', 'Beginner', '#ff9a9e,#fecfef|AW');

-- Reviews
INSERT INTO reviews (product_id, reviewer_name, review_text, rating) VALUES
(1, 'Mike Chen', 'Excellent course! Finally understood closures and async programming. The project-based approach really works.', 5),
(1, 'Lisa Wang', 'Very comprehensive. Took me from zero to confident in JavaScript. Highly recommend for beginners.', 5),
(2, 'Dev Student', 'Best React course I have taken. The instructor explains complex concepts clearly.', 5),
(3, 'AI Enthusiast', 'Great introduction to ML. Would love more advanced content on neural networks.', 4),
(4, 'Backend Dev', 'Solid Node.js course. The API project was very practical and real-world applicable.', 5),
(5, 'Mobile Maker', 'Flutter is amazing and this course teaches it well. Built my first app in 2 weeks!', 5);
