# Installation

First, clone this repository using the command.
```
git clone https://github.com/yixor/test_env.git
```

Then, navigate to the project directory.
```
cd test_env/
```

The fastest method to start the application is to use the "docker compose" command.
```
docker compose -f docker_compose.yaml up --build
```

The second method is to run the application with your own environment variables in the "Dockerfile" using the command:
```
docker build -t test_env . && docker run -it test_env
```

The third method involves changing the boolean value to "False" in the `settings.py` file and setting all necessary configurations.

![image](https://github.com/yixor/test_env/assets/119937880/b81c8412-0cb0-4b61-b562-677a163197c0)

The next step is to install all the necessary packages and create virtual environment.
```
python3 -m venv .venv/
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
After this, run `main.py`. 
```
python3 main.py
```
Note that **PostgreSQL** and **Redis** need to be running for the application to work.

# Usage
You can get a cached list of **"Product"** objects and their IDs at the following address: `"{HOST}:{PORT}/product/list"` with `GET` method.

![image](https://github.com/yixor/test_env/assets/119937880/a1ced45d-3fe5-424b-8739-c543bc830f46)

Access to products with their `id`, `GET` method:

![image](https://github.com/yixor/test_env/assets/119937880/c5b3bed4-5d84-40f0-b685-2753812c5886)

Pagination is available via the **page** parameter. Example: `?page=1`:

![image](https://github.com/yixor/test_env/assets/119937880/da6f8270-f5fc-490c-9e42-a86346305a26)

Adding new records is available at the path `/review/add/<int:product_id>` using the **POST** method and the **"application/json"** content-type.

```
curl -X POST http://172.19.0.4:8000/review/add/137 \
     -H "Content-Type: application/json" \
     -d '{"asin": "B06X14Z8JP", "title": "Test_Review", "review": "Test Review"}'
```
