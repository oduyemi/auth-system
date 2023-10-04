from authsys_app import app, db, celery


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # Start the Celery worker by executing the separate script
    import subprocess
    subprocess.Popen(['python', 'celery_worker.py'])

    app.run(debug=True, port=8000)
