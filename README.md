# d4sg_trauma

This is Backend project.

Environmet:

* Python 3.6

Sample Command

```
gunicorn -w 4 --worker-class eventlet -b 0.0.0.0:5000 server:app --log-level=debug
```