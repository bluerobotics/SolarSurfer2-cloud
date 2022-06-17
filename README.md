# SolarSurfer2-Cloud

## API
### Deploy
Run `python3 SolarSurfer2-Cloud/backend/main.py`

### Server
Currently the backend is running at [http://143.198.58.63:8000](http://143.198.58.63:8000)

### Routes

- `/` (GET)
    - Root route with welcome message
- `/rockblock-messages` (POST/GET)
    - Post Rockblock message or get several messages
- `/payloads` (GET)
    - Get processed payloads
- `/rockblock-message` (GET)
    - Get latest Rockblock message
