import psycopg2
import logging
import json
import re

logger = logging.getLogger(__name__)


def sanitize_value(value):
    """
    Remove invalid characters (like ₹ or commas) from string values.
    """
    if isinstance(value, str):
        # Remove invalid characters
        return re.sub(r'[^\x00-\x7F]+', '', value.replace(',', '').strip())
    return value


def sanitize_json(data):
    """
    Recursively sanitize JSON data by removing invalid characters and
    ensuring values are properly formatted.
    """
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                sanitized[key] = sanitize_json(value)
            else:
                sanitized[key] = sanitize_value(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_json(item) for item in data]
    return sanitize_value(data)


def ensure_stock_summary_table_exists(db_params):
    """
    Ensure the `in_stock_summary` table exists in the database with updated schema.
    """
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS rawdata.in_stock_summary (
        id SERIAL PRIMARY KEY,
        name TEXT,
        sector TEXT,
        volume TEXT,
        current_price TEXT,
        change TEXT,
        percentage_change TEXT,
        summary_data JSONB,
        competitors JSONB,
        performance JSONB,
        performance_details JSONB,
        about JSONB,
        management_team JSONB,
        swot JSONB,
        qvt JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    '''
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                logger.info("Ensured the table `in_stock_summary` exists.")
    except psycopg2.Error as e:
        logger.error(f"Database error ensuring `in_stock_summary`: {e}")
        raise


def save_stock_summary_data(db_params, data):
    """
    Save the scraped stock summary data to the PostgreSQL database, including the new columns.
    """
    ensure_stock_summary_table_exists(db_params)

    insert_query = '''
    INSERT INTO rawdata.in_stock_summary 
    (name, sector, volume, current_price, change, percentage_change, 
    beta, price_to_book, dividend_yield, pe_ratio, eps, market_cap, 
    competitors, performance, performance_details, about, management_team)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Handle single dictionary input
                if isinstance(data, dict):
                    data = [data]  # Convert to a list for uniform processing

                for record in data:
                    # Sanitize the record
                    sanitized_record = sanitize_json(record)

                    # Extract individual summary data fields
                    summary_data = sanitized_record.get("summary_data", {})
                    beta = summary_data.get("beta", "N/A")
                    price_to_book = summary_data.get("price_to_book", "N/A")
                    dividend_yield = summary_data.get("dividend_yield", "N/A")
                    pe_ratio = summary_data.get("pe_ratio", "N/A")
                    eps = summary_data.get("eps", "N/A")
                    market_cap = summary_data.get("market_cap", "N/A")

                    # Execute the query
                    cur.execute(
                        insert_query,
                        (
                            sanitized_record.get("name", "N/A"),
                            sanitized_record.get("sector", "N/A"),
                            sanitized_record.get("volume", "N/A"),
                            sanitized_record.get("current_price", "N/A"),
                            sanitized_record.get("change", "N/A"),
                            sanitized_record.get("percentage_change", "N/A"),
                            beta,
                            price_to_book,
                            dividend_yield,
                            pe_ratio,
                            eps,
                            market_cap,
                            json.dumps(sanitized_record.get("competitors", [])),
                            json.dumps(sanitized_record.get("performance", {})),
                            json.dumps(sanitized_record.get("performance_details", {})),
                            json.dumps(sanitized_record.get("about", {})),
                            json.dumps(sanitized_record.get("management_team", [])),
                        )
                    )
                conn.commit()
                logger.info("Stock summary data saved successfully.")
    except Exception as e:
        logger.error(f"Error saving stock summary data: {e}")
