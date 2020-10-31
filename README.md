Demo Project - FastAPI with SQLite
=======================
Useful Links:  

 + [FastAPI](https://fastapi.tiangolo.com)
 + [FastAPI with Database](https://fastapi.tiangolo.com/tutorial/sql-databases/)

Steps
------------
 1. Download database and put it under `${FastAPI-sample}/data/` folder  
 2. Install dependencies (fastAPI+uvicorn)  
    `pip install -r requirement.txt`
 3. Run the API  
    `./run.sh`
 4. Open browser and send GET request  
    `https://localhost:8000/search?word={word}`  

Demo
------------
1. browser: `http://localhost:8000/search?word=[PERSON]&limit=5`  
   ![](img/demo1.png)  
2. browser: `http://localhost:8000/search?word=%E4%BD%8F%E5%AE%85&limit=10`  
   ![](img/demo2.png)
