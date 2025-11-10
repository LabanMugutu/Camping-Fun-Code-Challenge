from . import create_app

app = create_app()

if __name__ == "__main__":
    # runs on http://localhost:5555 when executed as: python server/app.py
    app.run(port=5555, debug=True)
