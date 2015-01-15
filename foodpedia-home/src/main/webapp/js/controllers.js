(function(angular, console){
    var module = angular.module('foodpedia.ctrl', ['ngSPARQL', 'ngProgress']);
    
    module.controller('SearchCtrl', function($scope, sparql, ngProgress) {
        $scope.loading = false;
        $scope.send = function() {
            if($scope.search) {
                $scope.loading = true;
                ngProgress.start();
                sparql.select("SELECT DISTINCT ?product ?name ?barcode where {?product a food:Food ; gr:name ?name ;gr:hasEAN_UCC-13 ?barcode . ?product gr:name ?value . FILTER ( STR(?barcode) = '" + $scope.search + "' || regex(STR(?name), '" + $scope.search + "', 'i'))}"
                 ).then(function(products) {
                     products.forEach(_updateProductWithPubbyURL);
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

        var _updateProductWithPubbyURL = function(product) {
            product.pubbyURL = _formPubbyURL(product);
        }
	var _formPubbyURL = function(product){
            return "${pubby.url}" + product.barcode;
        }

    });
    
})(window.angular, window.console);
