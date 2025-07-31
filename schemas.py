from pydantic import BaseModel, field_validator

class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True

class CreatePost(PostBase):
    class Config:
        orm_mode = True

class CarOut(BaseModel):
    company: str
    name: str
    engine: str
    displacement: str
    horsepower: int
    top_speed: int
    zero_sixty: float
    price: int
    fuel_type: str
    seats: int
    torque: str

class CarCreate(BaseModel):
    company: str
    name: str
    engine: str
    displacement: str
    horsepower: int
    top_speed: int
    zero_sixty: float
    price: int
    fuel_type: str
    seats: int
    torque: str

    @field_validator('horsepower', mode="before")
    def normalize_horsepower(cls, value: str) -> int:
        if isinstance(value, int):
            return value
        if value is None:
            return 0
        try:
            clean_value = (
                value.lower()
                    .replace('up to', '')
                    .replace('~','')
                    .replace(',', '')
                    .replace('hp', '')
                    .replace(' ', '')
                )
            if '-' in clean_value:
                low, high = clean_value.split('-')
                return round((int(low) + int(high)) / 2)
            if '/' in clean_value:
                low, high = clean_value.split('/')
                return round((int(low) + int(high)) / 2)
            return int(clean_value)
        except:
            raise ValueError(f"Unexpected value {value}")
        
    @field_validator('top_speed', mode="before")
    def normalize_speed(cls, top_speed: str) -> int:
        if isinstance(top_speed, int):
            return top_speed
        if top_speed is None:
            return 0
        
        try:
            return int(top_speed.lower().replace('km/h', '').strip())
        except:
            raise ValueError(f"Unexpected value {top_speed}")
        
    @field_validator('zero_sixty', mode="before")
    def normalize_zero_sixty(cls, zero_sixty: str) -> float:
        if isinstance(zero_sixty, float):
            return zero_sixty
        if zero_sixty is None or zero_sixty.lower() == 'n/a':
            return 0.0
        try:
            # Clean the input by removing irrelevant text
            clean_value = (
                zero_sixty.lower()
                    .replace(' ', '')
                    .replace('sec', '')
            )

            # Handle ranges with '/' or '-'
            if '/' in clean_value:
                low, high = clean_value.split('/')
                return round((float(low) + float(high)) / 2, 2)
            if '-' in clean_value:
                low, high = clean_value.split('-')
                return round((float(low) + float(high)) / 2, 2)

            # If no delimiter, convert directly to float
            return float(clean_value)
        except Exception as e:
            raise ValueError(f"Unexpected value: {zero_sixty}")
        
    @field_validator('price', mode="before")
    def normalize_price(cls, price: str) -> int:
        if isinstance(price, int):
            return price
        if price is None:
            return 0
        
        try:
            cleaned_price = price.lower().replace('$', '').replace(',', '').replace(' ', '')
            if '-' in cleaned_price:
                low, high = cleaned_price.split('-')
                return round((int(low) + int(high)) / 2)
            if '/' in cleaned_price:
                low, high = cleaned_price.split('/')
                return round((int(low) + int(high)) / 2)
            return int(cleaned_price)
        except Exception as e:
            raise ValueError(f"Unexpected value: {price}")
    
    @field_validator('seats', mode='before')
    def normalize_seats(cls, seats: str) -> int:
        if isinstance(seats, float):
            return seats
        if seats is None:
            return 0

        try:
            cleaned_seats = seats.lower().strip()
            if '+' in cleaned_seats:
                return eval(cleaned_seats)
            return int(cleaned_seats)
        except:
            raise ValueError(f"Unexpected value {seats}")