from backend.strategy import get_dummy_data, add_indicators, generate_signal, compute_confidence

df = get_dummy_data()
df = add_indicators(df)

signal = generate_signal(df)
confidence = compute_confidence(df)

print("Signal:", signal)
print("Confidence:", confidence, "%")
print(df.tail())
