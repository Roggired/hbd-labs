package hbd.service.domain.entity

import hbd.service.domain.model.Order
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import java.time.LocalDateTime
import java.util.*

@Entity(name = "orders")
class OrderEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID,
    @Column(name = "order_date_created")
    val orderDateCreated: LocalDateTime,
    @Column(name = "delivery_id")
    val deliveryId: String,
    @Column(name = "deliveryman_id")
    val deliveryManId: String,
    @Column(name = "delivery_address")
    val deliveryAddress: String,
    @Column(name = "delivery_time")
    val deliveryTime: LocalDateTime,
    val rating: Double,
    val tips: Double?
)

fun OrderEntity.toModel(): Order = Order(
    orderId = id,
    orderDateCreated = orderDateCreated,
    deliveryId = deliveryId,
    deliveryManId = deliveryManId,
    deliveryAddress = deliveryAddress,
    deliveryTime = deliveryTime,
    rating = rating,
    tips = tips
)