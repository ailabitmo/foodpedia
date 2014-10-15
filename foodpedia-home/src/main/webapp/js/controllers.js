(function(angular, console){
    var module = angular.module('foodpedia.ctrl', ['ngSPARQL', 'ngProgress']);
    
    module.controller('SearchCtrl', function($scope, sparql, ngProgress) {
        $scope.loading = false;
        $scope.send = function() {
            if($scope.search) {
                $scope.loading = true;
                ngProgress.start();
                sparql.select("SELECT ?product ?name ?barcode {?product a food:Food ; gr:name ?name ;gr:hasEAN_UCC-13 ?barcode .{?product gr:name ?value . ?value bif:contains \"'" + $scope.search + "'\".}UNION{?product gr:hasEAN_UCC-13 ?value . ?value bif:contains \"'" + $scope.search + "'\".}}"
                 ).then(function(products) {
                     $scope.products = products;
                     $scope.loading = false;
                     ngProgress.complete();
                 }, function(){
                     $scope.loading = false;
                     ngProgress.complete();
                     alert('Упс, произошла ошибка! Попробуйте позже.');
                 });
            } else {
                alert('Ой! Вы ввели пустой запрос.');
            }
        };
    });
    
})(window.angular, window.console);