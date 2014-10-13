(function(angular, console){
    var module = angular.module('foodpedia.ctrl', ['ngSPARQL']);
    
    module.controller('SearchCtrl', function($scope, sparql) {
       $scope.send = function() {
           if($scope.search) {
               sparql.select("SELECT ?product ?name ?barcode {?product a food:Food ; gr:name ?name ;gr:hasEAN_UCC-13 ?barcode .{?product gr:name ?value . ?value bif:contains \"'" + $scope.search + "'\".}UNION{?product gr:hasEAN_UCC-13 ?value . ?value bif:contains \"'" + $scope.search + "'\".}}"
                ).then(function(products) {
                    $scope.products = products;
                }, function(){
                    alert('Упс, произошла ошибка! Попробуйте позже.');
                });
           } else {
               alert('Ой! Вы ввели пустой запрос.');
           }
       }; 
    });
    
})(window.angular, window.console);