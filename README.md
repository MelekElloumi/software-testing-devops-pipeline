# App 4 Software Testing & DevOps Pipeline
- This is a small python application that I made to try on 4 types of software testing and a DevOps pipeline.

## AppTest Description

- The user login then manages products (CRUD). He can buy a product or get the price average.
- I used sqlite3 for the database. It is initialised with databaseinit.py.
- I used Flask for the web development.

  ### Execution:
  ![2014-10-22 11_35_09](https://j.gifs.com/A6oyA7.gif)


## Software Testing
- In each folder you will find one level of testing with its Readme file:
    1. Unit testing
    2. Integration testing
    3. E2E testing
    4. UAT

## DevOps Pipeline
![example workflow](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/actions/workflows/DevOps_Pipeline.yml/badge.svg)

- I integrated a CI/CD pipeline using GitHub Actions, Docker and "deployment server".
- The main workflow consists of 3 jobs :
    1. Test
       - 2 parallel jobs: Tests on python 3.8 and 3.9
    2. Build
       - A docker image is built and pushed to [Docker Hub](https://hub.docker.com/r/melekelloumi/app4test)
    3. Deploy
    

  
