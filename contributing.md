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
#### Command Line Method
To create a pull request using the command line, follow these steps:

1. First, ensure you are on your feature branch:
   git checkout your-feature-branch

2. Push your branch to the main repository:
   git push origin your-feature-branch

3. After that, use the following command to create a pull request:
   git request-pull origin/main origin/your-feature-branch

Note: This will output a summary that you can copy to initiate the PR on GitHub.

#### GUI Method

To create a pull request using a graphical interface (e.g., GitHub):

1. Open your web browser and go to the main repository on GitHub.
2. You should see a notification suggesting you create a pull request for your recently pushed branch.
3. Click on the "Compare & pull request" button.
4. Fill in the pull request title and description.
5. Click the "Create pull request" button to submit your PR.
