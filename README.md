# cyber-security-project
A repository for the cyber security base project I

Project is created using Python and Flask. Running the project requires PostgreSQL, which can be installed from [here](https://www.postgresql.org/download/)

## Installation guide

- Clone this repository locally
- Install dependencies with ```pip install -r requirements.txt```
- Create a .env file, which should include the following information:
  - ```DATABASE_URL="PostgreSQL:///username"```, using your own username
    - you might alternatively have to use ```postgresql+psycopq2:///yourusername```
  - ```SECRET_KEY=key_here```, replacing key_here with your own secret key
- Run the database in a separate terminal with the command ```start-pg.sh```
- Run the application with ```flask run```
