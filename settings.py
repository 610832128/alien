class Settings():
	def __init__(self):
		self.screen_width = 1000
		self.screen_height = 650
		self.bg_color = (230, 230, 230)
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 10
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		self.ship_limit = 3
		self.score_scale = 1.5
		self.alien_points = 50
		self.speed_up_scale = 1.1
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1

	def increase_speed(self):
		self.ship_speed_factor *= self.speed_up_scale
		self.bullet_speed_factor *= self.speed_up_scale
		self.alien_speed_factor  *= self.speed_up_scale
		self.alien_points = int(self.alien_points * self.score_scale)
