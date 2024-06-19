package hbd.service.domain.model

import java.time.LocalDateTime
import java.util.*

data class Order(
    val orderId: UUID,
    val orderDateCreated: LocalDateTime,
    val deliveryId: String,
    val deliveryManId: String,
    val deliveryAddress: String,
    val deliveryTime: LocalDateTime,
    val rating: Double,
    val tips: Double?
)


