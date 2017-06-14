/*
 * Copyright 2017 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

'use strict';

(function () {

    var ServiceNowQueryTileViewController = function ($scope, ServiceNowQueryService, XlrTileHelper) {
        var vm = this;
        var tile;

        var predefinedColors = [];
        predefinedColors['New'] = '#7E827A';
        predefinedColors['Active'] = '#4AA0C8';
        predefinedColors['Open'] = '#FFA500';
        predefinedColors['Awaiting Problem'] = '#7E8AA2';
        predefinedColors['Awaiting User Info'] = '#7FB2F0';
        predefinedColors['Awaiting Evidence'] = '#45BF55';
        predefinedColors['Resolved'] = '#FFE11A';
        predefinedColors['Closed'] = '#FFA500';


        var colorPool = [
            '#B85C5A',
            '#35203B',
            '#644D52',
            '#8E2800',
            '#FF8598',
            '#FF6F69',
            '#F77A52',
            '#FCD364',
            '#FFE11A'
        ];


        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
        } else {
            // details mode
            tile = $scope.xlrTileDetailsCtrl.tile;
        }

        function tileConfigurationIsPopulated() {
            var config;
            // old style pre 7.0
            if (tile.properties == null) {
                config = tile.configurationProperties;
            } else {
                // new style since 7.0
                config = tile.properties;
            }
            return !_.isEmpty(config.servicenowServer);
        }

        function getColor(value) {
            if (predefinedColors[value]) return predefinedColors[value];
            return colorPool.pop();
        }

        function getTitle(){
            if(vm.issuesSummaryData.total > 1){
                return "tickets";
            }
            else{
                return "ticket";
            }
        }

        vm.chartOptions = {
            topTitleText: function (data) {
                return data.total;
            },
            bottomTitleText: getTitle,
            series: function (data) {
                var series = {
                    name: 'State',
                    data: []
                };
                series.data = _.map(data.data, function (value) {
                    return {y: value.counter, name: value.state, color: value.color};
                });
                return [ series ];
            },
            showLegend: false,
            donutThickness: '60%'
        };

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                ServiceNowQueryService.executeQuery(tile.id, config).then(
                    function (response) {
                        var serviceNowIssueArray = [];
                        var issues = response.data.data;
                        if(issues[0] === "Invalid table name"){
                            vm.invalidTableName = true;
                        }
                        else{
                            vm.invalidTableName = false;
                            vm.states = [];
                            vm.statesCounter = 0;
                            vm.issuesSummaryData = {
                                data: null,
                                total: 0
                            };
                            vm.issuesSummaryData.data = _.reduce(issues, function (result, value) {
                                var state = value.state;
                                vm.issuesSummaryData.total += 1;
                                if (result[state]) {
                                result[state].counter += 1;
                            } else {
                                result[state] = {
                                    counter: 1,
                                    color: getColor(state),
                                    state: state
                                };
                            }
                            value.color = result[state].color;
                            serviceNowIssueArray.push(value);
                            return result;

                        }, {});
                        _.forEach(vm.issuesSummaryData.data, function (value, key) {
                            if (vm.statesCounter < 5) vm.states.push(value);
                            vm.statesCounter++;
                        });
                        vm.gridOptions = createGridOptions(serviceNowIssueArray);
                        }
                    }
                ).finally(function () {
                    vm.loading = false;

                });
            }
        }

        function createGridOptions(serviceNowData) {
            var filterHeaderTemplate = "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>";
            var columnDefs = [
                    {
                        displayName: "Number",
                        field: "number",
                        cellTemplate: "static/@project.version@/include/ServiceNowQueryTile/grid/number-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '18%'
                    },
                    {
                        displayName: "Short description",
                        field: "short_description",
                        cellTemplate: "static/@project.version@/include/ServiceNowQueryTile/grid/short-description-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '25%'
                    },
                    {
                        displayName: "Priority",
                        field: "priority",
                        cellTemplate: "static/@project.version@/include/ServiceNowQueryTile/grid/priority-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '18%'
                    },
                    {
                        displayName: "State",
                        field: "state",
                        cellTemplate: "static/@project.version@/include/ServiceNowQueryTile/grid/state-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '19%'
                    },
                    {
                        displayName: "Assigned To",
                        field: "assigned_to",
                        cellTemplate: "static/@project.version@/include/ServiceNowQueryTile/grid/assigned-to-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: false,
                        width: '20%'
                    }
                ];
            return XlrTileHelper.getGridOptions(serviceNowData, columnDefs);
        }

        function refresh() {
            load({params: {refresh: true}});
        }

        load();

        vm.refresh = refresh;
    };

    ServiceNowQueryTileViewController.$inject = ['$scope', 'xlrelease.serviceNow.ServiceNowQueryService', 'XlrTileHelper'];

    var ServiceNowQueryService = function (Backend) {

        function executeQuery(tileId, config) {
            return Backend.get("/tiles/" + tileId + "/data", config);
        }
        return {
            executeQuery: executeQuery
        };
    };

    ServiceNowQueryService.$inject = ['Backend'];

    angular.module('xlrelease.ServiceNow.tile', []);
    angular.module('xlrelease.ServiceNow.tile').service('xlrelease.serviceNow.ServiceNowQueryService', ServiceNowQueryService);
    angular.module('xlrelease.ServiceNow.tile').controller('serviceNow.ServiceNowQueryTileViewController', ServiceNowQueryTileViewController);

})();

