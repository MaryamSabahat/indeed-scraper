from environs import Env

env = Env()
env.read_env()
# env.read_env('.env.local')

print(env)

USER=env.str('DB_USER')
HOST=env.str('DB_HOST')
PASSWORD=env.str('DB_PASSWORD')
DATABASE=env.str('DB_DATABASE')

print(USER)
print(HOST)
print(PASSWORD)
print(DATABASE)
