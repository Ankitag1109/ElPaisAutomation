# 📰 El País Opinion Scraper – Automation Project

## 📌 Project Overview

This project automates the process of extracting articles from the **El País – Opinion section** using Selenium and Python.

It performs the following tasks:

- Opens the El País website
- Navigates to the Opinion section
- Fetches the first 5 articles
- Extracts article titles and content
- Downloads article images
- Translates Spanish titles to English
- Counts repeated words in translated titles
- Runs tests on BrowserStack (Cloud Selenium)

---

## 🛠 Tech Stack

- Python 3.11
- Selenium WebDriver
- Pytest
- BrowserStack
- Requests
- python-dotenv

---

## 📂 Project Structure

```
ElPaisAutomation/
│
├── pages/
│   └── opinion_scraper.py
│
├── utils/
│   ├── translator.py
│   └── word_counter.py
│
├── tests/
│   └── test_el_pais.py
│
├── images/                # Downloaded article images
├── .env                   # BrowserStack credentials (not pushed to GitHub)
├── requirements.txt
└── README.md
```

---

## 🚀 Features Implemented

### 1️⃣ Website Automation

- Opens https://elpais.com
- Navigates to "Opinión" section
- Handles cookie popup

### 2️⃣ Article Scraping

- Extracts first 5 article links
- Visits each article page
- Scrapes:
  - Title
  - Full content
  - Article image

### 3️⃣ Image Download

- Saves images locally in `/images` folder

### 4️⃣ Translation

- Converts Spanish titles to English

### 5️⃣ Word Frequency Counter

- Counts repeated words in translated titles

### 6️⃣ Cloud Execution

- Tests run on:
  - BrowserStack
  - Windows 11
  - Latest Chrome

---

## 🔐 Security Setup (BrowserStack Credentials)

Create a `.env` file in the root folder:

```
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

Install dotenv:

```
pip install python-dotenv
```

---

## 📦 Installation Steps

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/ElPaisAutomation.git
cd ElPaisAutomation
```

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run tests

```
pytest -s
```

---

## 🧪 Test Cases Covered

- Open homepage
- Navigate to Opinion section
- Get first 5 article links
- Scrape article data
- Translate titles
- Count word frequency

---

## 📊 Sample Output

```
First 5 Article Links:
https://elpais.com/opinion/...

Article 1
TITLE: Exceso de ruido
CONTENT LENGTH: 957

Translated Titles:
Excess noise
Díaz Ayuso, MAGA leader
Why is Europe ignoring Serbia?

Word Frequency:
excess : 1
noise : 1
leader : 1
europe : 1
```

---

## ⚠ Notes

- `.env` file is excluded for security
- Images folder auto-created during execution
- Some articles may have different layouts, so content length may vary

---

## 👩‍💻 Author

**Ankita Gaikwad**  
Final Year – Information Technology  
Automation & Web Development Enthusiast

---

## ⭐ Conclusion

This project demonstrates:

- Web automation using Selenium
- Data extraction from real websites
- Cloud test execution with BrowserStack
- Python-based test automation using Pytest
- Clean project structuring and modular coding
