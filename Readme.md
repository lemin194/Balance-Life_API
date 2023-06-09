
# Balance-Life App API

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
4. Setup database:
```
    python manage.py makemigrations
```
```
    python manage.py migrate
```
These lines will create SQL tables. You can query the file "db.sqlite3".

5. Run server
```
    python manage.py runserver 0.0.0.0:8000
```
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
    python manage.py runserver 0.0.0.0:8000
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
        jsonEncode({
            'email': 'joe@gmail.com', 
            'password': 'abcd1234',
            'first_name': 'Joe',
            'last_name': 'Hill',
        });
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
        jsonEncode({
            'email': 'joe@gmail.com', 
            'password': 'abc123',
        });
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
### Uploading food image

```
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart' as path;
import 'package:http/http.dart' as http;


var url = '192.168.0.100:8000';

Future<String> sendPostRequest({endpoint, body}) async {
  final headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
  };
  try {
    final response = await http.post(Uri.http(url, endpoint),
        headers: headers, body: jsonEncode(body));
    if (response.statusCode != 200) throw Exception(response.body);
    return response.body;
  } catch (e) {
    debugPrint(e.toString());
    return e.toString();
  }
}

Future<void> uploadImage() async {
    final ImagePicker picker = ImagePicker();

    final XFile? image = await picker.pickImage(
        source: ImageSource.gallery, imageQuality: 70);
    if (image == null) {
        print("no image picked");
        return;
    }
    File imagefile = File(image.path);
    Uint8List imagebytes = await imagefile.readAsBytes();
    String base64string = base64.encode(imagebytes);
    var foodId = 2;
    var send_data = 
    {
        "file": 
        {
            "filename": path.basename(imagefile.path),
            "content": base64string,
        },
    };
    var response = await sendPostRequest(
        endpoint:
            "foods/" + foodId.toString() + "/uploadimage/",
        body: send_data);
    debugPrint(response);
}
```
## Note

### Reset database

The app's database is stored in file "db.sqlite3", if you want to reset it, you have to remigrate the whole database, which can be done through following steps:
* Delete the db.sqlite3 file.
* Delete migrations data, which are the files "****_initial.py" located in "food/migrations/" and "chats/migrations/". If not it will conflict with the previous migrating instructions by the django app.
![image](https://user-images.githubusercontent.com/61057734/236612118-17f55008-2af5-4c50-86f1-e1389364cefd.png)
* Remigrate the database by following commands (this will create a new "db.sqlite3" file):
```
    python manage.py makemigrations
    python manage.py migrate
```
