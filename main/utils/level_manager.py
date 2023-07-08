import math

class LevelManager:
	def __init__(self) -> None:
		self.constant = 1/math.sqrt(10)

	def get_level(self, xp):
		return self.constant*math.sqrt(xp) + 1
    
	def get_xp(self, level):
		return 10*(level**2 - 2*level + 1)
	
	def get_level_statistics(self, xp):
		level = self.get_level(xp)
		int_level = int(level) # Integer part of level
		dec_level = level - int_level # Float part of level

		xp_start = self.get_xp(int_level)
		xp_end = self.get_xp(int_level+1)
		range_xp = xp_end - xp_start

		progress_xp = round(dec_level, 4) * range_xp

		statistics = {
			'level': level,
			'lvl_xp_start': xp_start,
			'lvl_xp_end': xp_end,
			'progress_xp': progress_xp,
			'range_xp': range_xp
		}
		return statistics
	