def calculate_health(data):
    temperature = data.get("temperature", 0)
    current = data.get("current", 0)
    voltage = data.get("voltage", 0)
    vibration = data.get("vibration", 0)
    humidity = data.get("humidity", 0)
    oil_color = data.get("oil_color", 0)

    health_score = 100 - (
        temperature * 0.2 +
        current * 0.1 +
        vibration * 0.3 +
        humidity * 0.1 +
        oil_color * 0.3
    )

    risk_percentage = 100 - health_score

    if health_score > 70:
        status = "Healthy"
        prediction = "No Immediate Risk"
    elif health_score > 40:
        status = "Warning"
        prediction = "Maintenance Required Soon"
    else:
        status = "Critical"
        prediction = "Immediate Attention Needed"

    return {
        "health_score": round(health_score, 2),
        "risk_percentage": round(risk_percentage, 2),
        "status": status,
        "prediction": prediction
    }