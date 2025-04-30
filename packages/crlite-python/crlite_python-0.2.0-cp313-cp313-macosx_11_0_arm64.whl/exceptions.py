class CRLiteDBError(Exception):
	"""Any error in the CRLiteDB"""
	def __init__(self, message: str):
		super().__init__(f"{message}")

# class CRLiteDBError(Exception):
# 	pass
