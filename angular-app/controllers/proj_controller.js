appControllers.controller('projectCtrl', function ($scope, $modalInstance, items, BarmService){
    $scope.project = {}; //model for project
    $scope.data = {} //return data fron service to be returned
    $scope.items = items;
    $scope.selected = $scope.items[0];
    //Configurations for datepicker angular bootstrap

    $scope.open = function($event) {
    	$event.preventDefault();
    	$event.stopPropagation();

    	$scope.opened = true;
    };

    $scope.formats = ['dd-MMMM-yyyy','MM/dd/yyyy', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[1];

    $scope.ok = function(){

    	if($scope.project['name'] == null || $scope.project['name'] == '') {
    	    $("#namer_err").focus();
    	    //setTimeout( $("#hour_err").hide(), 3000);
    	}else if($scope.project['billable_hours'] == null || $scope.project['billalbe_hours' ]== '')   {
    	    $("#hour_err").focus();
    	    //setTimeout( $("#resource_err").hide(), 3000);
    	}else if($scope.project['start_date'] == null || $scope.project['start_date'] == '')   {
    	    $("#dateString").focus();
    	}else  {
            var dateString = $('#dateString').val();
            var timestamp = Date.parse(dateString).getTime()/1000;
            $scope.project['start_date'] = timestamp;
            BarmService.addProject($scope.project)
        	.success(function(data, status){
        	    $scope.data = data.name+", "+data.total_hours;
                $("#ok-btn").addClass("btn-disabled").html("<span id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> saving...");
                    setTimeout(function()   {
                        $("#ok-btn").removeClass("btn-disabled").html("Saved!");
                    }, 1000);

                    setTimeout(function()   {
                        $modalInstance.dismiss('cancel');
                    } , 2000);
		})
        	.error(function(data, status){
        	    $("#error_msg").removeClass().addClass("text text-danger").html("Add Project Failed!");
        	});
        }
    }

    $scope.cancel = function () {
	   $modalInstance.dismiss('cancel');
    };

});



