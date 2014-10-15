(function(angular) {'use strict';

var app = angular.module('foodpedia', ['foodpedia.ctrl', 'ngRoute']);

app.config(['$routeProvider', function($routeProvider) {
        $routeProvider
        .when('/', {
            templateUrl: 'partials/main.html',
            controller: 'SearchCtrl'
        })
        .otherwise({redirectTo: '/'});
}]);

app.config(function(ngProgressProvider) {
    ngProgressProvider.setColor('#6aa84f');
    ngProgressProvider.setHeight('2px');
});

var sparqlConfig = angular.module('ngSPARQL.config', []);
    sparqlConfig.constant(
        'SPARQL_CONFIG', {
            PREFIXES: {
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#'
            },
            ENDPOINTS: {
                ENDPOINT_1: "http://foodpedia.tk/sparql-cors"
            }
        }
    );

})(window.angular);