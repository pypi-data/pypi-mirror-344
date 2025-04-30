
# Facebook Messenger Graph API Python SDK ( v22.0 )

A lightweight Python SDK for sending messages (text and image attachments) using the Facebook Graph API along with the Facebook Messenger Send API.

## Installation

```python
pip install -U fb_gapi
```

## 🚀 Features

- **Send Text Messages**: Easily send text messages to users.
- **Send Remote Attachments**: Send remote attachments by URL.
- **Send Local Attachments**: Send local attachments by file path.
- **Get Conversation History**: Fetch the latest conversation history.
- **Error Handling**: The SDK will raise a `MessengerAPIError` when the Facebook API responds with an error.


## 🚀 Usage

### 📦 Import the client
```python
from fb_gapi import MessengerClient
```

### 🔒 Initialize with your Page Access Token 
```python
client = MessengerClient(access_token="YOUR_PAGE_ACCESS_TOKEN")
```

### ✉️ Sending a Text Message
```python
response = client.send_text(recipient_id="USER_PSID", message_text="Hello, user!")
print(response)
```

### 🖼️ Sending an Attachment By URL
```python
image_url = "https://example.com/image.jpg"
response = client.send_remote_attachment(recipient_id="USER_PSID", image_url=image_url)
print(response)
```

### 🖼️ Sending a Local Attachment
```python
file_path = "/path/to/image.jpg"
response = client.send_local_attachment(recipient_id="USER_PSID", file_path=file_path)
print(response)
```

### Get Conversation History (Optional Limit)
```python
response = client.get_chat_history(recipient_id="USER_PSID", limit=5)
print(response)
```

### ⚠️ Error Handling
This SDK will raise a `MessengerAPIError` when the Facebook API responds with an error.

### Example:
```python
from fb_gapi import MessengerAPIError

try:
    client.send_text("invalid_user_id", "Hi!")
except MessengerAPIError as e:
    print(f"GAPI Error: {e}")
```

### Error Output Example:
```
MessengerAPIError (HTTP 400): [OAuthException] Invalid OAuth access token. (code 190)
```

## 📄 Requirements

- **Python 3.6+**


## 🛠️ TODO

- **Improve conversation history limit.**
- **Add support for templates.**
- **Add support for quick replies.**
- **Add support for actions.**
- **Add support for custom buttons.**


## 📃 License

MIT License. Use freely and contribute!
