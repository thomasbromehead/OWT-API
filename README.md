## Create a user to interact with the API
```
curl -H "content-type:application/json" --data '{"username":"tom","password":"password"}' localhost:5000/api/v1/users

{
  "successfully_created_user": {
    "username": "tom"
  }
```
## Get  a token once signed in:
```
curl -u tom:password -i -X GET localhost:5000/api/v1/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 183
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Sat, 19 Jan 2019 19:10:50 GMT

{
  "token": "eyJhbGciOiJIUzUxMiIsImV4cCI6MTU0NzkyNTY1MCwiaWF0IjoxNTQ3OTI1MDUwfQ.eyJpZCI6M30.Balxnb883PkBIESDs-vNtDlF0XIgHupJRldbBN3nd1GLpYbMt9nkgyHKEzVQvoa3qLMP7cGgnldMAhubgnD07Q"
}
```

## Create a contact
```
curl -H "Content-type:application/json" --data '{"contact":{"first_name":"Roy", "last_name":"de la Piedra", "full_name":"Roy de la Piedra", "email": "greatdevs@keeplearning.com"}}' localhost:5000/api/v1/contacts
{
  "contact": {
    "address": null,
    "email": "greatdevs@keeplearning.com",
    "first-name": "Roy",
    "full-name": "Roy de la Piedra",
    "id": 5,
    "last-name": "de la Piedra",
    "mobile": null,
    "skills": []
  }
}
```

## Update a single contact
```
curl --request PUT -H "Content-type:application/json" --data '{"skills":["javascript", "python", "sql"]}' localhost:5000/api/v1/contacts/1
[
  {
    "Message": "Contact updated successfully"
  },
  {
    "address": null,
    "email": "henri@gmail.fr",
    "first-name": "Henri",
    "full-name": "Henri Matthieu Larrié",
    "id": 1,
    "last-name": "Larrié",
    "mobile": null,
    "skills": [
      {
        "id": 2,
        "level": 5,
        "name": "javascript"
      },
      {
        "id": 3,
        "level":4,
        "name": "python"
      },
      {
        "id": 4,
        "level": 4,
        "name": "sql"
      }
    ]
  }
]
```

## List out contacts by using the assigned token
```
curl -u eyJhbGciOiJIUzUxMiIsImV4cCI6MTU0NzkyNTgyOCwiaWF0IjoxNTQ3OTI1MjI4fQ.eyJpZCI6M30.hocLKTjKjVg-kvRkedoU28Mqqv1oZTUjMDSdvqCeRTKtTpzVPJdb9NUjBkvXSNsQkTaoUIOq3eO5CTc-TzoQ8g:blank GET localhost:5000/api/v1/contacts
{
  "contacts": [
    {
      "address": null,
      "email": "henri@gmail.fr",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 1,
      "last-name": "Larrié",
      "mobile": null,
      "skills": [
        {
          "id": 2,
          "level": 5,
          "name": "javascript"
        }
      ]
    },
    {
      "address": null,
      "email": "tom@yahoo.com",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 2,
      "last-name": "Larrié",
      "mobile": null,
      "skills": []
    },
    {
      "address": null,
      "email": "tom@yahoo.com",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 3,
      "last-name": "Larrié",
      "mobile": null,
      "skills": []
    },
    {
      "address": null,
      "email": "tom@yahoo.com",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 4,
      "last-name": "Larrié",
      "mobile": null,
      "skills": []
    }
  ]
}
```

## Create a skill
```
curl -i -H "Content-Type: application/json" -d '{"name":"typescript","level":5}' localhost:5000/api/v1/skills
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 53
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Sat, 19 Jan 2019 18:49:00 GMT

{
  "id": 4,
  "level": 5,
  "name": "typecript"
}
```

## List skills
```
curl localhost:5000/api/v1/skills
{
  "skills": [
    {
      "id": 1,
      "level": 5,
      "name": "jacript"
    },
    {
      "id": 2,
      "level": 5,
      "name": "javascript"
    }
  ]
}
```

## Update a skill
```
curl --request PUT -H "content-type:application/json" --data  '{"name":"typescript"}' localhost:5000/api/v1/skills/1

{
  "skill": {
    "id": 1,
    "level": 5,
    "name": "typescript"
  }
```
## Delete a skill
```
curl --request DELETE localhost:5000/api/v1/skills/1
Typescript was deleted successfully!%

```

## List all people with a certain skill
```
curl localhost:5000/api/v1/skills/python
{
  "contacts_with_these_skills": [
    {
      "address": null,
      "email": "henri@gmail.fr",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 1,
      "last-name": "Larrié",
      "mobile": null,
      "skills": [
        {
          "id": 2,
          "level": 5,
          "name": "javascript"
        },
        {
          "id": 5,
          "level": 5,
          "name": "python"
        }
      ]
    },
    {
      "address": null,
      "email": "tom@yahoo.com",
      "first-name": "Henri",
      "full-name": "Henri Matthieu Larrié",
      "id": 2,
      "last-name": "Larrié",
      "mobile": null,
      "skills": [
        {
          "id": 2,
          "level": 5,
          "name": "javascript"
        },
        {
          "id": 5,
          "level": 5,
          "name": "python"
        }
      ]
    }
  ]
}
```


