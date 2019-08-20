import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break
			
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	if stats.ship_left > 0:
		stats.ship_left -= 1
		sb.pre_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(screen, ai_settings, ship, aliens)	
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		stats.button_clicked = False
		pygame.mouse.set_visible(True)

def update_bullets(screen, ai_settings, ship, aliens, bullets, stats, sb):
	bullets.update()
	check_bullets(bullets)
		
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)
	
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for collision in collisions.values():
			stats.score += ai_settings.alien_points * len(collision)
		sb.pre_score()
		sb.check_high_score()
	if len(aliens) == 0:
		stats.level += 1
		sb.pre_level()
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(screen, ai_settings, ship, aliens)	

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
		alien.y = alien.rect.y
		alien.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
	check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
def get_number_rows(ai_settings, ship_height, alien_height):
	available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_row, alien_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.y = alien_height * 2 + 2 * alien_height * alien_row
	alien.rect.y = alien.y
	aliens.add(alien)

def create_fleet(screen, ai_settings, ship, aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	for alien_row in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_row, alien_number)
	
def check_keydown_events(stats, event, screen, ai_settings, ship, bullets, aliens, sb):
	if event.key == pygame.K_RIGHT:
		ship.move_right = True
	elif event.key == pygame.K_LEFT:
		ship.move_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(screen, ai_settings, ship, bullets)
	elif event.key == pygame.K_p:
		reset_game(stats, aliens, bullets, screen, ai_settings, ship, sb)
	elif event.key == pygame.K_q:
		sys.exit()
		
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.move_right = False
	elif event.key == pygame.K_LEFT:
		ship.move_left = False

def check_events(screen, ai_settings, ship, bullets, stats, play_button, aliens, sb):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(stats, event, screen, ai_settings, ship, bullets, aliens, sb)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
	if not stats.button_clicked and play_button.rect.collidepoint(mouse_x, mouse_y):
		reset_game(stats, aliens, bullets, screen, ai_settings, ship, sb)

def reset_game(stats, aliens, bullets, screen, ai_settings, ship, sb):
	ai_settings.initialize_dynamic_settings( )
	pygame.mouse.set_visible(False)
	stats.button_clicked = True
	sb.check_high_score()
	stats.reset_stats()
	stats.game_active = True
	aliens.empty()
	bullets.empty()
	sb.pre_score()
	sb.pre_high_score()
	sb.pre_level()
	sb.pre_ships()
	create_fleet(screen, ai_settings, ship, aliens)
	ship.center_ship()

def fire_bullet(screen, ai_settings, ship, bullets):
	if len(bullets) < ai_settings.bullet_allowed:
		bullet = Bullet(screen, ai_settings, ship)
		bullets.add(bullet) 
	
def check_bullets(bullets):
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def update_screen(screen, ai_settings, stats, ship, alien, bullets, play_button, sb):
	screen.fill(ai_settings.bg_color)
	for bullet in bullets:
		bullet.draw_bullet()
	ship.blitme()
	for alien in alien:
		alien.blitme()
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()
