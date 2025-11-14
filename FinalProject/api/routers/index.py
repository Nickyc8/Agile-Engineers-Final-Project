from . import (orders, order_details, customers, sandwiches,
    resources, recipes, promotions,reviews, payment_details
)


def load_routes(app):
    app.include_router(customers.router)
    app.include_router(sandwiches.router)
    app.include_router(resources.router)
    app.include_router(recipes.router)
    app.include_router(promotions.router)
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(reviews.router)
    app.include_router(payment_details.router)