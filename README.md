# 🏠 Tunisia Real Estate Dashboard

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

A modern and interactive dashboard for visualizing and analyzing real estate data in Tunisia, built with Dash and Plotly.

[Features](#-features) •
[Technologies](#%EF%B8%8F-technologies) •
[Installation](#-installation) •
[Usage](#-usage) •
[Structure](#-project-structure) •
[License](#-license)

</div>

## ✨ Features

### Data Analytics
- 📊 Interactive real estate statistics and metrics
- 📈 Distribution charts for listings by governorate
- 💰 Price distribution analysis
- 🏢 Property type analysis (Sale vs. Rent)
- 👥 Publisher insights (Shop vs. Individual)

### Listing Management
- 🆕 Real-time new listings display
- 🔍 Advanced filtering system
- 📅 Date-based filtering
- 💰 Price-based filtering

### User Experience
- 💻 Modern, intuitive interface
- 🎨 Responsive Bootstrap design
- 📱 Mobile-friendly layout
- 🔄 Real-time data updates

## 🛠️ Technologies

### Core
- **Python** - Primary programming language
- **Dash** - Web application framework
- **Plotly** - Data visualization library
- **Pandas** - Data manipulation

### Frontend
- **Dash Bootstrap Components** - UI framework
- **CSS** - Custom styling
- **FontAwesome** - Icons

### Backend
- **FastAPI** - REST API service
- **MongoDB** - Database system

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- MongoDB instance

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/SemerNahdi/Tunisia-Real-Estate-Scraper-Dashboard.git
cd Tunisia-Real-Estate-Scraper-Dashboard
```

2. Create Virtual Environment
```bash
python -m venv .venv
 ```

3. Activate Environment
```bash
.venv\Scripts\activate
 ```

4. Install Dependencies
```bash
pip install -r requirements.txt
 ```

## 🚀 Usage
1. Start Application
```bash
cd app
python -m app.main
 ```

2. Access Dashboard
```plaintext
http://localhost:8050
 ```

## 📁 Project Structure
```plaintext
Tunisia-Real-Estate-Scraper-Dashboard/
├── app/                    # Application Core
│   ├── assets/            # Static Files
│   │   └── styles.css     # Custom Styling
│   ├── config.py          # Configuration
│   ├── main.py           # Entry Point
│   ├── data_processor.py  # Data Processing
│   ├── graphs.py         # Chart Generation
│   ├── layouts.py        # UI Components
│   └── utils.py          # Helper Functions
├── requirements.txt       # Dependencies
└── README.md             # Documentation
 ```

## 🔗 Available Routes Route Description /

Dashboard Homepage /new-listings

Recent Properties /price-filter

Price Analysis /date-filter

Date-based Search /all-listings

Complete Inventory
## 📚 Core Dependencies Package Purpose Dash

Web Framework Plotly

Visualizations Pandas

Data Analysis MongoDB

Database
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.