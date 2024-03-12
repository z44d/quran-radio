import pyrogram

app = pyrogram.Client(
    "session_name",
    13251350,
    "66c0eacb36f9979ae6d153f207565cd6",
    in_memory=True
)

app.start()

string_session = app.export_session_string()

app.send_message("me", f"`{string_session}`")

print("\n\nCHECK SAVED MESSAGES")
