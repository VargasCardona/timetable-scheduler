
# timetable-scheduler

![Repo Size](https://img.shields.io/github/repo-size/VargasCardona/timetable-scheduler?style=for-the-badge)
![License](https://img.shields.io/github/license/VargasCardona/timetable-scheduler?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/VargasCardona/timetable-scheduler?style=for-the-badge)

A lightweight and flexible application for managing teacher timetables. Designed for simplicity and easy integration. This project is containerized using Docker with Docker Compose for managing the MySQL database.

## Features
- Easy-to-use interface for scheduling and managing teacher timetables.
- Supports CRUD operations for timetable management.
- Containerized using Docker and Docker Compose for smooth setup and deployment.

## Requirements
- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/timetable-scheduler.git
   cd timetable-scheduler
   ```

2. Build and start the containers using Docker Compose:
   ```
   docker-compose up --build
   ```

3. The MySQL database will be available and ready for interaction once the containers are up.

## Usage

- Access the application at `http://localhost:3306`.
- Interact with the timetable scheduler to add, modify, and view timetables.

## Contributors

- **Nicolás Vargas Cardona** - [GitHub Profile](https://github.com/VargasCardona)
- **Mateo Loaiza García** - [GitHub Profile](https://github.com/Matthub05)

## License
This project is licensed under the [GNU General public license](https://www.gnu.org/licenses/) - see the LICENSE file for details.
