# Weather Dashboard App

A full-featured weather dashboard built as part of the **PM Accelerator AI/ML Application Technical Assessment**.

[![Watch the Demo](https://drive.google.com/file/d/1oLPMimzoQZuzGG4diStECF2tXj5D5u1D/view?usp=sharing)

---

## Try the App

You can try the live app here: [Streamlit App Link](https://weatherapp-gzb24msy5smrehvcwddyh3.streamlit.app/)

---

## Features

* Fetch current weather for any city
* Get 5-day weather forecast
* Store weather data in a SQLite database
* Perform CRUD operations on stored weather records
* Interactive charts for temperature and humidity trends
* Info button about PM Accelerator with LinkedIn link
* Footer displaying developer's name
* Supports emojis for weather conditions 🌤️☁️🌧️❄️

---

## Why These Technologies?

**APIs**:

* **OpenWeather API** is used to fetch live, accurate weather data.
* Supports current weather + 5-day forecast.
* Easy to integrate, reliable, and free for this scale of project.

**Database**:

* **SQLite** is used for simplicity, fast deployment, and local persistence.
* Perfect for a small-scale app with CRUD operations.

---

## File Structure

```
weather_app/
│
├── app.py                # Main Streamlit app
├── weather_API.py        # API to fetch current weather
├── forecast_model.py     # API to fetch 5-day weather forecast
├── weather_db.py         # Database queries: insert, read, update, delete
├── init_db.py            # SQLite database initialization
├── utils.py              # Helper functions (e.g., kelvin_to_celsius)
├── requirements.txt      # Required Python libraries
└── .env                  # Stores API keys (ignored in Git)
```

---

## Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/yourusername/weatherapp-bcrj9hr7dulqtjygpx7gpc.git
cd weatherapp-bcrj9hr7dulqtjygpx7gpc
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file and add your OpenWeather API key:

```
OPENWEATHER_API_KEY=your_api_key_here
```

4. Initialize the database:

```bash
python init_db.py
```

5. Run the app:

```bash
streamlit run app.py
```

---

## Developer

**Reem Kassab – AI Engineer Intern**
LinkedIn: [https://www.linkedin.com/in/reem-kassab](www.linkedin.com/in/reem-kassab-33085928a)

---

## License

This project is for educational purposes as part of the PM Accelerator program.
