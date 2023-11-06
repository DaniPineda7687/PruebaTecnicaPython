from fastapi import FastAPI, HTTPException, Path, status
from typing import List
import requests
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Configuración de la base de datos MySQL
DATABASE_URL = "mysql://root:password@db/api_app"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definición de la tabla de productos e imagenes de productos en la base de datos
Base = declarative_base()
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(Text, default=None) 
    images = relationship("ProductImage", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="images")


# Modelo de datos de respuesta para el endpoint GET /api/data y /api/data/{id}
class ProductData(BaseModel):
    id: int
    title: str
    price: int
    description: str
    images: List[str]

# Endpoint para obtener datos del servicio externo
@app.get("/api/data", response_model=List[ProductData])
def get_data():
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=500, detail="Error al recuperar los datos de la api externa")


# Endpoint para obtener datos de un producto por ID de la base de datos
@app.get("/api/data/{product_id}", response_model=ProductData)
def get_product_by_id(product_id: int = Path(..., title="Product ID")):
    db = SessionLocal()
    
    try:
        # Busca el producto en la base de datos
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        product_data = ProductData(
            id=product.id,
            title=product.name,
            price=product.price,
            description=product.description,
            images=[image.url for image in product.images]
        )
        
        return product_data
    finally:
        db.close()
        
# Endpoint para almacenar datos en la base de datos
@app.post("/api/data", status_code=status.HTTP_201_CREATED)
def create_product():
     # Realizar una solicitud GET al servicio externo
    external_api_url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(external_api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al recuperar los datos de la api externa")

    external_data = response.json()[:20]

    db = SessionLocal()

    try:
        for product_data in external_data:
            product = Product(
                name=product_data["title"],
                price=product_data["price"],
                description=product_data["description"]
            )
            db.add(product)
            db.commit()
            db.refresh(product)

            for image_url in product_data["images"]:
                product_image = ProductImage(url=image_url, product_id=product.id)
                db.add(product_image)

        db.commit()
        db.close()

        return {"message": "Productos creados a partir de datos externos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrio un error en el servidor mientras se guardaban los datos")