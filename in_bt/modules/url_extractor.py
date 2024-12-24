def generate_urls(base_url, start_id, num_stocks):
    """
    Generates a list of URLs by incrementing the stock ID.
    """
    try:
        urls = [f"{base_url}{start_id + i}" for i in range(num_stocks)]
        return urls
    except Exception as e:
        raise ValueError(f"Error generating URLs: {e}")
