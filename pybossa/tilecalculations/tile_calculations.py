from bson import json_util
import json
class TileCalculations():

    def tile_cords_and_zoom_to_quadKey_and_url(self, data):
        task_data = []
        zoom = int(data['zoom'])
        for i in range(1, 13):
            tile = {}
            x_index = 'x'+str(i)
            y_index = 'y'+str(i)
            x = int(data[x_index])
            y = int(data[y_index])
            quad_key = self.tile_cords_and_zoom_to_quadKey(x, y, zoom)
            url = self.quadKey_to_url(quad_key)
            tile = {x_index: x,
                    y_index: y,
                    "quad_key": quad_key,
                    "url": url,
                    "zoom": zoom}
            task_data.append(tile)
        return task_data


    def tile_cords_and_zoom_to_quadKey(self, x, y, zoom):
        quadKey = ''
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if(x & mask) != 0:
                digit += 1
            if(y & mask) != 0:
                digit += 2
            quadKey += str(digit)
        return quadKey

    def quadKey_to_url(self, quadKey):
        #FIX: BING_MAPS_API_KEY -  get api key from local settings
        api_key  = 'AtAixlkrsDwLlwTwXFZqpVP9nKyV-KbP5TbBJHWAIDVaovuYWZOHCKvUOksICp8t' 
        tile_url = ("http://t0.tiles.virtualearth.net/tiles/a{}.jpeg?g=854&mkt=en-US&token={}".format(quadKey, api_key))
        return tile_url