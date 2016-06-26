angular.module("store").component('cart', {
    templateUrl: "/static/store/cart.component.html",  // TODO: how to inject to component?
    bindings: {
        items: '=',
    },
    controller: function CartController() {
        this.total = () => this.items.reduce(
            (prev, current) => prev + current.product.price * current.amount, 0)
        this.checkDelete = (item, action) => {
            if (action === 'click' || item.amount === 0) {
                console.log('Clicked');
                this.items.splice(this.items.indexOf(item), 1);
            }
        };
    }
});

