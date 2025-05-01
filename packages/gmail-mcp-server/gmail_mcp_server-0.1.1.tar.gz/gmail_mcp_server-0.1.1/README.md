Gmail MCP Server
Gmail MCP Server is a Python package that integrates Gmail and Google Calendar with Claude Desktop. It allows users to summarize emails, send emails, and automatically create calendar events for important emails using an MCP server.
Features

Summarize recent emails in your Gmail inbox.
Send emails directly from Claude Desktop.
Create Google Calendar events manually or automatically for emails labeled as "important".
Runs as a background server with a 10-minute scheduler for automatic event creation.

Installation
pip install gmail-mcp-server

Setup

Enable Gmail and Google Calendar APIs in Google Cloud Console.
Download credentials.json and place it in ~/.gmail_mcp_server/ (Windows: C:\Users\<Username>\.gmail_mcp_server\).
Install the package and run the server:pip install gmail-mcp-server
gmail-mcp-server



Usage with Claude Desktop
Configure Claude Desktop by adding the following to claude_desktop_config.json (e.g., C:\Users\<Username>\AppData\Roaming\Claude\claude_desktop_config.json):
{
  "mcpServers": {
    "email-mcp-server": {
      "command": "gmail-mcp-server",
      "args": [],
      "cwd": ""
    }
  }
}

Example commands:

Summarize emails: Summarize the last 3 emails in my inbox.
Send email: Send an email to example@gmail.com with subject "Test" and body "Hello".
Create calendar event: Create a calendar event for the last important email.

Automatic Calendar Events

Emails labeled "important" in Gmail are automatically processed every 10 minutes.
A calendar event is created, and the email is tagged with calendar_event_created.

Dependencies

google-api-python-client
google-auth-oauthlib
mcp
schedule

License
MIT
Support
For issues, visit GitHub Issues or email fakeloginpage13@gmail.com.
