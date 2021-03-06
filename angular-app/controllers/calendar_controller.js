appControllers.controller('calendarCtrl', function($scope, BarmService, $modal){
    $scope.items = {}
    $scope.events = [];
    $scope.selected = {};
    $scope.teams = [];
    $scope.projects = [];
    $scope.selector = [];
    function SearchString (str,arr) {
        for (var i=0; i<arr.length; i++) {
            if (arr[i] == str){
                return true;
            }
        }
        return false;
    }
    /* Setting calendar events during page load/ initialization of the calendar events*/
    $scope.setEvents = function()   {
            $scope.events = [];//clear events model array
            $scope.teams = [];//clear teams/resources model array

            BarmService.getCalendar()//get events from calendar service
            .success(function(data,status)  {

              $scope.resources = data.items;//store temporarily the data into scope-resources
              console.log(data.items);
              p = data.items;
              var dupNames = []; // temporary storage for the list of resource names
              var dupProjects = []; // temporary storage for the list of project names
              for (i=0; i< p.length; i++)   {
                var inputDay = p[i].alloc_date.year+'-'+p[i].alloc_date.month+'-'+p[i].alloc_date.day;//allocated date for the event
        	    var projectName = p[i].project_name;//project name of the event
        	    var resourceName = p[i].resource_name;
        	    var color = p[i].color;
                var cal_id = p[i].calendar_id;
                var alloc_hours = p[i].alloc_hours
                var title = ""+projectName+" ("+alloc_hours+")";
                console.log(inputDay);
    	       if (SearchString(resourceName,dupNames)){ // check if the resources has been added in the dupNames list

               }else{
                dupNames.push(resourceName); //push resource name if not in the list
                $scope.teams.push({name: resourceName, id: i, isChecked:true, color:color});
               }
               if(SearchString(projectName,dupProjects)){

               }else{
                dupProjects.push(projectName);
                $scope.projects.push({name: projectName, id: i, isChecked:true});
               }
                pushEvent(inputDay, title, color,resourceName, projectName,cal_id);
            }
                $scope.startCalendar();
                $scope.allteams = true;
                $scope.allprojects = true;
                //console.log($scope.teams)
            })
            .error(function(data, status){
                $scope.startCalendar();
            });
    };

    function pushEvent(inputDay,title,color, resourceName, projectName,cal_id)    {
        $scope.events.push({title : title,start : ""+inputDay+"",color   : ""+color+"", resourceName: ""+resourceName+"", projectName: ""+projectName+"", alloc_date: ""+inputDay+"", calendar_id: cal_id});
    }


    $scope.refreshCalendar = function() {
            $('#calendar').fullCalendar('removeEventSource',$scope.events);
            $scope.events = [];
            $scope.teams = [];
            $scope.projects = [];
            BarmService.getCalendar()
            .success(function(data,status){
                    $scope.resources = data.items;
                    p = data.items;
                    var dupNames = [];
                    var dupProjects = [];
                for (i=0; i< p.length; i++){
                    var inputDay = p[i].alloc_date.year+'-'+p[i].alloc_date.month+'-'+p[i].alloc_date.day;//allocated date for the event
                    var projectName = p[i].project_name;
                    var resourceName = p[i].resource_name;
                    var color = p[i].color;
                    var alloc_hours = p[i].alloc_hours;
                    var cal_id = p[i].calendar_id;
                    var title = ""+projectName+" ("+alloc_hours+")";
                    if (SearchString(resourceName,dupNames)){

                   }else{
                    dupNames.push(resourceName);
                    $scope.teams.push({name: resourceName, id: i, isChecked:true, color:color});
                   }
                   if(SearchString(projectName,dupProjects)){

                   }else{
                    dupProjects.push(projectName);
                    $scope.projects.push({name: projectName, id: i, isChecked:true});
                   }
                    pushEvent(inputDay, title, color,resourceName, projectName,cal_id);//Push checked projects
                }
                    $('#calendar').fullCalendar('addEventSource',$scope.events);
                })
            .error(function(data, status){

            });
    };

    //function to calculate window height
    function get_calendar_height() {
          return $(window).height() - 300;
    }

    $scope.startCalendar = function()   {
        // page is now ready, initialize the calendar...
        $('#calendar').fullCalendar({
            // put your options and callbacks here
            header: {
                left: ' today',
                center: 'prev , title ,next',
                right: 'month,basicWeek,basicDay',
            },
            defaultView: 'basicWeek',
            events: $scope.events,
            eventLimit: true, // allow "more" link when too many events
            editable: true,
            eventDurationEditable : false,
            theme: false,
            height: get_calendar_height(),
            //weekends: false,
            contentHeight: get_calendar_height(),
            eventClick: function(calEvent, jsEvent, view)   {
                var modalInstance = $modal.open(  {
                          templateUrl: 'ng/templates/modal/addTaskModal.html',
                          controller: 'taskCtrl',
                          size: 'lg',
                          resolve:{
                              items: function (){
                                    return calEvent;
                               }
                          }
                      });
                /*
                alert('Event: ' + calEvent.title);
                console.log(calEvent.start);
                alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
                alert('View: ' + view.name);

                // change the border color just for fun
                $(this).css('border-color', 'red');
                */

            }


        });
        //console.log($scope.events);

    };

    $(document).ready(function() {
        $scope.setEvents();
        $(window).resize(function() {
            $('#calendar').fullCalendar('option', 'contentHeight', get_calendar_height());
        });
    });


    $scope.getResource = function(params)   {
        var t = $scope.teams;
        var name_list = [];

        for (i=0; i< t.length; i++){
            if(t[i].isChecked == true){
                name_list.push(t[i].name);
            }
        }
        //console.log(name_list);

        $('#calendar').fullCalendar('removeEventSource',$scope.events);
            $scope.events = [];
            BarmService.getCalendar()
            .success(function(data,status)  {

              p = data.items;
              for (i=0; i< p.length; i++)   {
                var inputDay = p[i].alloc_date.year+'-'+p[i].alloc_date.month+'-'+p[i].alloc_date.day;//allocated date for the event
                var projectName = p[i].project_name;
                var resourceName = p[i].resource_name;
                var color = p[i].color;
                var cal_id = p[i].calendar_id;
                var alloc_hours = p[i].alloc_hours
                var title = ""+projectName+" ("+alloc_hours+")";
                  for(n=0; n<name_list.length; n++) {
                   if (name_list[n] == resourceName){
                     pushEvent(inputDay, title, color,resourceName, projectName,cal_id);//Push checked projects
                   }
        		  }
            }//end for checking of allocated hours
            $('#calendar').fullCalendar('addEventSource',$scope.events);
        })
        .error(function(data,status){

        });
    }

    $scope.getProjects = function  (params) {
        var p = $scope.projects;
        //$scope.teams = [];
        //console.log($scope.projects)
        var proj_list = [];
        for (var i = p.length - 1; i >= 0; i--) {
            if(p[i].isChecked == true)  {
                proj_list.push(p[i].name);
            }
        };

        $('#calendar').fullCalendar('removeEventSource', $scope.events);
            $scope.events = [];
            BarmService.getCalendar()
                .success(function (data, status) {
                    d = data.items;
                    var dupNames = [];
                    for(i=0; i<d.length; i++)   {
                        var inputDay = d[i].alloc_date.year+'-'+d[i].alloc_date.month+'-'+d[i].alloc_date.day;//allocated date for the event
                        var projectName = d[i].project_name;
                        var resourceName = d[i].resource_name;
                        var color = d[i].color;
                        var cal_id = d[i].calendar_id;
                        var alloc_hours = d[i].alloc_hours
                        var title = ""+projectName+" ("+alloc_hours+")";
                          for(n=0; n<proj_list.length; n++) {
                                if(proj_list[n] == projectName){
                            pushEvent(inputDay, title, color,resourceName, projectName,cal_id);//Push checked projects
                            }
                        }
                    }

                        //end for checking of allocated hours
                    $('#calendar').fullCalendar('addEventSource',$scope.events);
                })
                .error(function(data,status){

                });
    }

    $scope.selectAll = function(params){
        if($scope.allteams == true){
            $scope.refreshCalendar();
        }else{
            $('#calendar').fullCalendar('removeEventSource', $scope.events);
            $scope.events = [];
            uncheckResources();
            $('#calendar').fullCalendar('removeEventSource', $scope.events);
        }
    }

    function uncheckResources(){
        for (i=0; i<$scope.teams.length; i++){
            $scope.teams[i].isChecked = false;
        }
        for (var i = $scope.projects.length - 1; i >= 0; i--) {
            $scope.projects[i].isChecked = false;
        };
    }
});
