import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'pm-secret-key'
#     DEBUG = False

#     # Database configuration
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mydb.db'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///mydb.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Additional configuration options
#     # ...

# class DevelopmentConfig(Config):
#     DEBUG = True

# class ProductionConfig(Config):
#     pass

# # Other configuration classes for different environments
# # ...

# # Select the appropriate configuration class based on the execution environment
# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     # ...
# }



{
    "params":

    {
        "local_server":"True",
        "local_uri": "sqlite:///mydb.db",
        "prod_uri": "sqlite:///mydb.db",
        "twi_url": "https://www.twitter.com/pranitmawale",
        "fb_url": "https://www.facebook.com/PranitMawale",
        "gh_url": "https://www.facebook.com/PranitMawale",
        "blog_name" : "Pranit Mawale's Music Academy",
        "gmail-user":"bhagyeshmawale21@gmail.com",
        "gmail-password":"21believe21",
        "no of post":5



    }
}