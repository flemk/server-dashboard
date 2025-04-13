> This project is superseeded by [https://github.com/flemk/homelab-operator](flemk/homelab-operator).
---
# server-dashboard
## Functionality
This Repo provides the following functionality:

1. Show/Create a list of all your servers
2. Wake your Server via wake-on-lan
3. Shutdown your Server
4. Creating a heuristic from the last 30 days when your Server was woken
5. From this heuristic wake your Server before you even need it 

### Dashboard
![Server Dashboard](./src/dashboard.jpg)

### Heuristic displayed as bitmap
![Server Bitmap](./src/bitmap.jpg)

## Installation
```
git clone
```

```python
python manage.py makemigrations dashboard
python manage.py migrate
python manage.py crontab add
python manage.py runserver
```
