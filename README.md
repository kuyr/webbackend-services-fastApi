# Minimalist Social Media Backend Services

Welcome to the backend services of our minimalist social media app built with the FastAPI framework. This project aims to provide a simple and efficient backend infrastructure for handling essential social media functionalities.

## Features

- **User Management:** Create, read, update, and delete user profiles.
- **Post Handling:** Allow users to create, view, update, and delete posts.
- **Authentication:** Secure endpoints using JSON Web Tokens (JWT) for user authentication.
- **API Documentation:** Utilize FastAPI's automatic and interactive API documentation.

## Getting Started

1. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access API Documentation:**
   Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API using the interactive documentation.

## Configuration

- Adjust configurations such as database connection, JWT secret, and other settings in the `config.py` file.

## Dependencies

- FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- SQLAlchemy: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
- Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)

## Contributing

We welcome contributions! If you'd like to contribute to this project, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the FastAPI team for providing an excellent framework for building APIs.

Happy coding! 🚀
