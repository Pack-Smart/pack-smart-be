# Pack Smart Backend Application

Pack Smart is an application that allows uers to fill out a short survey about an upcoming trip and then provides a list of items to bring broken down into various categories. Users can then edit and save their packing lists.

## Summary

  - [Project Description](#project-description)
  - [Setup Instructions](#setup-instructions)
  - [Runing the tests](#running-the-tests)
  - [Learning Goals](#learning-goals)
  - [Functionality](#functionality)
  - [Programming Languages Used](#programming-languages-used)
  - [Key Takeaways](#key-takeaways)
  - [Next Steps](#next-steps)
  - [Contributors](#contributors)
  - [Acknowledgements](#acknowledgements)


## Project Description

Description...Coming Soon!

- [Project Brief and Rubric](https://mod4.turing.io/projects/capstone.html)
- [Deployed Github Page...Coming Soon!]

## Setup Instructions

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. This app is built with Python using a [PostgreSQL](https://www.postgresql.org/) database, so please make sure you have those installed. You can download Python [here](https://www.python.org/downloads/), and make sure to download version `3.9.1`. You may also want to download the `venv` module which provides support for creating lightweight virtual environments.

`python3 -m venv ./venv` will download the `venv` module, and if you have a `xcrun: error: invalid active developer path ` error you can run this command: `xcode-select --install`.

You can follow directions via the Setup documentation, and please see below for some helpful commands if you run into any errors.

* Clone down this repository to your local machine: `git clone git@github.com:Pack-Smart/pack-smart-be.git`
* Change into the directory: `cd pack-smart-be`
* Activate the virtual environment: `source venv/bin/activate`
* Install requirements: `pip3 install -r requirements.txt`
* Create the database: `createdb pack_smart_dev`
* Set the database URL: `export DATABASE_URL=postgresql://localhost:5432/pack_smart_dev`
* Upgrade the database: `python3 manage.py db upgrade`
* Create the test database: `createdb pack_smart_test`
* Install a tool to help import csv file: `pip3 install psycopg2-binary`
* Seed the database: `python3 manage.py db_seed`
* Spin up the local server: `python3 run.py`
* In [Postman](https://www.postman.com/), create a new request by clicking `New`, `Request`
* Enter your request URL endpoint - it is most likely `http://127.0.0.1:5000/api/v1/list/new`
* In `Body`, set to `raw` and `JSON`
* Data structure should be in the following format:
   ```
   {
     data: {
       id: 0,
       type: 'survey',
       attributes: {
         gender: ['All', quizData.gender],
         weather: ['All', ...modifyWeatherData],
         tripDetails: {
           title: quizData.name,
           destination: quizData.destination,
           number_of_days: quizData.number_of_days,
         },
         categories: [
           'Accessories',
           'Clothing',
           'Essentials',
           'Toiletries',
           'Misc.',
           ...quizData.categories
         ]
       }
     }
   }
    ```

To shut off your virtual environment, run `deactivate`.

Note: This project was created using a [starter repo](https://github.com/iandouglas/flask-restful-travis-heroku). Please check it out for more details and context about the setup.

## Running the Tests

## Learning Goals

Learning Goals...Coming Soon!

## Functionality

This API will return data broken down into categories that are specified in the call from the frontend.

An example of a call from the frontend might look like:

```
{
    "data": {
        "id": 0,
        "type": "survey",
        "attributes": {
            "gender": ["All", "Male"],
            "weather": ["All", "%hot%", "%rainy%"],
            "destination": "Miami",
            "number_of_days": "7",
            "categories": ["Wedding", "Beach", "Child_all", "Child_0-2"]
        }
    }
}
```

The response may look like:

EXAMPLE HERE

## Programming Languages Used

Languages...Coming Soon!

## Planning

[Wireframes](https://excalidraw.com/#room=8aef215904a24ca203cf,zHjBq8xtMaifCnF07wP2jQ) created using [Excalidraw](https://excalidraw.com/).

Database schema:

![Screen Shot 2021-02-22 at 1 35 55 PM](https://user-images.githubusercontent.com/7945439/108887035-f176c800-75c6-11eb-8393-0f42e943e35a.png)

## Key Takeaways

### Challenges

Challenges...Coming Soon!

### Wins

Wins...Coming Soon!

## Next Steps

Next Steps... Coming Soon!


## Contributors

* [Jose Lopez](https://github.com/JoseLopez235)
* [Kevin David Cuadros](https://github.com/kevxo)
* [Roberto Basulto](https://github.com/Eternal-Flame085)
* [Sheryl Stillman](https://github.com/stillsheryl)

## Acknowledgements

* [Will Mitchell](https://github.com/wvmitchell) - Project Manager
* [Ian Douglas](https://github.com/iandouglas) - flask-restful-travis-heroku [Starter Repo](https://github.com/iandouglas/flask-restful-travis-heroku)
