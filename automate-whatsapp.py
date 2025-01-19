import streamlit as st
import pywhatkit as kit
import pyautogui
import datetime
import time

def validate_inputs(phone, message, schedule_time):
    """Validate the phone number, message, and schedule time."""
    if not phone.startswith("+") or not phone[1:].isdigit():
        return "Invalid phone number. Please include the country code (e.g., +1234567890)."

    if not message.strip():
        return "Message cannot be empty."

    try:
        scheduled_hour, scheduled_minute = map(int, schedule_time.split(":"))
        now = datetime.datetime.now()
        scheduled_time = now.replace(hour=scheduled_hour, minute=scheduled_minute, second=0, microsecond=0)
        if scheduled_time < now:
            
            return "Scheduled time cannot be in the past."
    except ValueError:
        return "Invalid time format. Use HH:MM in 24-hour format."

    return None

def send_messages(phone, message, schedule_time):
    """Send 100 repeated WhatsApp messages."""
    scheduled_hour, scheduled_minute = map(int, schedule_time.split(":"))
    for i in range(5):
        try:
            kit.sendwhatmsg(phone, message, scheduled_hour, scheduled_minute + i)
            time.sleep(6)  # Avoid overlapping messages
        except Exception as e:
            return f"Failed to send message {i + 1}. Error: {str(e)}"
    return "All messages sent successfully."

def main():
    st.title("WhatsApp Message Sender")

    # Input fields
    phone = st.text_input("Phone Number (with country code, e.g., +1234567890)")
    message = st.text_area("Message")
    schedule_time = st.text_input("Scheduled Time (HH:MM 24-hour format)")
    
    # Submit button
    if st.button("Submit"):
        # Validate inputs
        validation_error = validate_inputs(phone, message, schedule_time)
        if validation_error:
            st.error(validation_error)
        else:
            st.success("Inputs are valid. Scheduling messages...")
            result = send_messages(phone, message, schedule_time)
            st.info(result)

if __name__ == "__main__":
    main()