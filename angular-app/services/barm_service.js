appServices.service('BarmService', function($http){
    return {
    addPerson: function(params){
        return $http.post('/api/persons/create', params);
    },
    addProject: function(params){
        return $http.post('/api/projects/create', params);
    },
    getProjects: function(){
	return $http.get('/api/projects/list', {});
    },
    deleteProject: function(key){
    return $http.delete('/api/projects/:'+key.urlsafe);
    },
    updateProject: function(params){
	return $http.post('/api/projects/:'+params.key.urlsafe, params);
    },
    addAllocation: function(params){
	return $http.post('/api/allocations/create', params);
    },
    getAllocation: function(){
	return $http.get('/api/allocations/list');
    },
    findAllocation: function(key){
    return $http.get('/api/allocations/:'+key);
    },
    findEvent: function(key){
    return $http.get('/api/allocations/find/:'+key);
    },
    addEvent: function(params){
    return $http.post('/api/events/create', params);
    },
    loadEvent: function(key){
    return $http.get('/api/events/find/:'+key);
    },
    updateEvent: function(params){
    return $http.post('/api/events/:'+params.key.urlsafe, params);
    },
    deleteEvent: function(key){
    return $http.delete('/api/events/:'+key.urlsafe);
    },
    deleteAllocation: function(key){
    return $http.delete('/api/allocations/:'+key);
    },
    getAllResources: function(){
        return $http.get('/api/persons/list');
    },
    getCalendar: function(){
	return $http.get('/api/calendars/list');
    },
    getTasks: function(){
    return $http.get('/api/tasks/list');
    },
    addTask: function(params){
    return $http.post('/api/tasks/create', params);
    },
    updateTask: function(params){
    return $http.post('/api/tasks/:'+params.key.urlsafe, params);
    }


    };
});
