from fastapi import FastAPI, Depends, Query, HTTPException
from typing import Annotated    # Tells FastAPI to treat the value as both a type and a dependency.

app: FastAPI = FastAPI()

# 1. Hello Dependency

def get_simple_goal():
    return {"goal": "We are building AI agents Workforce"}

@app.get("/get-simple-goal")
def simple_goal(response: Annotated[dict, Depends(get_simple_goal)]):
    return response

# 2. Dependency with Parameter
# We can even pass function parameters in Dep.

def get_goal(username: str):
    return {"goal": "We are building AI agents Workforce", "username": username}

@app.get("/get-goal")
def get_my_goal(response: Annotated[dict, Depends(get_goal)]):
    return response


# 3. Dependency with Query Parameters
# Check a Secret Key

# dependency function
def dep_login(username: str = Query(None), password: str = Query(None)):
    if username == "admin" and password == "admin":
        return {"message": "Login Succesful!"}
    else:
        return {"message": "Login Failed"}
    
@app.get("/signin")
def login_api(user: Annotated[dict, Depends(dep_login)]):
    return user


# 4. Multiple Dependencies

def depfunc1(num: int):
    num = int(num)
    num += 1
    return num

def depfunc2(num: int):
    num = int(num)
    num += 2
    return num


@app.get("/main/{num}")
def get_main(num: int, num1: Annotated[int, Depends(depfunc1)], num2: Annotated[int, Depends(depfunc2)]):
    total= num + num1 + num2
    return f"Total : {total}"


# 5. CLASSES

blogs = {
    "1": "Generative AI Blog",
    "2": "Machine Learning Blog",
    "3": "Deep Learning Blog"
}

users = {
    "8": "shanzay",
    "9": "fatima"
}

class GetObjectOr404():
    def __init__(self, model)-> None:
        self.model = model

    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Object ID {id} not found")
        return obj
    
    
blog_dependency = GetObjectOr404(blogs)

@app.get("/blog/{id}")
def get_blog(blog_name: Annotated[dict, Depends(blog_dependency)]):
    return blog_name


user_dependency = GetObjectOr404(users)

@app.get("/user/{id}")
def get_user(user_name: Annotated[dict, Depends(user_dependency)]):
    return user_name