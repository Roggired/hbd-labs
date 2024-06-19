package hbd.service.domain.service

import hbd.service.domain.entity.OrderEntity
import hbd.service.domain.entity.toModel
import hbd.service.domain.model.DeliveryMan
import hbd.service.domain.model.Order
import hbd.service.domain.repository.DeliveryManRepository
import hbd.service.domain.repository.OrderRepository
import hbd.service.http.request.OrderDto
import hbd.service.http.request.OrderRequest
import org.springframework.data.domain.Page
import org.springframework.data.domain.PageRequest
import org.springframework.data.domain.Sort
import org.springframework.stereotype.Service
import java.time.LocalDateTime
import java.util.*

@Service
class DeliveryService(
    private val orderRepository: OrderRepository,
    private val deliveryManRepository: DeliveryManRepository
) {

    fun getAllDeliveryMen(pageSize: Int, pageNumber: Int): Page<DeliveryMan> {
        return deliveryManRepository.findAll(PageRequest.of(pageNumber, pageSize)).map { it.toModel() }
    }

    fun getAllOrders(pageSize: Int, pageNumber: Int, orderRequest: OrderRequest?): Page<Order> {
        val sort = if (orderRequest?.sortField != null)
            Sort.by(orderRequest.sortField.map { Sort.Order(it.order, it.field.fieldName) })
        else Sort.by("id")
        return orderRepository.findAll(PageRequest.of(pageNumber, pageSize, sort)).map { it.toModel() }
    }

    fun createOrder(orderDto: OrderDto): Order {
        return orderRepository.save(
            OrderEntity(
                id = UUID.randomUUID(),
                orderDateCreated = LocalDateTime.now(),
                deliveryId = orderDto.deliveryId,
                deliveryManId = orderDto.deliveryManId,
                deliveryAddress = orderDto.deliveryAddress,
                deliveryTime = orderDto.deliveryTime,
                rating = orderDto.rating,
                tips = orderDto.tips
            )
        ).toModel()
    }

}