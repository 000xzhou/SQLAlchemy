# SQLAlchemy

- current problem
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  isn't default date time is always 00:00
  datetime.now() works on app.py but when add it as created_at the time still shows 00:00 no matter what too
