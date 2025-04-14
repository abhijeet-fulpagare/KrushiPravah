from flask import Flask, render_template, request, jsonify, flash
import mysql.connector
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration - using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Unable to connect to the database', 'danger')
            return render_template('index.html', trending_vegetables=[])
            
        cursor = conn.cursor(dictionary=True)
        
        # Get trending vegetables (vegetables with significant price changes)
        cursor.execute("""
            SELECT 
                Item as name,
                CAST(MAX(`Predicted Max`) AS DECIMAL(10,2)) as price,
                CAST(
                    ((MAX(`Predicted Max`) - MIN(`Predicted Max`)) / MIN(`Predicted Max`) * 100)
                    AS DECIMAL(10,2)
                ) as price_change
            FROM future_predictions
            WHERE Date >= CURDATE()
            AND Item IS NOT NULL
            AND `Predicted Max` IS NOT NULL
            GROUP BY Item
            HAVING COUNT(*) > 1
            ORDER BY ABS(
                ((MAX(`Predicted Max`) - MIN(`Predicted Max`)) / MIN(`Predicted Max`) * 100)
            ) DESC
            LIMIT 6
        """)
        
        trending_vegetables = cursor.fetchall()
        
        # Format the data
        for veg in trending_vegetables:
            veg['name'] = veg['name'].strip()
            veg['price'] = float(veg['price'])
            veg['change'] = float(veg['price_change'])
        
        cursor.close()
        conn.close()
        
        return render_template('index.html', trending_vegetables=trending_vegetables)
        
    except Exception as e:
        print(f"Error in index route: {e}")
        flash(f'An error occurred: {str(e)}', 'danger')
        return render_template('index.html', trending_vegetables=[])

@app.route('/price-prediction')
def price_prediction():
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Unable to connect to the database', 'danger')
            return render_template('price_prediction.html', vegetables=[])
            
        cursor = conn.cursor()
        
        # Get distinct vegetables, handle NULL values
        cursor.execute("""
            SELECT DISTINCT Item 
            FROM future_predictions 
            WHERE Item IS NOT NULL 
            ORDER BY Item
        """)
        
        vegetables = []
        for row in cursor.fetchall():
            if row[0]:  # Only add non-None values
                vegetables.append(row[0])
        
        cursor.close()
        conn.close()
        
        if not vegetables:
            flash('No vegetables found in database', 'warning')
            return render_template('price_prediction.html', vegetables=[])
        
        return render_template('price_prediction.html', vegetables=vegetables)
        
    except Exception as e:
        print(f"Error in price prediction route: {e}")
        flash(f'An error occurred: {str(e)}', 'danger')
        return render_template('price_prediction.html', vegetables=[])

@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    try:
        vegetable = request.form.get('vegetable')
        date_str = request.form.get('date')  # Already in YYYY-MM-DD format
        
        print(f"\n=== New Prediction Request ===")
        print(f"Vegetable: {vegetable}")
        print(f"Input Date: {date_str}")
        
        if not vegetable or not date_str:
            return jsonify({
                'success': False,
                'message': 'Both vegetable and date are required'
            })

        # Validate date format
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # Keep the date in YYYY-MM-DD format
            formatted_date = date_str
            print(f"Using date: {formatted_date}")
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': 'Invalid date format'
            })

        conn = get_db_connection()
        if conn is None:
            return jsonify({
                'success': False,
                'message': 'Database connection failed'
            })
            
        cursor = conn.cursor(dictionary=True)
        
        # Debug query
        print("\n--- Checking database records ---")
        debug_query = """
        SELECT Date, Item, 
               CAST(`Predicted Min` AS CHAR) as min_price,
               CAST(`Predicted Max` AS CHAR) as max_price
        FROM future_predictions 
        WHERE Item = %s
        AND Item IS NOT NULL
        AND Date IS NOT NULL
        LIMIT 5
        """
        cursor.execute(debug_query, (vegetable,))
        debug_results = cursor.fetchall()
        print(f"Sample records for {vegetable}:")
        for record in debug_results:
            print(f"Date: {record['Date']}, "
                  f"Min: {record['min_price']}, "
                  f"Max: {record['max_price']}")
        
        # Main query
        query = """
        SELECT 
            Item,
            Date,
            CAST(`Predicted Min` AS DECIMAL(10,2)) as min_price,
            CAST(`Predicted Max` AS DECIMAL(10,2)) as max_price
        FROM future_predictions 
        WHERE Item = %s 
        AND Date = %s
        AND Item IS NOT NULL
        AND Date IS NOT NULL
        AND `Predicted Min` IS NOT NULL
        AND `Predicted Max` IS NOT NULL
        """
        
        cursor.execute(query, (vegetable, formatted_date))
        result = cursor.fetchone()
        
        print(f"Query result: {result}")
        
        if not result:
            # Get available dates
            date_query = """
            SELECT DISTINCT Date
            FROM future_predictions 
            WHERE Item = %s
            AND Item IS NOT NULL
            AND Date IS NOT NULL
            ORDER BY Date
            LIMIT 10
            """
            cursor.execute(date_query, (vegetable,))
            available_dates = []
            for row in cursor.fetchall():
                if row['Date']:  # Only add non-None dates
                    available_dates.append(row['Date'])
            
            cursor.close()
            conn.close()
            
            message = f'No prediction found for {vegetable} on {formatted_date}.'
            if available_dates:
                message += f' Available dates: {", ".join(available_dates)}'
            
            print(f"\nNo result: {message}")
            return jsonify({
                'success': False,
                'message': message
            })
        
        # Format the response
        response_data = {
            'success': True,
            'data': {
                'date': result['Date'],
                'vegetable': result['Item'],
                'min_price': float(result['min_price']) if result['min_price'] else 0.0,
                'max_price': float(result['max_price']) if result['max_price'] else 0.0
            }
        }
        
        cursor.close()
        conn.close()
        
        print(f"\nSending response: {response_data}")
        return jsonify(response_data)
            
    except Exception as e:
        print(f"\nError in get_prediction route: {e}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })

@app.route('/price-trends')
def price_trends():
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all unique vegetables with their codes
        cursor.execute("SELECT DISTINCT `Code No`, Item FROM original ORDER BY Item")
        items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('price_trends.html', items=items)
    except Exception as e:
        print(f"Database Error: {str(e)}")
        flash(f"Error loading vegetables: {str(e)}", "error")
        return render_template('price_trends.html', items=[])

@app.route('/get_price_trends')
def get_price_trends():
    code_no = request.args.get('code_no')
    days = request.args.get('days', 'all')
    
    print(f"\n=== Debug: Price Trends Request ===")
    print(f"Code No: {code_no}")
    print(f"Days: {days}")
    
    if not code_no:
        return jsonify({'success': False, 'message': 'Vegetable code is required'})
    
    try:
        conn = mysql.connector.connect(**db_config)
        if not conn:
            print("Failed to connect to database")
            return jsonify({'success': False, 'message': 'Database connection failed'})
            
        cursor = conn.cursor(dictionary=True)
        
        # First, let's check the table structure
        cursor.execute("DESCRIBE original")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"Column: {col['Field']}, Type: {col['Type']}")
        
        # Debug: Check if vegetable exists and print the exact code_no we're searching for
        cursor.execute("SELECT DISTINCT Item, `Code No` FROM original WHERE `Code No` = %s", (code_no,))
        veg_name = cursor.fetchone()
        print(f"\nVegetable found: {veg_name}")
        
        if not veg_name:
            return jsonify({'success': False, 'message': 'Vegetable not found'})
        
        # Get price data with debug output
        query = """
            SELECT 
                Date,
                CAST(Min AS DECIMAL(10,2)) as min_price,
                CAST(Max AS DECIMAL(10,2)) as max_price
            FROM original 
            WHERE `Code No` = %s
            AND Min IS NOT NULL
            AND Max IS NOT NULL
            AND Date IS NOT NULL
            ORDER BY Date DESC
            LIMIT 100
        """
        
        print(f"\nExecuting query with code_no: {code_no}")
        cursor.execute(query, (code_no,))
        rows = cursor.fetchall()
        print(f"Number of rows found: {len(rows)}")
        
        if not rows:
            # Try a broader query to debug
            debug_query = """
                SELECT COUNT(*) as count 
                FROM original 
                WHERE `Code No` = %s
            """
            cursor.execute(debug_query, (code_no,))
            total_count = cursor.fetchone()['count']
            print(f"\nTotal records for this vegetable: {total_count}")
            
            return jsonify({
                'success': False,
                'message': 'No price data found for this vegetable'
            })
        
        # Debug: Print first few rows
        print("\nSample data:")
        for idx, row in enumerate(rows[:3]):
            print(f"Row {idx + 1}: {row}")
        
        # Prepare clean data arrays (reverse to get ascending order)
        rows.reverse()
        dates = []
        min_prices = []
        max_prices = []
        
        for row in rows:
            try:
                if row['Date'] and row['min_price'] is not None and row['max_price'] is not None:
                    formatted_date = row['Date']  # Date is already text, no strftime needed
                    min_price = float(row['min_price'])
                    max_price = float(row['max_price'])
                    
                    dates.append(formatted_date)
                    min_prices.append(min_price)
                    max_prices.append(max_price)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {str(e)}")
                continue
        
        if not dates or not min_prices or not max_prices:
            print("No valid data points found after processing")
            return jsonify({
                'success': False,
                'message': 'No valid price data found for this vegetable'
            })
        
        # Get the latest values for the current price display
        latest = rows[0]  # First row since we reversed the list
        
        response_data = {
            'code_no': code_no,
            'vegetable_name': veg_name['Item'],
            'current': {
                'min_price': float(latest['min_price']) if latest['min_price'] is not None else 0.0,
                'max_price': float(latest['max_price']) if latest['max_price'] is not None else 0.0
            },
            'dates': dates,
            'min_prices': min_prices,
            'max_prices': max_prices
        }
        
        cursor.close()
        conn.close()
        
        print("\nResponse data:")
        print(f"Number of dates: {len(dates)}")
        print(f"Number of prices: {len(min_prices)}, {len(max_prices)}")
        print(f"Sample dates: {dates[:3]}")
        print(f"Sample min prices: {min_prices[:3]}")
        print(f"Sample max prices: {max_prices[:3]}")
        
        return jsonify({'success': True, 'data': response_data})
        
    except Exception as e:
        print(f"\nAPI Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 