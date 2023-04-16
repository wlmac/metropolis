# API v3

**Note** All endpoints return JSON notwithstanding exceptions.

**Note** use the Last-Modified header to determine if you should receive content. (conditional requests will not be implemented)

**Base URL**: `https://maclyonsden.com/api`

## Get Feeds
`GET v3/feeds`

**Cache Until**: 24 hours after last fetch

**Returns** a list of the IDs of the organizations to be used as feeds.

**Example**:
```json
[1, 8]
```

## Get Staff

- `GET v3/staff`

**Cache Until**: 24 hours after the last fetch

**Returns** a list of all `Staff`.

## Get Terms

- `GET terms`

**Cache Until**: 24 hours after last fetch
**Note** has `Last-Modified` header.

**Returns** a list of all `Term`s.

## Objects

**Base URL**: `v3/obj/<type>`

**Cache Until**: changes are detected (via the changes endpoint, which should be fetched when data is requested from the user of the library)

For `organization`:

**Returns**: The results sorted by `member count` in *descending* order 

## Get Objects

- `GET /`

**Note** has `Last-Modified` header.

For `event`:

**Returns** list of `{ name, time, organization } ` of `event`.
**Note** use Single to get details.

Allows additional query params `start` and `end` of the format `2006-02-01` (following Go's time format).
Both dates are in AoE time, and the start date is moved to the previous day.

For `flatpage` and `user`:
Cannot be used.

For `Flatpage, User, Organization, Exhibit, BlogPost`:
You can pass a lookup query param with the format `?lookup=<field>` to change how the results are filtered. (e.g. `?lookup=username` if you want to filter by username instead of ID for `User`) Must be an exact match.

### Query

`shrink_last_modified_before`ts modified before supplied time will just have a pk in place of the object.

Pagination (`limit` and `offset`; both **mandatory**): control what data to return.
**Note** using one of `limit` and `offset` causes undefined behaviour.
**Note**
`limit` is the maximum number of items to return.
`offset` is the starting position of the items to return.
See [docs](https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination) for details.

the result will be this format:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/objects.json
type: object
properties:
  count: { type: integer }
  next: { type: string, format: url }
  previous: { type: string, format: url }
  results: { type: array, items: object_specific_type }
```

Example:
```json
{
    "count": 1023,
    "next": "https://maclyonsden.com/api/v3/events?limit=100&offset=500",
    "previous": "https://maclyonsden.com/api/v3/events?limit=100&offset=300",
    "results": [ … ]
}
```

## Create Object
`POST new`

## (Single) Object

- `GET retrieve/<id>`
- `PUT single/<id>`
- `PATCH single/<id>`
- `DELETE single/<id>`

**Note** has `Last-Modified` header.

**Note**. Query params (e.g. `username`) can be added as a disjunctive filter.
          Also, `0` as `<id>` makes the server ignore `0` when retrieving the object.

### For `flatpage`

**Note** `id` is the slug (percent-encoded).

**Returns** title then content separated by `\n`, such as:
```
This is the title blah in plain text
This is the *content* in CommonMark!

No emojis :blobsadrain:.
```

**Success** returns a 2xx code. 

## Error
Errors are returned with their corresponding fields.

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/errors.json
type: object
required: [ properties ]
properties:
  errors:
    type: array
    minLen: 1
    items:
      type: object
      required: [ for, description ]
      properties:
        for:
          type: string
          description: The JSONPath of the field this error was triggered by.
        description:
          type: string
```

## Announcement
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/announcement.json
type: object
properties:
  id: { type: integer }
  created_date: { type: string, format: date-time }
  last_modified_date: { type: string, format: date-time }
  show_after: { type: string, format: date-time }
  title: { type: string }
  body: { type: string }
  is_public: { type: boolean }
  status: { type: string, enum: [ "d", "p", "a", "r" ] }
  rejection_reason: { type: string }
  author: { type: integer }
  organization: { type: integer }
  supervisor: { type: integer | null }
  tags: { type: array, items: integer }
  likes: { type: integer }
  comments: 
    type: object
    properties:
      id: { type: integer }     
      has_children: { type: boolean }
      body: { type: string }
      author: { type: integer | null }
      likes: { type: integer }
```

## Blog Post
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/blog-post.json
type: object
properties:
  id: { type: integer }
  slug: { type: string }
  title: { type: string }
  body: { type: string }
  author: { type: integer }
  views: { type: integer }
  created_date: { type: string, format: date-time }
  last_modified_date: { type: string, format: date-time }
  featured_image: { type: string, format: url }
  featured_image_description: { type: string }
  is_published: { type: boolean }
  tags: { type: array, items: integer }
  likes: { type: integer }
  comments: 
    type: object
    properties:
      id: { type: integer }     
      has_children: { type: boolean }
      body: { type: string }
      author: { type: integer | null }
      likes: { type: integer }
```

## Exhibit
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/exhibit.json
type: object
properties:
  id: { type: integer }
  slug: { type: string }
  title: { type: string }
  author: { type: integer }
  created_date: { type: string, format: date-time }
  last_modified_date: { type: string, format: date-time }
  content: { type: string, format: url }
  content_description: { type: string }
  is_published: { type: boolean }
  tags: { type: array, items: integer }
  likes: { type: integer }
  comments:
    type: object
    properties:
      id: { type: integer }
      has_children: { type: boolean }
      body: { type: string }
      author: { type: integer | null }
      likes: { type: integer }
```

## Event
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/event.json
type: object
properties:
  name: { type: string }
  description: { type: string }
  term: { type: integer }
  organization: { type: integer }
  time:
    type: object
    properties:
      start: { type: string, format: date-time }
      end: { type: string, format: date-time }
  scheduleFormat: { type: integer }
  instructional: { type: integer }
  is_public: { type: boolean }
  should_announce: { type: boolean }

  tags: { type: array, items: integer }
```

## Flatpage

`url` can be used for the lookup query string to filter by url path (e.g. `GET /api/v3/obj/flatpage/retrieve//hello/?lookup=url`).

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/flatpage.json
type: object
properties:
  slug: { type: string }
  content: { type: string }
```

## User

`username` can be used for the lookup query string to filter by username.

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/user.json
type: object
properties:
  id: { type: integer }
  username: { type: string }
  password: { type: string } # write-only
  first_name: { type: string }
  last_name: { type: string }
  bio: { type: string }
  timezone: { type: string }
  graduatingYear: { type: integer }
  organizations: { type: array, items: { type: integer } }
  following: { type: array, items: { type: integer } }
  gravatar_url: { type: string, format: url }
  saved_blogs: { type: array, items: { type: integer } }
  saved_announcements: { type: array, items: { type: integer } }
  is_teacher: { type: boolean }
```


## Organization

`slug` can be used for the lookup query string to filter by slug


```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/organization.json
type: object
properties:
  id: { type: integer }
  owner: { type: integer }
  supervisors: { type: array, items: { type: integer } }
  execs: { type: array, items: { type: integer } }
  members: { type: array, items: { type: integer } }
  name: { type: string }
  bio: { type: string }
  extra_content: { type: string }
  slug: { type: string }
  registered_date: { type: string, format: date-time }
  show_members: { type: boolean }
  is_active: { type: boolean }
  is_open: { type: boolean }
  applications_open: { type: boolean }
  tags: { type: array, items: { type: integer } }
  banner: { type: string }
  icon: { type: string }
  links: { type: array, items: { type: string } }
```

## Comment
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/comment.json
type: object
properties:
  id: { type: integer }
  author: { type: integer | null }
  content_type: { type: integer }
  object_id: { type: integer }
  body: { type: string | null }
  created_at: { type: string | null }
  likes: { type: integer }
  edited: { type: boolean }
  children: 
    type: array
    items:
      type: object
      properties:
        id: { type: integer }     
        has_children: { type: boolean }
        body: { type: string }
        author: { type: integer | null }
        likes: { type: integer }
```

## Tag
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/tag.json
type: object
properties:
  id: { type: integer }
  name: { type: string }
  color: { type: string }
```

## Banners
`GET v3/banners`

**Cache Until**: 600 seconds after last fetch

**Returns** upcoming and current banner(s).

TODO(nyiyui): fix docs per implementation (sus)

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/banners.json
type: object
properties:
  current:
    type: array
    items:
      type: object
      properties:
        content: { type: string }
  upcoming:
    type: array
    items:
      type: object
      properties:
        content: { type: string }
```

## Expo Notifications

Do `OPTIONS v3/notif/token` for docs.

