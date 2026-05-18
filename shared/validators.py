def validate_name_surname(name, surname):
    if not name or not surname:
        return "Name and surname cannot be empty."
    if len(name) < 2 or len(surname) < 2:
        return "Name and surname must be at least 2 characters long."
    if not name.isalpha() or not surname.isalpha():
        return "Name and surname can only contain letters."
    return None

def validate_username_phone(username, phone_number):
    if not username or not phone_number:
        return "Username and phone number cannot be empty."
    if len(username) < 2:
        return "Username must be at least 2 characters long."
    if not username.isalnum():
        return "Username can only contain letters and numbers."
    if not phone_number.isdigit() or len(phone_number) < 10:
        return "Phone number must be at least 10 digits long and contain only numbers."
    return None