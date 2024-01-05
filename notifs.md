# Expo Notifications

## Methods
- `PUT /api/v3/notif/token`
- `DELETE /api/v3/notif/token`

JSON object for PUT and DELETE is both of the form:
- `{"expo_push_token": "ExponentPushToken[abc123]", "options": {}}`
- `{"expo_push_token": "abc123", "options": {}}`
(Using `ExponentPushToken[...]` is preferred because then we can eventually remove support for the `...` form.)

The `options` key format is as follows:
```json
{
  "options": {
    "allow": {
      "<notification-category>": <notification-options>
    }
  }
}
```

Example for the `options` key:
```json
{
  "expo_push_token": "...",
  "options": {
    "allow": {
      "event.singleday": {} // daily reminders
      "ann.public": {} // public announcements
      "ann.personal": {} // announcements from tags and organizations user is member of
    }
  }
}
```
