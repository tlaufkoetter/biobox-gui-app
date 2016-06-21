(function () {
    'use strict';

    angular
        .module('BioboxGui')
        .factory('bioboxService', bioboxService);

    function bioboxService($http) {
        var service = {
            getBiobox: getBiobox,
            getBioboxes: getBioboxes,
            updateBioboxes: updateBioboxes,
            getInterface: getInterface,
            getInterfaces: getInterfaces,
            queryStates: queryStates,
            addSource: addSource,
            deleteTask: deleteTask
        }
        return service;

        function addSource(source) {
            return $http.post('/bioboxgui/api/sources', source)
        };

        function getBioboxes() {
            return $http.get('/bioboxgui/api/bioboxes');
        };

        function getBiobox(id) {
            return $http.get('bioboxgui/api/bioboxes/' + id);
        };

        function updateBioboxes() {
            return $http.put('/bioboxgui/api/bioboxes');
        };

        function getInterfaces() {
            return $http.get('/bioboxgui/api/interfaces');
        };

        function getInterface(selectedInterface) {
            return $http.get('/bioboxgui/api/bioboxes?interface=' + selectedInterface);
        };

        function queryStates() {
            return $http.get('/bioboxgui/api/states');
        };

        function submitTask(user, container, cmd, file) {
            var task = {};
            task.user = user;
            task.container = container;
            task.cmd = cmd;
            task.file = file;
            return $http.post('/bioboxgui/api/states', task);
        };

        function deleteTask(id) {
            return $http.delete('/bioboxgui/api/states/' + id);
        };

    };
})();
