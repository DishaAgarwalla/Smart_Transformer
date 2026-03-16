from predict import predict_lstm

# Test input
data = {
    "type": "M",
    "air_temp": 300,
    "process_temp": 310,
    "rpm": 1500,
    "torque": 40,
    "tool_wear": 10
}

result = predict_lstm(data)

print("Raw Result:", result)

# If using dict version
if isinstance(result, dict):

    print("Prediction:", result["prediction"])
    print("Confidence:", result["confidence"])

# If using float version
else:

    print("Prediction value:", result)

    if result > 0.5:
        print("Machine Failure Likely ⚠️")
    else:
        print("Machine Healthy ✅")