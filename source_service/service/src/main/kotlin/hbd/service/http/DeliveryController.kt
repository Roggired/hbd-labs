package hbd.service.http

import hbd.service.domain.model.DeliveryMan
import hbd.service.domain.model.Order
import hbd.service.domain.service.DeliveryService
import hbd.service.http.request.OrderDto
import hbd.service.http.request.OrderRequest
import org.springframework.data.domain.Page
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/delivery/")
class DeliveryController(
    private val deliveryService: DeliveryService
) {

    @PostMapping("/orders")
    fun getAllOrders(
        @RequestParam pageSize: Int,
        @RequestParam pageNumber: Int,
        @RequestBody orderRequest: OrderRequest?
    ): Page<Order> = deliveryService.getAllOrders(pageSize, pageNumber, orderRequest)


    @GetMapping("/delivers")
    fun getAllDeliveryMen(
        @RequestParam pageSize: Int,
        @RequestParam pageNumber: Int
    ): Page<DeliveryMan> = deliveryService.getAllDeliveryMen(pageSize = pageSize, pageNumber = pageNumber)


    @PostMapping("/order")
    fun createOrder(
        @RequestBody orderDto: OrderDto
    ): Order {
        return deliveryService.createOrder(orderDto)
    }
}