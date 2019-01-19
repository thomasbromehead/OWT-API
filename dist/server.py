from flask import Flask

app = Flask(__name__)
print("h")

if __name__ == "__main__":
  app.debug = True
  app.run(port=5059)
