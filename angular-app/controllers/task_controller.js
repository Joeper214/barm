appControllers.controller('taskCtrl', function ($scope, $modalInstance, items, BarmService)  {


    $scope.task = {};
    $scope.loadTasks = function(){
        $scope.items = {};
        $scope.items = items;
        BarmService.getTasks()
            .success(function (data,status){
                var p = data.items;
                console.log($scope.items);
                for (i=0; i<p.length; i++){
                    if(p[i].calendar_id == $scope.items.calendar_id){

                        $scope.task['taskContent'] = p[i].taskContent;
                        $scope.task['key'] = p[i].key;
                    }
                }
            })
            .error(function(data,status){

            });
    };

    $scope.ok = function(){
        if($scope.task['taskContent'] == '' || $scope.task['taskContent'] == null){
              $("#name_err").focus();
        }else{
            addUpdateTask();
        }
    }

    function addUpdateTask(){
                $("#ok-btn").addClass("btn-disabled").html("<span id='loading' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> saving...");
            $scope.task['calendar_id'] = $scope.items.calendar_id;
            if($scope.task['key'] == '' || $scope.task['key'] == null){
                BarmService.addTask($scope.task)
                    .success(function (data,status){
                        loadingDiag();
                    })
                    .error(function(data,status){

                    });
            }else{
                BarmService.updateTask($scope.task)
                    .success(function(data,status){
                        loadingDiag();
                    })
                    .error(function(data,status){

                    });
            }

    }

    function loadingDiag(){

        setTimeout(function()   {
            $("#ok-btn").removeClass("btn-disabled").html("Saved!");
        }, 1000);

        setTimeout(function()   {
            $modalInstance.dismiss('cancel');
        } , 2000);
    }



    $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
    };

    $scope.loadTasks();

});



