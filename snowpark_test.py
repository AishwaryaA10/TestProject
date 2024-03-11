from snowflake.snowpark.session import Session

connection_params = {'user': "REFRACT.FOSFOR@LNTINFOTECH.COM", 'password': "Password321", 'account':"fya62509.us-east-1", 'role':"FOSFOR_REFRACT", 'warehouse': "FOSFOR_REFRACT"}

session = Session.builder.configs(connection_params).create()
data = session.sql("SHOW DATABASES;").collect()
print(data)
session.close()
