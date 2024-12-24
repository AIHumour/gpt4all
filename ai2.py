from transformers import AutoTokenizer, AutoModelForCausalLM
import yfinance as yf

# Load the tokenizer and model
model_name = "tiiuae/Falcon3-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="float16"
)

# Ensure `pad_token_id` is set explicitly
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Initialize conversation history with a system prompt
system_prompt = ("The following is a helpful, accurate, and professional conversation with an AI. "
                 "The AI focuses on Indian companies, stock market data, and general knowledge.")
conversation_history = [system_prompt]

# Function to fetch financial data using yfinance
def get_stock_data(stock_ticker):
    try:
        stock = yf.Ticker(stock_ticker)
        info = stock.info
        # Extract relevant financial data
        current_price = info.get("regularMarketPrice", "Data not available")
        previous_close = info.get("previousClose", "Data not available")
        day_high = info.get("dayHigh", "Data not available")
        day_low = info.get("dayLow", "Data not available")
        return current_price, previous_close, day_high, day_low
    except Exception as e:
        print(f"Error fetching data for {stock_ticker}: {e}")
        return None

# Chat interface
print("Chat with the AI! Type 'exit' to end the conversation.")
while True:
    # Get user input
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Check if the input is about stock data
    if "stock" in user_input.lower() or "price" in user_input.lower():
        # Check for specific companies (e.g., BEL)
        if "bel" in user_input.lower():
            stock_ticker = "BEL.NS"  # Bharat Electronics Limited (India) on NSE
        else:
            stock_ticker = None

        if stock_ticker:
            # Fetch stock data
            stock_data = get_stock_data(stock_ticker)
            if stock_data:
                current_price, previous_close, day_high, day_low = stock_data
                # Format and display the response
                ai_response = (f"Bharat Electronics Limited (BEL):\n"
                               f"  Current Price: ₹{current_price} INR\n"
                               f"  Previous Close: ₹{previous_close} INR\n"
                               f"  Day High: ₹{day_high} INR\n"
                               f"  Day Low: ₹{day_low} INR")
            else:
                ai_response = ("Sorry, I could not fetch the stock data for Bharat Electronics Limited "
                               "at the moment. Please try again later.")
        else:
            ai_response = "I currently support fetching stock price data for specific Indian companies like BEL."
        
        # Print AI response and continue the loop
        print(f"AI: {ai_response}")
        continue

    # General conversation logic
    conversation_history.append(f"User: {user_input}")

    # Build the prompt with conversation history
    prompt = "\n".join(conversation_history) + "\nAI:"

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    inputs["attention_mask"] = inputs.input_ids.ne(tokenizer.pad_token_id).int()

    # Generate a response
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs["attention_mask"],
        max_length=300,  # Adjust for response length
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

    # Decode and clean the response
    ai_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    ai_response = ai_response[len(prompt):].strip()

    # Add AI response to conversation history
    conversation_history.append(f"AI: {ai_response}")

    # Print the AI response
    print(f"AI: {ai_response}")
