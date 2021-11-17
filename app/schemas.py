from datetime import time
from pydantic import BaseModel, Field
from typing import List, Optional

class Credentail(BaseModel):
    id: Optional[str]
    resource: str
    encrypted_key: str
    public_key: str
    expire_at: str
    active: bool