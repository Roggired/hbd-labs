package hbd.service.domain.service

import hbd.service.domain.entity.DeliveryManEntity
import hbd.service.domain.entity.OrderEntity
import hbd.service.domain.repository.DeliveryManRepository
import hbd.service.domain.repository.OrderRepository
import hbd.service.http.OrderRequest
import org.springframework.data.domain.Page
import org.springframework.data.domain.PageRequest
import org.springframework.data.domain.Sort
import org.springframework.stereotype.Service
import java.time.LocalDateTime

@Service
class DeliveryService(
    private val orderRepository: OrderRepository,
    private val deliveryManRepository: DeliveryManRepository
) {

    fun getAllDeliveryMen(
        pageSize: Int,
        pageNumber: Int
    ): Page<DeliveryManEntity> = deliveryManRepository.findAll(
        PageRequest.of(pageNumber, pageSize, Sort.by("id"))
    )

    fun getAllOrders(
        pageSize: Int,
        pageNumber: Int,
        orderRequest: OrderRequest
    ): Page<OrderEntity> = orderRepository.findAllFiltered(
        deliveryTimeFilterClause = LocalDateTime.parse(orderRequest.deliveryTimeFilterClause),
        pageable = PageRequest.of(pageNumber, pageSize, Sort.by("orderDateCreated"))
    )
}
