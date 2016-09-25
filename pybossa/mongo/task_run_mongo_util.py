from pybossa.mongo.base_mongo_util import BaseMongoUtil

class TaskRunMongoUtil(BaseMongoUtil):
    def __init__(self):
        super(TaskRunMongoUtil, self).__init__('taskruns')


	def validate_human_presence(self, redundancy, project_id=None, task_id=None):
	    if project_id and task_id:
	        data = self.consolidate_redundancy(project_id, task_id)
	    elif project_id:
	        data = self.consolidate_redundancy(project_id)
	    elif task_id:
	        data = self.consolidate_redundancy(task_id)
	    else:
	        data = self.consolidate_redundancy()

	    results = []
	    for item in data:
	        if 'tiles' in item:
	            redundancy_tile = {}
	            redundancy_tile['zoom'] = 10  #FIX: item['zoom']
	            redundancy_tile['task_id'] = item['task_id']
	            tiles = item['tiles']
	            for tile in tiles:
	                if tile['true'] >= redundancy and tile['true'] > tile['false']:
	                    redundancy_tile['x'] = tile['x']
	                    redundancy_tile['y'] = tile['y']
	                    redundancy_tile['true'] = tile['true']
	                results.append(redundancy_tile)
	    return results