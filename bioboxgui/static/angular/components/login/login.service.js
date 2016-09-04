(function () {
    'use strict';

    angular
        .module('BioboxGui')
        .factory('loginService', loginService);

    function loginService($http, $log, $q, $route, sessionService) {
        var service = {
            login: login,
            logout: logout
        };
        return service;

        function login(user) {
            return $http.post('/bioboxgui/api/token', user)
                .then(
                        function(response) {
                            $log.info("logged in: ", user);
                            var token = response.data.token;
                            var roles = response.data.roles;
                            if (token && roles) {
                                user.authentication_token = token;
                                user.roles = roles;
                                sessionService.setCurrentUser(user);
                            } else {
                                return $q.reject(reponse.status);
                            }
                        },
                        function(response) {
                            $log.warn("login failed: ", response);
                            return $q.reject(response.status);
                        }
                     );
        }

        function logout() {
            return $http.delete('/bioboxgui/api/token')
                .then(
                        function(response) {
                            $log.info("logged out");
                            sessionService.setCurrentUser(null);
                            $route.reload();
                        }
                     );
        }
    };
})();
