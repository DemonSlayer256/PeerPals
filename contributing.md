# Contributing to Peerpals

Thank you for considering contributing to our project! Here are some guidelines to help you get started.

## Project Structure

The repository is organized as follows:

``` bash 
project-name/
├── backend/             // Django project files
│   ├── your_app/        // Django app for your functionality
│   ├── manage.py        // Django management script
│   └── settings.py      // Django settings
│
├── frontend/            // React project files
│   ├── src/             // Source files
│   └── public/          // Public files (index.html, etc.)
│
├── database/            // SQL database scripts/migrations
├── docs/                // Documentation files
├── tests/               // Tests for both backend and frontend
└── CONTRIBUTING.md      // Contribution guidelines
```

## How to Contribute

### 1. Fork the Repository

Create a personal copy of the repository.

### 2. Create a Branch

Create a branch for your feature:

``` bash 
git checkout -b feature/your-username/feature-description 
``` 

### 3. Install Dependencies

#### Backend

To set up the Django backend:

``` bash
cd backend
pip install -r requirements.txt  # Install backend dependencies
``` 

#### Frontend

To set up the React frontend:

``` bash
cd frontend
npm install                     # Install frontend dependencies
``` 

### 4. Running the Applications

#### Start the Backend

To run the Django server locally:

``` bash
cd backend
python manage.py runserver  # Starts the Django development server
``` 

#### Start the Frontend

To run the React app locally:

``` bash
cd frontend
npm start                    # Starts the React development server
``` 

### 5. Database Migrations

To apply database migrations in Django:

``` bash
cd backend
python manage.py makemigrations  # Creates migration files based on changes
python manage.py migrate         # Applies migrations to the database
``` 

### 6. Testing

Run tests to ensure your changes do not break existing functionality:

#### Backend

``` bash
cd backend
python manage.py test           # Runs all Django tests
``` 

#### Frontend

``` bash
cd frontend
npm test                       # Runs all React tests
``` 

### 7. Commit Your Changes

Always provide a descriptive commit message:

``` bash
git add .
git commit -m "Brief description of changes"
``` 

### 8. Push to Your Branch

Push your changes to your forked repository:

``` bash
git push origin feature/your-username/feature-description
``` 

### 9. Create a Pull Request

Go to the main repository and open a pull request (PR) from your branch.

### Code of Conduct

Please adhere to our project's code of conduct while interacting with others.
