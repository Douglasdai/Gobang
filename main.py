import pygame
from pygame.locals import *
from FiveGameMap import *
from ChessAI import *
import sys
import copy
class Button():
    def __init__(self,screen,text,x,y,color,enable):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = color
        self.text_color = (255,255,255)
        self.enable = enable
        self.font = pygame.font.SysFont('SimHei',BUTTON_HEIGHT *2//3)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.topleft = (x,y)
        self.text = text
        self.init_msg()
    
    def init_msg(self):
        if self.enable:
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[0])
        else:
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw(self):
        if self.enable:
            self.screen.fill(self.button_color[0],self.rect)
        else:
            self.screen.fill(self.button_color[1],self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

class StartButton(Button):
    def __init__(self,screen,text,x,y):
        super().__init__(screen,text,x,y,[(26,173,25),(158,217,157)],True)
    
    def click(self,game):
        if self.enable:
            game.start()
            game.winner = None
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[1])
            self.enable = False
            return True
        return False
    
    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[0])
            self.enable = True
    
class GiveUpButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(230,67,64),(236,139,137)],False)
    
    def click(self,game):
        if self.enable:
            game.is_play = False
            if game.winner is None:
                game.winner = game.map.reverseTurn(game.player)
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[1])
            self.enable =False
            return True
        return False
    
    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[0])
            self.enable = True
#TODO
class RegretButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(26,173,25),(	127,255,170)],False)

    def click(self,game):
        game.map = game.map_old
        #game.map_old =
        # if self.enable:
        #     game.is_play = False
        #     if game.winner is None:
        #         game.winner = game.map.reverseTurn(game.player)
        #     self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[1])
        #     self.enable =False
        #     return True
        # return False
    
    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[0])
            self.enable = True
#TODO
class QuitButton(Button):
    def __init__(self, screen, text, x, y,):
        super().__init__(screen, text, x, y,  [(26,173,25),(127,255,170)],True)

    def click(self,game):
        pygame.quit()
        sys.exit()
        
    def unclick(self):
        self.msg_image = self.font.render(self.text,True,self.text_color,self.button_color[0])
        self.enable = True
        # game.quit()
        # sys.exit()
    

class Game():
    def __init__(self,caption,play_mode,AI_first):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        pygame.display.set_caption(caption)
        #循环播放bgm
        pygame.mixer.music.load('fivechess_bgm.mp3')
        pygame.mixer.music.play(-1)
        #五子棋图标Icon
        pygame.display.set_icon(pygame.image.load('fivechess_png.png'))
        self.clock = pygame.time.Clock()
        self.mode = play_mode
        self.buttons = []
        self.buttons.append(StartButton(self.screen,'开始',MAP_WIDTH+30,15))
        self.buttons.append(GiveUpButton(self.screen,'放弃',MAP_WIDTH+30,BUTTON_HEIGHT+45))
        self.buttons.append(RegretButton(self.screen,'悔棋',MAP_WIDTH+30,BUTTON_HEIGHT*2+75))
        self.buttons.append(QuitButton(self.screen,'退出',MAP_WIDTH+30,BUTTON_HEIGHT*3+100))
        self.is_play = False

        self.map  = Map(CHESS_LEN,CHESS_LEN)
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE
        self.action = None
        self.AI = ChessAI(CHESS_LEN)
        self.AI_first = AI_first
        self.winner = None
    
    def start(self):
        self.is_play =True
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE
        self.map.reset()
        self.AI.number = 0
        if (self.mode ==USER_VS_AI_MODE and self.AI_first) or self.mode ==AI_VS_AI_MODE:
            self.useAI = True
        else:
            self.useAI = False
    
    def play(self):
        self.clock.tick(60)
        light_yellow = (247,238,214)
        pygame.draw.rect(self.screen,light_yellow,pygame.Rect(0,0,MAP_WIDTH,MAP_HEIGHT ))
        pygame.draw.rect(self.screen,(255,255,255),pygame.Rect(MAP_WIDTH,0,INFO_WIDTH,SCREEN_HEIGHT))

        for button in self.buttons:
            button.draw()
        #TODO
        #self.map_old = copy.deepcopy(self.map)
        if self.is_play and not self.isOver():
            if self.useAI:
                x,y = self.AI.findBestChess(self.map.map, self.player)
                self.checkClick(x,y,True)
                if self.mode == USER_VS_AI_MODE:
                    self.useAI =False
            if self.mode != AI_VS_AI_MODE:
                if self.action is not None:
                    self.checkClick(self.action[0],self.action[1])
                    self.action =None
                    if self.mode ==USER_VS_AI_MODE:
                        self.showAIThink()
        
                if not self.isOver():
                    self.changeMouseShow()
        
        if self.isOver():
                self.showWinner()
        #self.map_old = copy.deepcopy(self.map)
        self.map.drawBackground(self.screen)
        self.map.drawChess(self.screen)

    def changeMouseShow(self):
        map_x,map_y = pygame.mouse.get_pos()
        x,y = self.map.MapPosToIndex(map_x,map_y)
        if self.map.isInMap(map_x,map_y) and self.map.isEmpty(x,y):
            pygame.mouse.set_visible(False)
            light_red = (213,90,107)
            pos, radius = (map_x,map_y),CHESS_RADIUS
            pygame.draw.circle(self.screen,light_red,pos,radius)
        else:
            pygame.mouse.set_visible(True)
    
    def checkClick(self,x,y,isAI = False):
        self.AI.click(self.map,x,y,self.player)
        if self.AI.isWin(self.map.map,self.player):
            self.winner =self.player
            self.click_button(self.buttons[1])
        else:
            self.player = self.map.reverseTurn(self.player)
            if not isAI and self.mode != USER_VS_USER_MODE:
                self.useAI =True
            
    def mouseClick(self,map_x,map_y):
        if self.is_play and self.map.isInMap(map_x,map_y) and not self.isOver():
            x,y = self.map.MapPosToIndex(map_x,map_y)
            if self.map.isEmpty(x,y):
                self.action = (x,y)
    
    def isOver(self):
        return self.winner is not None
    
    def showFont(self,text,location_x,location_y,height):
        font = pygame.font.SysFont(None,height)
        font_image = font.render(text,True,(0,0,255),(255,255,255))
        font_image_rect = font_image.get_rect()
        font_image_rect.x = location_x
        font_image_rect.y = location_y
        self.screen.blit(font_image,font_image_rect)
    
    def showAIThink(self):
        self.showFont('AI is thinking ... ',MAP_WIDTH+25,SCREEN_HEIGHT//2-30,30)
    
    def showWinner(self):
        if self.winner ==MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            str ='Winner is White'
        else:
            str = 'Winner is Black'
        self.showFont(str,MAP_WIDTH+25,SCREEN_HEIGHT-60,30)
        pygame.mouse.set_visible(True)
    
    def click_button(self,button):
        if button.click(self):
            for tmp in self.buttons:
                if tmp !=button:
                    tmp.unclick()
    
    def check_buttons(self,mouse_x,mouse_y):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_x,mouse_y):
                self.click_button(button)
                break
    
def USER_AI():
    game = Game('Five Chess'+GAME_VERSION,GAME_PLAY_MODE,AI_RUN_FIRST)
    while True:
        game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                game.mouseClick(mouse_x,mouse_y)
                game.check_buttons(mouse_x,mouse_y)

def USER_USER():
    GAME_PLAY_MODE = 0
    game = Game('Five Chess'+GAME_VERSION,GAME_PLAY_MODE,AI_RUN_FIRST)
    while True:
        game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                game.mouseClick(mouse_x,mouse_y)
                game.check_buttons(mouse_x,mouse_y)

def AI_AI():
    GAME_PLAY_MODE =2
    game = Game('Five Chess'+GAME_VERSION,GAME_PLAY_MODE,AI_RUN_FIRST)
    while True:
        game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                game.mouseClick(mouse_x,mouse_y)
                game.check_buttons(mouse_x,mouse_y)

# if __name__ =='__main__':
#     main()


