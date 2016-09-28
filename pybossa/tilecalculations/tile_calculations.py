from StringIO import StringIO
import base64
from pybossa.tilecalculations.tileinfo import tileInfo

tileInfo = tileInfo()

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
        print task_data
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
        api_key  = 'AtAixlkrsDwLlwTwXFZqpVP9nKyV-KbP5TbBJHWAIDVaovuYWZOHCKvUOksICp8t' #config.get("API_KEY")
        tile_url = ("http://t0.tiles.virtualearth.net/tiles/a{}.jpeg?g=854&mkt=en-US&token={}".format(quadKey, api_key))
        response = self.stream_image(tile_url)
        return response

    def stream_image(self, url):
        w = tileInfo.Info(url)
        img_source = self.html_image(w.content, w.content_type)
        return img_source

    def html_image(self, data, content_type):
        f = StringIO(data)
        encoded = base64.b64encode(f.read())
        return "data:{};base64,{}".format(content_type, encoded)
