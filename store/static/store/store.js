"use strict";

function indexBy(data, key='id') {
    const d = {};
    for (let p of data) {
        d[p.id] = p;
    }
    return d;
}

var m = angular.module("store", ["ngRoute", "dj"]);

m.filter('upperCase', function () {
   return function(input) {
       return input.toTitleCase();
   }
});

m.factory('inventory', function InventoryService($http, apiPaths) {
    return $http.get(apiPaths.product_list).then(resp => resp.data);
});

m.factory('inventoryById', function InventorByIdService(inventory) {
    return inventory.then(indexBy);
});


m.config(function ($routeProvider, basePath) {

    //console.log('CONFIG PHASE', $routeProvider);

    $routeProvider.when('/', {
        templateUrl: basePath + 'directory.html'
    });

        $routeProvider.when('/inventory/:invId/', {
        templateUrl: basePath + 'inventory.html',
        controller: function InventoryController(inventory) {
            // console.log(inventory);
            this.inventory = inventory;
        },
        controllerAs: '$ctrl',
        resolve: {
            inventory: function ($route, inventoryById) {
                // console.log($route);
                return inventoryById.then(data => data[$route.current.params.invId]);
            }
        }
    });

    $routeProvider.when('/inventory/:invId/product/:prodId/', {
        templateUrl: basePath + 'product.html',
        controller: function ProductController(product, $routeParams) {
            console.log(product.inventory.filter(value => value.id === Number($routeParams.prodId))[0]);
            // console.log(product.inventory);
            this.product = product.inventory.filter(value => value.id === Number($routeParams.prodId))[0];
            this.parent = $routeParams.invId;
        },
        controllerAs: '$ctrl',
        resolve: {
            product: function ($route, inventoryById) {
                // console.log($route);
                return inventoryById.then(data => data[$route.current.params.invId]);
            }
        }
    });

    // $routeProvider.when('/product/:id/', {
    //     templateUrl: basePath + 'product.html',
    //     controller: function ProductCtrl(product) {
    //         this.product = product;
    //     },
    //     controllerAs: '$ctrl',
    //     resolve: {
    //         product: function ($route, inventoryById) {
    //             return inventoryById.then(data => data[$route.current.params.id]);
    //         }
    //     }
    // });


});

// m.run(function ($rootScope, basePath) {
//     $rootScope.mainTemplate = basePath + "main.html";
// });


m.controller('StoreCtrl', function StoreCtrl(inventory) {
    this.loaded = false;
    this.loadingMessage = "Loading inventory...";
    inventory.then(data => {
        this.inventory = data;
        this.loaded = true;
    }).catch(()=> {
        this.loadingMessage = "Something went terribly wrong. sorry."
    });

    this.cartItems = [];

    this.addToCart = product => {
        for (let p of this.cartItems) {
            if (p.product.id === product.id) {
                p.amount++;
                return;
            }
        }
        this.cartItems.push(
            {product: product, amount: 1}
        );
    };

});

/* 
  * To Title Case 2.1 – http://individed.com/code/to-title-case/
  * Copyright © 2008–2013 David Gouch. Licensed under the MIT License.
 */

String.prototype.toTitleCase = function(){
  var smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;

  return this.replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g, function(match, index, title){
    if (index > 0 && index + match.length !== title.length &&
      match.search(smallWords) > -1 && title.charAt(index - 2) !== ":" &&
      (title.charAt(index + match.length) !== '-' || title.charAt(index - 1) === '-') &&
      title.charAt(index - 1).search(/[^\s-]/) < 0) {
      return match.toLowerCase();
    }

    if (match.substr(1).search(/[A-Z]|\../) > -1) {
      return match;
    }

    return match.charAt(0).toUpperCase() + match.substr(1);
  });
};