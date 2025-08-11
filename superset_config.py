SECRET_KEY = 'JiI87ouhSQSxVdsZO/nLXVSkGC5DhbWLe5CLpEFN1nwPeZb1BMSC525V'

import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql://greenchain_admin:MTvRpQRtD2c5yIpQplT9dDDgXRC6BhYm@dpg-d285uac9c44c73a3sa70-a.frankfurt-postgres.render.com:5432/greenchain_db"
)





