# This file is part of FoodPuter.

#     Foobar is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import pygame


pygame.init()

deny_snd = pygame.mixer.Sound("./Sound/cantdo.wav")
start_snd = pygame.mixer.Sound("./Sound/playgame.wav")
coin_snd = pygame.mixer.Sound("./Sound/31377__freqman__27-coins.wav")

def deny():
    deny_snd.play()


