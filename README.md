**# 🏠 Tunisia Real Estate Dashboard**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

A modern and interactive dashboard for visualizing and analyzing real estate data in Tunisia, built with Dash and Plotly.

**## ✨ Features**

**### 1. Data Visualization**

- 📊 Interactive real estate statistics and metrics
- 📈 Distribution charts for listings by governorate
- 💰 Price distribution analysis
- 🏢 Sale vs. Rent distribution visualization
- 👥 Publisher type analysis (Shop vs. Individual)

**### 2. Listings Management**

- 🆕 New listings display with detailed information
- 🔍 Advanced filtering capabilities
- 📱 Responsive design for all devices

**### 3. User Interface**

- 💻 Modern and intuitive dashboard layout
- 🎨 Custom styling with Bootstrap components
- 📱 Mobile-responsive design
- 🔄 Interactive data filtering

**## 🛠️ Technologies Used**

- ***Python****: Core programming language
- ***Dash****: Web framework for building interactive dashboards
- ***Plotly****: Interactive data visualization library
- ***Dash Bootstrap Components****: UI components for modern design
- ***Pandas****: Data manipulation and analysis
- ***FastAPI****: Backend API for data retrieval
- ***MongoDB****: Database for storing real estate data

**## 📦 Installation**

**### Prerequisites**

1. ****Python 3.7+****: Ensure Python is installed on your system

2. ****pip****: Python package manager

3. ****MongoDB****: Running instance for data storage

**### Steps**

1. Clone the repository:

```bash

git clone [REPO_URL]

cd Tunisia-Real-Estate-Scraper-Dashboard

```

2. Create a virtual environment:

```bash

python -m venv .venv

```

3. Activate the virtual environment:

- Windows:

```bash

.venv\Scripts\activate

```

- macOS/Linux:

```bash

source .venv/bin/activate

```

4. Install dependencies:

```bash

pip install -r requirements.txt

```

**## 🚀 Running the Application**

1. Navigate to the project directory

2. Activate the virtual environment (if not already done)

3. Run the application:

```bash

cd app

python main.py

```

4. Access the dashboard in your browser:

```

http://localhost:8050

```

**## 📁 Project Structure**

```

Tunisia-Real-Estate-Scraper-Dashboard/

├── app/

│   ├── main.py              # Application entry point

│   ├── config.py            # Application configuration

│   ├── data_processor.py    # Data processing and analysis

│   └── layouts.py           # Dashboard layout components

├── assets/

│   └── styles.css           # Custom CSS styles

└── requirements.txt         # Project dependencies

```

**## 🔗 Available Pages**

- `/` - Homepage with statistics and new listings
- `/new-listings` - List of new property listings
- `/price-filter` - Price-based filtering and analysis

**## 📚 Main Dependencies**

- [Dash](https://dash.plotly.com/) - Framework for interactive web applications
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) - Bootstrap UI components
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis
- [Plotly](https://plotly.com/) - Interactive visualizations

**## 📄 License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

