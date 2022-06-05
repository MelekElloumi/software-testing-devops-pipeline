# App 4 Software Testing & DevOps Pipeline
- This is a small python application that I made to try on 4 types of software testing and a DevOps pipeline.

## App4Test Description

- The user login then manages products (CRUD). He can buy a product or get the price average.
- I used sqlite3 for the database. It is initialised with databaseinit.py.
- I used Flask for the web development.

  ### Execution:
  ![2014-10-22 11_35_09](https://j.gifs.com/A6oyA7.gif)


## Software Testing
- In each folder you will find one level of testing with its Readme file:
    1. [Unit testing](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/tree/main/UnitTest)
    2. [Integration testing](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/tree/main/Integration%20Test)
    3. [E2E testing](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/tree/main/e2e%20Test)
    4. [UAT](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/tree/main/UAT)

## DevOps Pipeline
![example workflow](https://github.com/MelekElloumi/Software-Testing-DevOps-Pipeline/actions/workflows/DevOps_Pipeline.yml/badge.svg)

- I integrated a CI/CD pipeline using GitHub Actions, Docker and Amazon ECS.
- The main workflow consists of 3 jobs :
    1. Test
       - 2 parallel jobs: Tests on python 3.8 and 3.9
    2. Build
       - A docker image is built and pushed to [Docker Hub](https://hub.docker.com/r/melekelloumi/app4test)
    3. Deploy
        - The image is deployed to ECS with a service of 2 tasks and exposed on port 5000.
        - If service is running, check App4Test [here](http://44.200.159.100:5000/)
  
    ### Pipeline:
    ![Imgur](https://i.imgur.com/95VMQqK.png)
    ### Deployed app:
    ![Imgur](https://i.imgur.com/qNBk1u7.png)

  
