# KrushiPravah

KrushiPravah is a web application that provides agricultural price predictions and market trends for various vegetables. The application helps farmers and traders make informed decisions by analyzing historical price data and providing future price predictions.

## Features

- **Price Predictions**: Get future price predictions for various vegetables
- **Price Trends**: View historical price trends and patterns
- **Trending Vegetables**: See which vegetables are experiencing significant price changes
- **Interactive Charts**: Visual representation of price data and trends

## Uses

- **Farmers**: Make informed decisions about which crops to grow based on predicted prices
- **Traders**: Plan their trading strategies using historical and predicted price trends
- **Market Analysts**: Study market patterns and price fluctuations
- **Agricultural Businesses**: Make data-driven decisions for crop planning and inventory management

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Environment**: Uses environment variables for configuration

## Project Structure

```
KrushiPravah/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── static/            # Static files (CSS, JS, images)
└── templates/         # HTML templates
```

## API Endpoints

- `/` - Home page with trending vegetables
- `/price-prediction` - Price prediction page
- `/price-trends` - Historical price trends
- `/get_prediction` - API endpoint for price predictions
- `/get_price_trends` - API endpoint for price trend data


