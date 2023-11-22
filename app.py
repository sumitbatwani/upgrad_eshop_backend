from fastapi import Body, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt
from config.config import initiate_database
from database.database import add_user
# from models.admin import Admin, AdminSignIn
from models.user import User, UserSignIn
from models.address import Address

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Adjust this to match the origin of your React app
    "http://localhost:8080",
    "*"
    # Add more allowed origins as needed
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can restrict this to specific headers if needed
)

token_listener = JWTBearer()
hash_helper = CryptContext(schemes=["bcrypt"])


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


@app.post("/users")
async def user_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    await add_user(user)
    return {"success": True, "message": "Successfully Signed up!"}

@app.post("/auth")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one(User.email == user_credentials.username)
    if user_exists:
        password = hash_helper.verify(user_credentials.password, user_exists.password)
        if password:
            user = {
                "email": user_exists.email,
                "firstName": user_exists.firstName,
                "lastName": user_exists.lastName,
                "role": user_exists.role,
                "isAdmin": True if user_exists.role == "admin" else False 
            }
            return {"user": user, "token": sign_jwt(user_credentials.username)}

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")

@app.get("/auth/self")
async def user_login(email: str):
    user_exists = await User.find_one(User.email == email)
    if user_exists:
        user = {
                "email": user_exists.email,
                "firstName": user_exists.firstName,
                "lastName": user_exists.lastName,
                "role": user_exists.role,
                "isAdmin": True if user_exists.role == "admin" else False 
            }
        return {"user": user}

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@app.get("/product-categories")
async def get_product_categories():
    product_categories = {"apparel", "electronics", "personal care"}
    return {"data": product_categories}

products = [
    {
        "id": '0',
        "name": 'Tshirt',
        "description": 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
        "category": "apparel",
        "price": 10,
        "manufacturer": "Soni",
        "availableItems": 10,
        "imageUrl": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTDDs0tPjxOZYpy0Ntmf5Fot9hcPh5g_GOkk6V8TsExUq_xNwxk"
    },
    {
        "id": '1',
        "name": 'Jeans',
        "description": 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
        "category": "apparel",
        "price": 12,
        "manufacturer": "Apple",
        "availableItems": 2,
        "imageUrl": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTDDs0tPjxOZYpy0Ntmf5Fot9hcPh5g_GOkk6V8TsExUq_xNwxk"
    },
    {
        "id": '2',
        "name": 'Cream',
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting",
        "category": 'personal care',
        "price": 13,
        "manufacturer": "Amazon",
        "availableItems": 20,
        "imageUrl": "https://abdelghafour122.github.io/ecommerce-product-page/static/media/image-product-1.520cc50bd13955f55cb2.jpg"
    },
    {
        "id": '3',
        "name": 'Shampoo',
        "description": 'Lorem Ipsum is simply dummy text of the printing',
        "category": "personal care",
        "price": 14,
        "manufacturer": "Microsoft",
        "availableItems": 11,
        "imageUrl": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTDDs0tPjxOZYpy0Ntmf5Fot9hcPh5g_GOkk6V8TsExUq_xNwxk"
    },
    {
        "id": '4',
        "name": 'Bluetooth',
        "description": 'Lorem Ipsum is simply dummy text of the printing',
        "category": "electronics",
        "price": 15,
        "manufacturer": "MI",
        "availableItems": 45,
        "imageUrl": "https://abdelghafour122.github.io/ecommerce-product-page/static/media/image-product-1.520cc50bd13955f55cb2.jpg"
    },
    {
        "id": '5',
        "name": 'Speaker',
        "description": 'Lorem Ipsum is simply dummy text of the printing',
        "category": "electronics",
        "price": 16,
        "manufacturer": "HP",
        "availableItems": 50,
        "imageUrl": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTDDs0tPjxOZYpy0Ntmf5Fot9hcPh5g_GOkk6V8TsExUq_xNwxk"
    }
];

@app.get("/products")
async def get_products():
    return {"data": products}

@app.get("/products/{product_id}")
async def get_products_by_id(product_id: str):
    filtered_product = [item for item in products if item["id"] == product_id]
    return {"data": filtered_product[0]}

@app.patch("/products/{id}")
async def update_products(id: str, product: dict):
    index = next((i for i, item in enumerate(products) if item["id"] == id), None)
    if index is not None:
        # Update product details based on the request data
        products[index].update(product)
        return {"success": True, "message": "Product updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    
@app.post("/products")
async def add_products(product: dict):
    new_product = {**product, "id": str(len(products) + 1)}
    products.append(new_product)
    return {"success": True, "message": "Product added successfully"}

@app.delete("/products/{id}")
async def delete_products(id: str):
     index = next((i for i, item in enumerate(products) if item["id"] == id), None)
     if index is not None:
        # Update product details based on the request data
        products.pop(index)
        return {"success": True, "message": "Product deleted successfully"}
     else:
         raise HTTPException(status_code=404, detail="Product not found")

@app.get("/orders")
async def create_order(order: str):
    return {"message": "Your order is confirmed"}


addresses = [
    {
        "id": '0',
        "email": "sumitbatwani@gmail.com",
        "name": "Sumit Kumar",
        "contactNumber": "1234567890",
        "city": "mumbai",
        "landmark": "tina bliss",
        "street": "chembur",
        "state": "maharashtra",
        "zipcode": "400899",
    }
]

@app.post("/addresses")
async def add_address(address: dict = Body(...)):
    addresses.append({**address, "id": len(addresses) + 1})
    return {"success": True, "message": "Successfully added address!"}

@app.get("/addresses")
async def get_address():
    return {
        "status_code": 200,
        "data": addresses,
    }

@app.post("/orders")
async def place_order(order: dict = Body(...)):
    return {"success": True, "message": "Order placed successfully!"}
