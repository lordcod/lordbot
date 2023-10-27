import nextcord
from nextcord import ui,utils
from typing import Union

sym =  '   '

class Main(ui.View):
    def __init__(self,value:list):
        super().__init__(timeout=None)
        self.len = len(value)-1
        self.index = 0
        self.value = value
    
    def custom_emoji(self,**kwargs):
        for kw in kwargs:
            atr = getattr(self,f'button_{kw}')
            atr.emoji = kwargs[kw]
    
    async def handler_disable(self):
        if self.index > 0:
            self.button_previous.disabled = False 
            self.button_backward.disabled = False 
        
        if self.index <= 0:
            self.button_previous.disabled = True  
            self.button_backward.disabled = True 
        
        if self.index < self.len:
            self.button_forward.disabled = False
            self.button_next.disabled = False
        
        if self.index >= self.len:
            self.button_forward.disabled = True
            self.button_next.disabled = True
    
    async def previous(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    
    async def backward(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    
    async def forward(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    
    async def next(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    
    def add_element(self,val):
        self.value.append(val)
        self.len += 1
    
    def renove_element(self,val):
        self.value.remove(val)
        self.len -= 1
    
    @ui.button(emoji='⏮',style=nextcord.ButtonStyle.grey,disabled=True)
    async def button_previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.index = 0
        await self.handler_disable()
        await self.previous(button,interaction)
        
    @ui.button(emoji='◀️',style=nextcord.ButtonStyle.grey,disabled=True)
    async def button_backward(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.index -= 1
        await self.handler_disable()
        await self.backward(button,interaction)
    
    @ui.button(emoji='▶',style=nextcord.ButtonStyle.grey,custom_id='12girni3')
    async def button_forward(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.index += 1
        await self.handler_disable()
        await self.forward(button,interaction)
    
    @ui.button(emoji='⏭',style=nextcord.ButtonStyle.grey)
    async def button_next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.index = self.len
        await self.handler_disable()
        await self.next(button,interaction)