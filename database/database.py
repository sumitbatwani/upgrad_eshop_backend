# from typing import List, Union

# from beanie import PydanticObjectId

from ast import List
from models.admin import Admin
from models.user import User
from models.address import Address
# from models.student import Student

# admin_collection = Admin
# student_collection = Student

address_collection = Address

async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def add_address(new_address: Address) -> Address:
    address = await new_address.create()
    return address

async def get_address():
    addresses = await address_collection.all().to_list()
    return addresses

async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin

# async def add_admin(new_admin: Admin) -> Admin:
#     admin = await new_admin.create()
#     return admin
    
# async def retrieve_students() -> List[Student]:
#     students = await student_collection.all().to_list()
#     return students


# async def add_student(new_student: Student) -> Student:
#     student = await new_student.create()
#     return student


# async def retrieve_student(id: PydanticObjectId) -> Student:
#     student = await student_collection.get(id)
#     if student:
#         return student


# async def delete_student(id: PydanticObjectId) -> bool:
#     student = await student_collection.get(id)
#     if student:
#         await student.delete()
#         return True


# async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
#     des_body = {k: v for k, v in data.items() if v is not None}
#     update_query = {"$set": {field: value for field, value in des_body.items()}}
#     student = await student_collection.get(id)
#     if student:
#         await student.update(update_query)
#         return student
#     return False
