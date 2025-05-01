# FastAPI Builder

FastApiFy is a command-line tool designed to streamline the creation of well-organized file structures for FastAPI
projects. It enables developers to kickstart their projects with best practices in mind, reducing boilerplate and setup
time.

## Features

- **Automated File Structure Creation**: Generate a production-ready project structure in seconds.
- **Customizable Templates**: Define your own templates to suit your development style.
- **Extensible Commands**: Add custom commands to extend functionality.
- **User-Friendly Interface**: Simple CLI commands for intuitive usage.

---

## Installation

Install FastApiFy via pip:

```bash
pip install fastapify
```

---

## Usage

### Create a New Project

To create a new FastAPI project, run:

```bash
fastapify startproject my-fastapi-project
```

This will scaffold a directory structure with the following layout:

```
my-fastapi-project/
├── .envs/
│   ├── .local/
│   │      ├── .db
│   │      └── .web
│   └── .prod/
│   
├── compose/
│   ├── local/
│   │      └── django/
│   │            └── Dockerfile
│   └── prod/
│          └── django/ 
├── core
│   ├── config.py
│   ├── database.py
│   └── middlewares.py
│  
├── requirements/
│   ├── base.txt
│   └── local.txt
│  
├── src/
│   ├── __init__.py
│   └── api.py
│
├── local.yml
├── prod.yml
└── README.md
```

### Create new App

Easily add new applications to your project with:

```bash
fastapify startapp myapp
```

This creates `src/myapp/` with the following structure:

app structure:

```
myapp/
├── __init__.py
├── admin.py
├── models.py
├── router.py
├── schemas.py
└── service.py
```

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository and
create a pull request.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

---

## License

FastApiFy is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by the simplicity and power of FastAPI.
- Thanks to the open-source community for providing valuable resources and inspiration.

---

Get started today with FastApiFy and make your API development fast, efficient, and fun!
