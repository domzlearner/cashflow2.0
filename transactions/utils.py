from datetime import datetime, timedelta

def get_month_choices():
    current_date = datetime.now()
    months = []
    for i in range(-12, 12):  # Adjust range as needed
        month_date = current_date + timedelta(days=i * 30)
        value = month_date.strftime("%Y-%m")
        label = month_date.strftime("%B %Y")
        months.append((value, label))
    return months