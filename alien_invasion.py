import sys
import pygame
import game_functions as gf
from ship import Ship
from bullet import Bullet
from alien import Alien
from settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from Button import Button
from scoreboard import Scoreboard

def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("alien")
	ship = Ship(screen, ai_settings)
	bullets = Group()
	aliens = Group()
	gf.create_fleet(screen, ai_settings, ship, aliens)
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	play_button = Button(ai_settings, screen, "Play")
	while True:
		gf.check_events(screen, ai_settings, ship, bullets, stats, play_button, aliens, sb)
		if stats.game_active:
			ship.update()
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
			gf.update_bullets(screen, ai_settings, ship, aliens, bullets, stats, sb)
			
		gf.update_screen(screen, ai_settings, stats, ship, aliens, bullets, play_button, sb)

run_game()
