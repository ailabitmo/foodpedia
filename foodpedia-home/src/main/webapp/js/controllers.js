(function(angular, console){
    var module = angular.module('foodpedia.ctrl', ['ngProgress']);
    
    module.controller('SearchCtrl', function($scope, $window, $translate) {
        $scope.loading = false;
        
        $scope.send = function() {
            if($scope.search) {
                $window.location.href = '/search?q=' + $scope.search 
                        + '&lang=' + $translate.use()
                        + '&offset=0';
            } else {
                $translate('ALERT_EMPTY').then(function(translation) {
                    alert(translation);
                });
            }
        };
    });
    
    module.controller('LangCtrl', function($scope, $translate) {
        $scope.changeLanguage = function(langKey) {
            $translate.use(langKey);
        };
    });
    
})(window.angular, window.console);
