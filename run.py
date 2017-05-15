#! /usr/bin/env python
from app import app
app.secret_key = 'many random bytes'
app.run(debug=True,host="0.0.0.0",port=8080)