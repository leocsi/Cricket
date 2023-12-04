'''This module is used to store frequently stored colors and palettes in RGB and HSV format.'''

from exceptions.light_server_exceptions import ColorCreationException
import colorsys

class Color:
    def __init__(self, **kwargs: 'dict[str:str]'):
        '''Constructor for a `Color` object, takes exactly one named parameter, 
        which specifies what color to create. The values you can use are hex|rgb|hsv
        stores the color in Yeelight required format
        
        Example:
        >>> Color(hex='31CFE0')
        >>> Color(rgb='49,207,224')
        >>> Color(hsv='186,78,88')
        '''
        if len(kwargs) > 1:
            raise ColorCreationException(kwargs, 'Please specify only one way to create color')
        if len(kwargs) == 0:
            raise ColorCreationException(kwargs, 'Please specify what color you\'d like to create. ')
        

        allowed_params = ['hex', 'rgb','hsv']
        param = list(kwargs.keys())[0]
        if param not in allowed_params:
            raise ColorCreationException(kwargs, 'Please specify what color you\'d like to create. ')
        
        value = kwargs[param]

        if param == 'hex':
            self.color = int(value, 16)
        else:
            numbers = [int(n) for n in value.split(',')]
            if param == 'hsv':
                numbers = [int(round(col * 255)) for col in colorsys.hsv_to_rgb(*numbers)]

            self.color = numbers[0] * 65536 + numbers[1] * 256 + numbers[2]

class ColorStore:
    COLORS = {
        'blue' : Color(hex='1674F0'),
        'sky_blue' : Color(hex='00A4F0'),
        'turquoise' : Color(hex='00FFBC'),
        'mint' : Color(hex='0AEF45'),
        'aqua_green': Color(hex='16F096')
    }

    PALETTES = {
        'aurora_borealis' : ['blue', 'sky_blue', 'turquoise', 'aqua_green','mint']
    }

    @staticmethod
    def get_multiple(names: 'list[str]') -> 'list[Color]':
        colors = []
        for name in names:
            colors.append(ColorStore.COLORS[name])
        return colors

    @staticmethod
    def get_palette(palette_name: str) -> 'list[Color]':
        palette = ColorStore.PALETTES[palette_name]
        return ColorStore.get_multiple(palette)
