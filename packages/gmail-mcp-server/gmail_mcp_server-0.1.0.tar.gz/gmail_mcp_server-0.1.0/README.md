Gmail MCP Server
A Python-based MCP server for integrating Gmail and Google Calendar to summarize emails, send emails, and create calendar events from important emails.
Installation
pip install gmail-mcp-server

Setup (For Testing)

Ensure gcp-oauth.keys.json is in C:\Users\Aniket\.gmail-mcp\ (Windows).
Run the server:gmail-mcp-server



Usage
Use with Claude Desktop:

Summarize emails: Summarize the last 3 emails in my inbox.
Send email: Send an email to example@gmail.com with subject "Test" and body "Hello".
Create calendar event: Create a calendar event for the last important email.

Dependencies

google-api-python-client
google-auth-oauthlib
mcp
schedule

License
MIT
