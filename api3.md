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

## Get User

= `GET v3/user/<id>`

**Cache Until**: 24 hours after last fetch

**Returns**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/user.json
type: object
properties:
  id: { type: integer }
  username: { type: string }
  first_name: { type: string, minLength: 1 }
  last_name: { type: string, minLength: 1 }
  bio: { type: string }
  timezone: { type: string }
  graduating_year: { type: string }
  organizations: { type: array, items: { type: integer } }
  tags_following: { type: array, items: { type: integer } }
```

## Get Terms

- `GET terms`

**Cache Until**: 24 hours after last fetch
**Note** has `Last-Modified` header.

**Returns** a list of all `Term`s.

## Objects

**Base URL**: `v3/obj/<type>`

**Cache Until**: changes are detected (via the changes endpoint, which should be fetched when data is requested from the user of the library)

## Get Objects

- `GET /`

**Note** has `Last-Modified` header.

For `event`:
**Returns** list of `{ name, time, organization } ` of `event`.
**Note** use Single to get details.

For `flatpage` and `user`:
Cannot be used.

### Query

`shrink_last_modified_before`ts modified before supplied time will just have a pk in place of the object.

Pagination (`limit` and `offset`; both **mandatory**): control what data to return.
**Note** using one of `limit` and `offset` causes undefined behaviour.
**Note**
`limit` is the maximum number of items to return.
`offset` is the starting position of the items to return.
See [https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination] for details.

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

### For `flatpage`

**Note** `id` is the slug.

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
  author: { type: integer }
  organization: { type: integer }
  tags: { type: array, items: integer }

  status: { type: string, enum: [ "d", "p", "a", "r" ] }

  supervisor: { type: integer }
  rejectionReason: { type: string }
```

## Blog Post
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/blog-post.json
type: object
properties:
  author: { type: integer }
  organization: { type: integer }
  tags: { type: array, items: integer }

  status: { type: string, enum: [ pending, approved ] }

  featuredImage: { type: string, format: url }
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
  public_: { type: boolean }

  tags: { type: array, items: integer }
```

## Flatpage
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/flatpage.json
type: object
properties:
  slug: { type: string }
  content: { type: string }
```

## User
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/user.json
type: object
properties:
  id: { type: integer }
  slug: { type: string }
  name: { type: string }
  bio: { type: string }
  timezone: { type: string }
  graduatingYear: { type: integer }
  organizations: { type: array, items: { type: integer } }
  following: { type: array, items: { type: integer } }
```


## Organization
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

