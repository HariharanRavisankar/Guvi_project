# Police_log

##Project Overview

**SecureCheck** is a real-time digital logbook system for police check posts. The goal is to replace inefficient manual logging with a centralized PostgreSQL database and a Python-Streamlit dashboard for real-time tracking, analytics, and monitoring of vehicle stops, violations, and officer actions.

---

## Technologies Used

- **Python** (Pandas, SQLAlchemy)
- **PostgreSQL / MySQL**
- **Streamlit** (Dashboard UI)
- **SQL** (Subqueries, Joins, Window Functions)

---

##  Streamlit Dashboard Features

-  Display vehicle logs and violations.
- Filterable search (e.g., by date, driver, violation).
- Real-time visualizations (e.g., peak hours, arrest rates).
  - Predictive insights using Python + SQL queries.

---

##  System Architecture

### Step 1: Python Data Processing
- Handle missing or invalid data.
- Convert and format data for database insertion.

### Step 2: SQL Database Design
- Design normalized schema.
- Insert and query using Python.

### Step 3: Streamlit UI
- Visualize violations, durations, demographics.
- Use SQL joins and window functions for insights.

---

##  SQL Features

- **Joins & Subqueries**
- **Window Functions**
- **Date & Time Extracts**
- **Filtering, Ranking, and Aggregation**

Example Queries:
- Top violations by arrest/search rate
- Violation trends by age and race
- Hourly and monthly stop analysis
- Drug-related stop locations by country
