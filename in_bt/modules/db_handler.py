import psycopg2
import logging

logger = logging.getLogger(__name__)

def ensure_stock_summary_table_exists(db_params):
    """
    Ensure the `in_stock_summary` table exists in the database.
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
        low_today TEXT,
        high_today TEXT,
        low_52_week TEXT,
        high_52_week TEXT,
        beta TEXT,
        price_to_book TEXT,
        dividend_yield TEXT,
        pe_ratio TEXT,
        eps TEXT,
        market_cap TEXT,
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
    Save the scraped stock summary data to the PostgreSQL database.
    """
    ensure_stock_summary_table_exists(db_params)

    insert_query = '''
    INSERT INTO rawdata.in_stock_summary 
    (name, sector, volume, current_price, change, percentage_change, 
    low_today, high_today, low_52_week, high_52_week, beta, 
    price_to_book, dividend_yield, pe_ratio, eps, market_cap)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Handle single dictionary input
                if isinstance(data, dict):
                    data = [data]  # Convert to a list for uniform processing

                for record in data:
                    # Log the record being inserted
                    logger.debug(f"Record being inserted: {record}")

                    cur.execute(
                        insert_query,
                        (
                            record.get("name", "N/A"),
                            record.get("sector", "N/A"),
                            record.get("volume", "N/A"),
                            record.get("current_price", "N/A"),
                            record.get("change", "N/A"),
                            record.get("percentage_change", "N/A"),
                            record.get("low_today", "N/A"),
                            record.get("high_today", "N/A"),
                            record.get("low_52_week", "N/A"),
                            record.get("high_52_week", "N/A"),
                            record.get("Beta", "N/A"),
                            record.get("Price-to-Book (X)*", "N/A"),
                            record.get("Dividend Yield (%)", "N/A"),
                            record.get("Price-to-Earnings (P/E) (X)*", "N/A"),
                            record.get("Earnings Per Share (₹)", "N/A"),
                            record.get("Market Cap (₹ Cr.)*", "N/A"),
                        )
                    )
                conn.commit()
                logger.info("Stock summary data saved successfully.")
    except Exception as e:
        logger.error(f"Error saving stock summary data: {e}")




def ensure_stock_analysis_table_exists(db_params):
    """
    Ensures the in_stock_analysis table exists in the database.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS rawdata.in_stock_analysis (
        id SERIAL PRIMARY KEY,
        stock_name TEXT,
        swot_strength TEXT,
        swot_weakness TEXT,
        swot_opportunity TEXT,
        swot_threat TEXT,
        qvt_quality TEXT,
        qvt_valuation TEXT,
        qvt_technicals TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                logger.info("Ensured the `in_stock_analysis` table exists.")
    except psycopg2.Error as e:
        logger.error(f"Database error ensuring `in_stock_analysis`: {e}")
        raise


def save_stock_analysis_data(db_params, data):
    """
    Saves the scraped stock analysis data to the in_stock_analysis table.
    """
    ensure_stock_analysis_table_exists(db_params)

    insert_query = """
    INSERT INTO rawdata.in_stock_analysis 
    (stock_name, swot_strength, swot_weakness, swot_opportunity, swot_threat, qvt_quality, qvt_valuation, qvt_technicals)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    insert_query,
                    (
                        data.get("stock_name", "N/A"),
                        data.get("swot_strength", "N/A"),
                        data.get("swot_weakness", "N/A"),
                        data.get("swot_opportunity", "N/A"),
                        data.get("swot_threat", "N/A"),
                        data.get("qvt_quality", "N/A"),
                        data.get("qvt_valuation", "N/A"),
                        data.get("qvt_technicals", "N/A"),
                    )
                )
                conn.commit()
                logger.info("Stock analysis data saved successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error saving stock analysis data: {e}")
        raise
