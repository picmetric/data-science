from flaskapp.models.persist import Persistent

if __name__ == "__main__":
	p = Persistent(max_tries=15)
	del p
