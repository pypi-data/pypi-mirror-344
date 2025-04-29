# postcash
Postcash – A lightweight, async-first notification library for Python and FastAPI. Send Emails (SMTP), Discord, and Telegram messages easily, with pluggable backends.


## Example usage

```python
import asyncio
from postcash import send_email

async def main():
    await send_email(
        to_email="someone@example.com",
        subject="Welcome!",
        body="Thanks for registering!",
    )

asyncio.run(main())
```

