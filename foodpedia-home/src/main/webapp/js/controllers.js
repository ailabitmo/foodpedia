(function(angular, console){
    var module = angular.module('foodpedia.ctrl', ['ngSPARQL', 'ngProgress']);
    
    module.controller('SearchCtrl', function($scope, sparql, ngProgress, $translate) {
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
                 }, function() {
                     $scope.loading = false;
                     ngProgress.complete();
                    $translate('ALERT_ERROR').then(function(translation) {
                        alert(translation);
                    });
                 });
            } else {
                $translate('ALERT_EMPTY').then(function(translation) {
                    alert(translation);
                });
            }
        };

        var _updateProductWithPubbyURL = function(product) {
            product.pubbyURL = _formPubbyURL(product);
        };
	var _formPubbyURL = function(product){
            return "${pubby.url}" + product.barcode;
        };

    });
    
    module.controller('LangCtrl', function($scope, $translate) {
        $scope.changeLanguage = function(langKey) {
            $translate.use(langKey);
        };
    });
    
})(window.angular, window.console);
