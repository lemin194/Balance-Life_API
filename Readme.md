
# Foodtracking App API

A simple foodtracking API, for school project.


## Installation

1. Clone repository.
```
    git clone https://github.com/lemin194/Balance_TTNM
```
```
    cd Balance_TTNM
```
2. Create a virtual env.

```
    python -m venv project_env
```
```
    project_env\Scripts\activate.bat
```
3. Install requirements.

```
    pip install -r requirements.txt
```
```
    pip install -U channels["daphne"]
```
4. Setup database:
```
    python manage.py makemigrations
```
```
    python manage.py migrate
```
These lines will create MySQL tables. You can check with MySQL Workbench.

5. Run server
```
    python manage.py runserver
```
## Database
This API use MySQL as the database manager, so make sure you have it installed. 
## Superuser and admin page
Run the following command to create a superuser that you can use to play with the database.
```
    python manage.py createsuperuser
```
Run server then go to the admin page at 127.0.0.1:8000/admin/, login with the account you created.
The admin page will let you do anything with the database, which will help you catch the main idea of what this API is doing.

## How to use (in Dart)
1. Run server.
```
    python manage.py runserver
```
The server will be launched on local host at port 8000 by default.\
Go to 127.0.0.1:8000/ to see all entrypoints available to use.\
There are 4 types of requests that will mainly be used in this project: "GET", "POST", "PUT", "DELETE".\
Explain:
* Send a request to the server by the http package of flutter, or you can use Postman to make test requests and playaround with the databases.
* A body of the request will be in JSON type.
* "GET" request is for getting information, the body is usually empty.
* "POST" request is for sending the body and sometimes receive back the data from the server, for example: creating a food object; or to receive all food objects with corresponding search input.
* "PUT" request is for updating an item. For example: sending a PUT request to endpoint /meals/5/update/ to perform an update on the meal object with the id = 5.
* "DELETE" request is for deleting an item. For example: sending a DELETE request to endpoint /meals/5/delete/ will delete the meal with id = 5 if exists (if doesn't exist it will response with a Bad Request)
* Every endpoints can be seen at 127.0.0.1:8000/
*
* There is an endpoint at /load_data/, which will load the ingredients and nutrients data with the 

    
2. Import http package.
* Installation: https://pub.dev/packages/http/install
```
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';
```

3. Register, login.
* Register and login request will return an user id if succeed.
#### Register
```
void register() async {
    final url = 'localhost:8000';

    final headers = {
    'Content-type': 'application/json',
    };
    final user_profile_msg =
        jsonEncode({'username': 'joe', 'password': 'abcd1234'});
    try {
        final response = await http.post(Uri.http(url, '/accounts/register/'),
            headers: headers, body: user_profile_msg);

        if (response.statusCode != 200) throw Exception(response.body);
        var jsonObject = jsonDecode(response.body);
        debugPrint(response.body);
    } catch (e) {
        debugPrint(e.toString());
    }
}
```

#### Login
```
void login() async {
    final url = 'localhost:8000';

    final headers = {
        'Content-type': 'application/json',
    };
    final user_profile_msg =
        jsonEncode({'username': 'dane', 'password': 'abcd1234'});
    try {
        final response = await http.post(Uri.http(url, '/accounts/login/'),
            headers: headers, body: user_profile_msg);

        final data = jsonDecode(response.body);
        if (response.statusCode != 200) throw Exception(response.body);
        var user_id = data["user_id"];
        debugPrint('User ${user_id} logged in\n');
        // There won't be any logging in at the server, only the user id will be return for accessing unique user's data.
    } catch (e) {
        debugPrint(e.toString());
    }
}
```

4. Load example database.

* Send a GET request to 127.0.0.1:8000/load_data/ to load nutrients and ingredients database before hand.

5. Example fetching ingredients data.
```
void getIngredients() async {
    final url = 'localhost:8000';
    final headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    };
    try {
        final response = await http.post(Uri.http(url, '/ingredients/'),
            headers: headers,
            body: jsonEncode({
            "show_details": false,
            "show_total": false,
            }));
        if (response.statusCode != 200) throw Exception(response.body);
        debugPrint(response.body);
    } catch (e) {
        debugPrint(e.toString());
    }
}
```
