
# Balance App API

Simple API for keeping track of food and daily meal data.


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
4. Install requirements.

```
    pip install -r requirements.txt
```
```
    pip install -U channels["daphne"]
```
5. Setup database:
```
    python manage.py makemigrations
```
```
    python manage.py migrate
```
6. Run server
```
    python manage.py runserver
```
## How to use (in Dart)
1. Run server.
```
    python manage.py runserver
```
2. Import http package.
```
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';
```

3. Register, login.
* Register and login request will return a token if succeed, the token will be used for later authentication.
#### Register
```
void register() async {
    final url = 'localhost:8000';

    final headers = {
        'Content-type': 'application/json',
    };
    final user_profile_msg = jsonEncode({'username': 'joe', 'password': 'abcd1234'});
    try {
        final response = await http.post(
            Uri.http(url, '/accounts/register/'),
            headers: headers,
            body: user_profile_msg
        );

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
    final user_profile_msg = jsonEncode({'username': 'joe', 'password': 'abcd1234'});
    try {
        final response = await http.post(
            Uri.http(url, '/accounts/login/'),
            headers: headers,
            body: user_profile_msg
        );

        final data = jsonDecode(response.body);
        token = data["token"]; // User token which will be used for accessing personal data.
        debugPrint('Token ${token}\n');
    } catch (e) {
        debugPrint(e.toString());
    }
}
```

4. Load foods and nutrients.

* Send a GET request to localhost:8000/load_data/ to load nutrients and foods database.

5. Example fetching food data.
```
void getFoods() async {
    final url = 'localhost:8000';
    final headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Token ${token}', // Insert personal token to header
    };
    try {
        final response = await http.post(Uri.http(url, '/foods/'),
            headers: headers,
            body: jsonEncode({
                "show_details": false,
                // if true, returns all nutritional values for each food (VERY LONG).
            }
        ));
        debugPrint(response.body);
        str = response.body;
    } catch (e) {
        debugPrint(e.toString());
    }
}
```
