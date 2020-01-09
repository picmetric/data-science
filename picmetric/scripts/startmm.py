from flaskapp.models.persist import Persistent
import os

if __name__ == "__main__":
	print(os.getcwd())
	p = Persistent(max_tries=15)
	del p
