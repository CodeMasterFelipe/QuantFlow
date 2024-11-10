from quantflow.core.events import FillEvent
from quantflow.core.types import Order, OrderStatus
import uuid


class OrderManagementSystem:
    def __init__(self, event_queue, execution_handler):
        self.event_queue = event_queue
        self.execution_handler = execution_handler
        self.order_book = {}

    def handle_order_request(self, order_request):
        order = self.create_order(order_request)
        self.order_book[order.order_id] = order
        return self.execution_handler.execute_order(order)

    def recieve_fill(self, fill):
        order = self.order_book.get(fill.order_id)
        if order:
            order.status = OrderStatus.FILLED
            self.event_queue.put(FillEvent(fill))

    def create_order(self, order_request):
        order_id = self.generate_order_id()
        return Order(
            order_id=order_id,
            symbol=order_request.symbol,
            price=order_request.price,
            order_type=order_request.order_type,
            quantity=order_request.quantity,
            stop_loss=order_request.stop_loss,
            take_profit=order_request.take_profit,
            status=OrderStatus.NEW,
        )

    def generate_order_id(self):
        return str(uuid.uuid4())
    
    def check_stoploss_takeprofit(self):
        self.execution_handler.check_stoploss_takeprofit()
