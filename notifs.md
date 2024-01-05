# Expo Notifications

## Methods
- `PUT /api/v3/notif/token`
- `DELETE /api/v3/notif/token`

Note how there is no GET method. The idea is the app must keep its notification settings in its local memory (and the site a bit less attack surfcae).

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

| Category Key      | Description                                         | Options |
|-------------------|-----------------------------------------------------|---------|
| `event.singleday` | Daily reminders                                     | None    |
| `ann.public`      | Announcements for everyone                          | None    |
| `ann.personal`    | Announcements from following tags and organizations | None    |

Options are always objects, and new keys may be added in the future (e.g. `{"remind_time": "07:00"}` for `event.singleday`).

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
