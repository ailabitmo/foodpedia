(function(angular) {'use strict';

var app = angular.module('foodpedia', [
    'foodpedia.ctrl', 'ngRoute', 'pascalprecht.translate']);

app.config(['$routeProvider', function($routeProvider) {
        $routeProvider
        .when('/', {
            templateUrl: 'partials/main.html',
            controller: 'SearchCtrl'
        })
        .otherwise({redirectTo: '/'});
}]);

app.config(function(ngProgressProvider, $translateProvider) {
    ngProgressProvider.setColor('#6aa84f');
    ngProgressProvider.setHeight('2px');
    
    $translateProvider.translations('en', {
        BUTTON_SEARCH: 'Search',
        HEADER_RESULTS: 'Results (total {{length}}):',
        SEARCH_PLACEHOLDER: '"4607081352675" or "milk"',
        ALERT_EMPTY: 'Oh! You\'ve entered an empty query.',
        ALERT_ERROR: 'Oops, an error occurred! Try again later.'
    });
    
    $translateProvider.translations('ru', {
        BUTTON_SEARCH: 'Поиск',
        HEADER_RESULTS: 'Результаты поиска (всего {{length}}):',
        SEARCH_PLACEHOLDER: '"4607081352675" или "макаронные изделия"',
        ALERT_EMPTY: 'Ой! Вы ввели пустой запрос.',
        ALERT_ERROR: 'Упс, произошла ошибка! Попробуйте позже.'
    });
    
    $translateProvider.preferredLanguage('ru');
});

var sparqlConfig = angular.module('ngSPARQL.config', []);
    sparqlConfig.constant(
        'SPARQL_CONFIG', {
            PREFIXES: {
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#',
                'food': 'http://purl.org/foodontology#',
                'foodpedia-owl': 'http://foodpedia.tk/ontology#',
                'gr': 'http://purl.org/goodrelations/v1#'
            },
            ENDPOINTS: {
                ENDPOINT_1: "${endpoint.url}"
            }
        }
    );

})(window.angular);
