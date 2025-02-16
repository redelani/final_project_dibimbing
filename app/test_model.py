from model import predict_sentiment  # Adjust path if needed

try:
    # Test with a positive review
    sentiment = predict_sentiment("Hasil dari face wash ini bagus banget, aku sangat suka, bersih sekali")
    print(f"Positive review: {sentiment}")

    # Test with a negative review
    sentiment = predict_sentiment("face wash jelek sekali, muka ku jerawatan parah")
    print(f"Negative review: {sentiment}")

    # Add more test cases as needed...

except Exception as e:
    print(f"Error during testing: {e}")