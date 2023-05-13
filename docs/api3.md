# API v3

**Note** All endpoints return JSON notwithstanding exceptions.

**Note** use the Last-Modified header to determine if you should receive content. (conditional requests will not be
implemented)

**Base URL**: `https://maclyonsden.com/api`

## Get Feeds

`GET v3/feeds`

**Cache Until**: 24 hours after last fetch

**Returns** a list of the IDs of the organizations to be used as feeds.

**Example**:

```json
[ 1, 8 ]
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

**Cache Until**: changes are detected (via the changes endpoint, which should be fetched when data is requested from the
user of the library)

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
You can pass a lookup query param with the format `?lookup=<field>` to change how the results are filtered. (
e.g. `?lookup=username` if you want to filter by username instead of ID for `User`) Must be an exact match.

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

## (List of) Objects

You can add **Listing Filters** where supported[^1] to narrow down results. You can also chain these filters together
and the system will **OR** them.
e.g. `GET /api/v3/obj/announcement?tags=10&tags=42` will return all announcements that have either the tags _10 **OR**
42_.

__**BUT WAIT!**__ what if you want to find all objects that have **BOTH** tag _10_ **AND** 42? _well_, you can use
the `&search_type` query param which accepts either `AND` or `OR` as its value (default is OR).

###### Examples

- `GET /api/v3/obj/course?position=3&term=2&search_type=AND` will return all are **BOTH** in position _3_ **AND** in
  term _2_.
- `GET /api/v3/obj/announcement?tags=10&tags=42&organization=83&search_type=AND` will return all announcements that have
  **BOTH** tag _10_, _42_ **AND** is from the organization with ID _83_.
- `GET /api/v3/obj/announcement?tags=10&tags=42&search_type=OR` will return all announcements that have **EITHER** tag
  _10_ **OR** _42_.

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

###### When listing

You can use the following filters:

- `tags`: a tag ID to filter by.
- `author`: an author ID to filter by
- `organization`: an organization ID to filter by. (cannot be used with along with itself when using `AND`
  e.g. `?organization=1&organization=2&search_type=AND` is invalid)

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
  author:
    type: object
    properties:
      id: { type: integer }
      username: { type: string }
      first_name: { type: string }
      last_name: { type: string }
  organization:
    type: object
    properties:
      id: { type: integer }
      name: { type: string }
      icon: { type: string, format: url }
  supervisor: { type: integer | null }
  tags:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        color: { type: string }
  likes: { type: integer }
  comments:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        has_children: { type: boolean }
        body: { type: string }
        author:
          type: object | null
          properties:
            id: { type: integer }
            username: { type: string }
            first_name: { type: string }
            last_name: { type: string }
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
  author:
    type: object
    properties:
      id: { type: integer }
      username: { type: string }
      first_name: { type: string }
      last_name: { type: string }
  views: { type: integer }
  created_date: { type: string, format: date-time }
  last_modified_date: { type: string, format: date-time }
  featured_image: { type: string, format: url }
  featured_image_description: { type: string }
  is_published: { type: boolean }
  tags:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        color: { type: string }
  likes: { type: integer }
  comments:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        has_children: { type: boolean }
        body: { type: string }
        author:
          type: object | null
          properties:
            id: { type: integer }
            username: { type: string }
            first_name: { type: string }
            last_name: { type: string }    
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
  author:
    type: object
    properties:
      id: { type: integer }
      username: { type: string }
  created_date: { type: string, format: date-time }
  last_modified_date: { type: string, format: date-time }
  content: { type: string, format: url }
  content_description: { type: string }
  is_published: { type: boolean }
  tags:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        color: { type: string }
  likes: { type: integer }
  comments:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        has_children: { type: boolean }
        body: { type: string }
        author:
          type: object | null
          properties:
            id: { type: integer }
            username: { type: string }
            first_name: { type: string }
            last_name: { type: string }
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
  organization:
    type: object
    properties:
      id: { type: integer }
      name: { type: string }
      icon: { type: string, format: url }
  time:
    type: object
    properties:
      start: { type: string, format: date-time }
      end: { type: string, format: date-time }
  scheduleFormat: { type: integer }
  instructional: { type: integer }
  is_public: { type: boolean }
  should_announce: { type: boolean }
  tags:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        color: { type: string }
```

## Flatpage

`url` can be used for the lookup query string to filter by url path (
e.g. `GET /api/v3/obj/flatpage/retrieve//hello/?lookup=url`).

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
  tags:
    type: array
    items:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        color: { type: string }
  banner: { type: string }
  icon: { type: string, format: url }
  links: { type: array, items: { type: string } }
```

## Comment

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/comment.json
type: object
properties:
  id: { type: integer }
  author:
    type: object | null
    properties:
      id: { type: integer }
      username: { type: string }
  content_type: { type: string }
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
        body: { type: string }
        created_at: { type: string | null }
        has_children: { type: boolean }
        likes: { type: integer }
        author:
          type: object | null
          properties:
            id: { type: integer }
            username: { type: string }
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

## Course

`term` and `position` can be used when listing in the query string to filter by them. (
e.g. `GET /api/v3/obj/course?term=1&position=1`

**NOTE:** `term` is the term *id*, not the term *position*.

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/course.json
type: object
properties:
  id: { type: integer }
  code: { type: string }
  description: { type: string }
  position: { type: integer }
```

## Term

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/term.json
type: object
properties:
  id: { type: integer }
  name: { type: string }
  description: { type: string }
  timetable_format: { type: string }
  start_date: { type: string, format: date-time }
  end_date: { type: string, format: date-time }
  is_frozen: { type: boolean }
```

## Timetable

When viewing:

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/timetable-view.json
type: object
properties:
  term:
    "$ref": /api/v3/schema/term.json
  courses:
    type: array
    items: { "$ref": /api/v3/schema/course.json }

```

When mutating:

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://maclyonsden.com/api/v3/schema/timetable-mutate.json
type: object
properties:
  term: { type: integer }
  courses: { type: array, items: integer }
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

[^1]: check object doc to see supported args. 
