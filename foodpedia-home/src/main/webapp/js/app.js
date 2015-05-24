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
        TITLE: 'FOODpedia - Food Products and ingredients as Linked Data Dataset',
        BUTTON_SEARCH: 'Search',
        HEADER_RESULTS: 'Results (total {{length}}):',
        SEARCH_PLACEHOLDER: '"4607081352675" or "milk"',
        ALERT_EMPTY: 'Oh! You\'ve entered an empty query.',
        ALERT_ERROR: 'Oops, an error occurred! Try again later.',
        THUMB_EXPLORE: 'Explore',
        THUMB_USE: 'Use',
        THUMB_ABOUT: 'About',
        THUMB_ABOUT_CONTENT: ''
    });
    
    $translateProvider.translations('ru', {
        TITLE: 'FOODpedia - База связанных данных (Linked Data) о продуктах питания и ингредиентах',
        BUTTON_SEARCH: 'Поиск',
        HEADER_RESULTS: 'Результаты поиска (всего {{length}}):',
        SEARCH_PLACEHOLDER: '"4607081352675" или "макаронные изделия"',
        ALERT_EMPTY: 'Ой! Вы ввели пустой запрос.',
        ALERT_ERROR: 'Упс, произошла ошибка! Попробуйте позже.',
        THUMB_EXPLORE: 'Исследовать',
        THUMB_USE: 'Использовать',
        THUMB_ABOUT: 'О проекте',
        THUMB_ABOUT_CONTENT: ''
    });
    
    $translateProvider.preferredLanguage('ru');
});

})(window.angular);
